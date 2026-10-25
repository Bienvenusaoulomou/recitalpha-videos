"""Récitalpha EP01 renderer — procedural motion graphics, 1080x1920 @30fps, piped to ffmpeg."""
import json, math, os, random, re, subprocess, sys
import numpy as np
import skia

ROOT = os.environ.get("REC_ROOT", "/home/claude/rec")
sys.path.insert(0, ROOT)
from script import CAPTION_OVERRIDES

W, H, FPS = 1080, 1920, 30
CX = W / 2
FONTS = "/home/claude/rec/fonts"
TL = json.load(open(f"{ROOT}/timeline.json"))
TOTAL = TL["total"]
SCENES = TL["scenes"]
SCN = {s["id"]: s for s in SCENES}

CLEAN = "--clean" in sys.argv          # no captions (for re-voicing)
PREVIEW = None                         # e.g. --frames 10,200,400 renders PNGs only
for a in sys.argv:
    if a.startswith("--frames="):
        PREVIEW = [int(x) for x in a.split("=")[1].split(",")]
OUT = f"{ROOT}/out_clean.mp4" if CLEAN else f"{ROOT}/out.mp4"

# ---------- palette & fonts ----------
def C(rgb, a=1.0):
    r, g, b = rgb
    return skia.ColorSetARGB(int(max(0, min(1, a)) * 255), r, g, b)

BG, CREAM, GOLD, GOLD2 = (12, 11, 9), (243, 233, 210), (214, 168, 75), (246, 205, 112)
RED, MUTED, DARK, INK = (206, 62, 44), (150, 138, 115), (30, 27, 22), (24, 20, 16)

def TF(p): return skia.Typeface.MakeFromFile(p)
ANTON = TF(f"{FONTS}/Anton-Regular.ttf")
BEBAS = TF(f"{FONTS}/BebasNeue-Regular.ttf")
PLAY = TF(f"{FONTS}/PlayfairDisplay[wght].ttf")
POPB = TF("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf")
_fc = {}
def F(tf, size):
    k = (id(tf), int(size))
    if k not in _fc:
        f = skia.Font(tf, size); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias)
        _fc[k] = f
    return _fc[k]

# ---------- easing / timing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def eo(x): return 1 - (1 - x) ** 3                      # ease-out cubic
def eio(x): return 3 * x * x - 2 * x * x * x
def back(x, s=1.7): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

# ---------- caption word timing ----------
def norm(w): return re.sub(r"[^a-z0-9$%]", "", w.lower())
WORDS = []   # dicts: w, t0, t1, scene, si, wi
for sc in SCENES:
    for si, s in enumerate(sc["sentences"]):
        cap = CAPTION_OVERRIDES.get(s["text"], s["text"])
        ws = cap.split()
        wts = []
        for w in ws:
            k = len(w) + 2
            if re.search(r"\d", w): k += 7
            if w.endswith((",", ".", ":", "?", "!", "...")): k += 4
            wts.append(k)
        tot = sum(wts); t = s["start"]; dur = s["end"] - s["start"]
        for wi, (w, k) in enumerate(zip(ws, wts)):
            d = dur * k / tot
            WORDS.append(dict(w=w, t0=t, t1=t + d, scene=sc["id"], si=si, wi=wi, send=s["end"]))
            t += d

def wt(sid, word, nth=0):
    """time (relative to scene start) when caption word `word` starts in scene sid"""
    n = 0
    for x in WORDS:
        if x["scene"] == sid and norm(x["w"]) == norm(word):
            if n == nth: return x["t0"] - SCN[sid]["start"]
            n += 1
    raise KeyError((sid, word))

def beat(sid, i): return SCN[sid]["sentences"][i]["start"] - SCN[sid]["start"]

# caption chunks
CHUNKS = []
for sc in SCENES:
    for si in range(len(sc["sentences"])):
        ws = [x for x in WORDS if x["scene"] == sc["id"] and x["si"] == si]
        cur = []
        for x in ws:
            cur.append(x)
            txt = " ".join(y["w"] for y in cur)
            if len(cur) >= 3 or len(txt) >= 15 or x["w"].endswith((",", ".", ":", "?", "!")):
                CHUNKS.append(cur); cur = []
        if cur: CHUNKS.append(cur)
for i, ch in enumerate(CHUNKS):
    end = ch[-1]["send"] + 0.12
    if i + 1 < len(CHUNKS): end = min(end, CHUNKS[i + 1][0]["t0"])
    for x in ch: x["chunk_end"] = end

# ---------- drawing helpers ----------
def P(color, stroke=0, aa=True, cap=None):
    p = skia.Paint(AntiAlias=aa, Color=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeJoin(skia.Paint.kRound_Join)
        p.setStrokeCap(cap or skia.Paint.kRound_Cap)
    return p

def text_w(s, font, spacing=0):
    return font.measureText(s) + spacing * max(0, len(s) - 1)

def text(c, s, x, y, tf, size, rgb, a=1.0, align="c", spacing=0, glow=0, stroke=None, glow_rgb=None):
    f = F(tf, size)
    w = text_w(s, f, spacing)
    if a <= 0.002: return w
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    def draw(paint):
        if spacing == 0:
            c.drawString(s, x0, y, f, paint)
        else:
            xx = x0
            for ch in s:
                c.drawString(ch, xx, y, f, paint); xx += f.measureText(ch) + spacing
    if glow:
        gp = P(C(glow_rgb or rgb, a * 0.55)); gp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, glow))
        draw(gp)
    if stroke:
        draw(P(C(stroke[0], a), stroke=stroke[1]))
    draw(P(C(rgb, a)))
    return w

def shadowed(c, fn, blur=18, a=0.6):
    # draws fn() into a layer with a drop shadow
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.DropShadow(0, 10, blur, blur, C((0, 0, 0), a)))
    c.saveLayer(None, p); fn(); c.restore()

def layer_alpha(c, a):
    c.saveLayerAlpha(None, int(clamp(a) * 255))

def person(c, x, y, r, rgb, a=1.0):
    p = P(C(rgb, a))
    c.drawCircle(x, y - r * 0.55, r * 0.42, p)
    c.drawRoundRect(skia.Rect(x - r * 0.72, y - r * 0.05, x + r * 0.72, y + r * 0.95), r * 0.6, r * 0.6, p)

def coin(c, x, y, r, a=1.0, label=None, size=None):
    c.drawCircle(x, y, r, P(C((150, 112, 40), a)))
    c.drawCircle(x, y - r * 0.04, r * 0.96, P(C(GOLD, a)))
    c.drawCircle(x, y - r * 0.04, r * 0.78, P(C((176, 132, 52), a), stroke=max(1.5, r * 0.06)))
    if label:
        text(c, label, x, y + (size or r * 0.6) * 0.36, ANTON, size or r * 0.6, (70, 50, 18), a)

def stamp(c, x, y, label, rgb, size, ang, a, sc=1.0, sub=None):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(sc, sc)
    f = F(ANTON, size); w = f.measureText(label)
    pad = size * 0.32; h = size * 1.05 + (size * 0.5 if sub else 0)
    r = skia.Rect(-w / 2 - pad, -h / 2 - pad * 0.6, w / 2 + pad, h / 2 + pad * 0.6)
    c.drawRoundRect(r, 18, 18, P(C(rgb, a), stroke=10))
    r2 = skia.Rect(r.left() + 16, r.top() + 16, r.right() - 16, r.bottom() - 16)
    c.drawRoundRect(r2, 10, 10, P(C(rgb, a * 0.8), stroke=3))
    yy = size * 0.36 - (size * 0.25 if sub else 0)
    text(c, label, 0, yy, ANTON, size, rgb, a)
    if sub: text(c, sub, 0, yy + size * 0.62, BEBAS, size * 0.48, rgb, a, spacing=4)
    c.restore()

def rule(c, x0, x1, y, rgb, a, w=3):
    c.drawLine(x0, y, x1, y, P(C(rgb, a), stroke=w))

def fmt_money(v): return "${:,.0f}".format(v)

# ---------- static layers ----------
rng = np.random.default_rng(7)
def mk_img(arr): return skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.kRGBA_8888_ColorType)
GRAIN = []
for i in range(6):
    n = rng.normal(128, 34, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
    n = np.repeat(np.repeat(n, 2, 0), 2, 1)
    arr = np.dstack([n, n, n, np.full_like(n, 255)])
    GRAIN.append(mk_img(arr))

def vignette_paint():
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(CX, 820), 1180,
        [C((0, 0, 0), 0), C((0, 0, 0), 0.25), C((0, 0, 0), 0.85)], [0.0, 0.55, 1.0]))
    return p
VIG = vignette_paint()

DUST = [(random.Random(i).uniform(0, W), random.Random(i + 99).uniform(0, H),
         random.Random(i + 7).uniform(1.2, 3.2), random.Random(i + 3).uniform(8, 26),
         random.Random(i + 5).uniform(0.15, 0.45)) for i in range(70)]


# ---------- FX v2 (2026-10-25): punch-zoom hits, whip transitions, light leaks, embers, b-roll ----------
FX = True
HITS = []      # absolute seconds of impact moments (set with set_hits(IMPACTS))
BROLL = {}     # scene_id -> dict(frames=[skia.Image], fps=, alpha=, credit=)
def set_hits(impacts):
    global HITS
    out = []
    for item in impacts:
        sid, w, off = item[0], item[1], item[2]
        if sid in SCN:
            try: out.append(SCN[sid]["start"] + wt(sid, w) + off)
            except Exception: pass
    HITS = sorted(out)

def load_broll(path, start=0.0, dur=6.0, fps=15, alpha=0.5, credit=None, w=540, h=960):
    """Decode a clip with ffmpeg, crop to 9:16, grade to Récitalpha sepia. Returns a dict for BROLL[scene_id]."""
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(start), "-t", str(dur), "-i", path,
           "-vf", f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (w * h * 3)
    frames = []
    alpha_ch = np.full((h, w, 1), 255, np.uint8)
    for i in range(n):   # frame by frame to keep memory low
        f = np.frombuffer(raw, np.uint8, count=w * h * 3, offset=i * w * h * 3).reshape(h, w, 3).astype(np.float32)
        g = np.clip((f.mean(axis=2, keepdims=True) / 255.0 - 0.08) * 1.15, 0, 1)
        sep = (np.concatenate([g * 245, g * 205, g * 150], axis=2) * 0.85 + 6).astype(np.uint8)
        frames.append(mk_img(np.concatenate([sep, alpha_ch], axis=2)))
    del raw
    return dict(frames=frames, fps=fps, alpha=alpha, credit=credit)

def hit_k(t):
    k = 0.0
    for h in HITS:
        if 0 <= t - h < 0.6: k = max(k, math.exp(-(t - h) * 7.0))
    return k

EMBERS = [(random.Random(i * 7).uniform(0, W), random.Random(i * 13).uniform(0, H), random.Random(i * 3).uniform(2.0, 5.5),
           random.Random(i * 5).uniform(30, 90), random.Random(i * 11).uniform(0, 6.28)) for i in range(46)]
def fx_background(c, t, sid, lt):
    b = BROLL.get(sid)
    if b and b["frames"]:
        i = min(len(b["frames"]) - 1, int(lt * b["fps"]) % len(b["frames"]))
        img = b["frames"][i]
        pa = skia.Paint(); pa.setAlphaf(b["alpha"])
        zz = 1.0 + 0.06 * (lt / 6.0)
        c.save(); c.translate(CX, H / 2); c.scale(zz, zz); c.translate(-CX, -H / 2)
        c.drawImageRect(img, skia.Rect(0, 0, W, H), skia.SamplingOptions(skia.FilterMode.kLinear), pa)
        c.restore()
        sh = skia.Paint()
        sh.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)],
                     [C(BG, 0.75), C(BG, 0.25), C(BG, 0.35), C(BG, 0.9)], [0.0, 0.3, 0.6, 1.0]))
        c.drawRect(skia.Rect(0, 0, W, H), sh)
        if b.get("credit"):
            text(c, b["credit"], W - 60, 1262, BEBAS, 26, MUTED, 0.8, align="r", spacing=2)
    # moving light leak
    lx = CX + 520 * math.sin(t * 0.23); ly = 520 + 380 * math.sin(t * 0.17 + 1.3)
    lp = skia.Paint(); lp.setBlendMode(skia.BlendMode.kScreen)
    lp.setShader(skia.GradientShader.MakeRadial(skia.Point(lx, ly), 620, [C((255, 190, 90), 0.16), C((255, 190, 90), 0.0)], [0.0, 1.0]))
    c.drawRect(skia.Rect(0, 0, W, H), lp)
    # rising embers
    for (x, y, r, sp, ph) in EMBERS:
        yy = (y - t * sp) % H; xx = x + 18 * math.sin(t * 0.8 + ph)
        a = 0.25 + 0.25 * math.sin(t * 2.0 + ph)
        gp = P(C(GOLD2, a * 0.6)); gp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 1.6))
        c.drawCircle(xx, yy, r * 1.4, gp)
        c.drawCircle(xx, yy, r * 0.5, P(C((255, 236, 190), a)))

RED_SCENES = {"collapse", "damage"}
def background(c, t, sid):
    c.clear(C(BG))
    warm = (120, 26, 18) if sid in RED_SCENES else (92, 68, 30)
    br = 0.55 + 0.08 * math.sin(t * 0.9)
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(CX, 760 + 30 * math.sin(t * 0.3)), 820,
        [C(warm, br), C(warm, 0.0)], [0.0, 1.0]))
    c.drawRect(skia.Rect(0, 0, W, H), p)
    # faint 1920s art-deco frame lines
    fa = 0.10
    c.drawRoundRect(skia.Rect(46, 300, W - 46, 1225), 6, 6, P(C(GOLD, fa), stroke=2))
    for (x, y) in ((46, 300), (W - 46, 300), (46, 1225), (W - 46, 1225)):
        c.drawCircle(x, y, 5, P(C(GOLD, 0.25)))
    for (x, y, r, sp, a) in DUST:
        yy = (y - t * sp) % H; xx = x + 10 * math.sin(t * 0.5 + y)
        c.drawCircle(xx, yy, r, P(C(CREAM, a * 0.5)))

def overlays(c, fi):
    c.drawRect(skia.Rect(0, 0, W, H), VIG)
    gp = skia.Paint(); gp.setBlendMode(skia.BlendMode.kOverlay); gp.setAlphaf(0.16)
    c.drawImage(GRAIN[fi % len(GRAIN)], 0, 0, skia.SamplingOptions(), gp)

END_CARD_AT = None
def brand(c, t, sid):
    a = 1.0
    last = SCENES[-1]["id"]
    if sid == last and END_CARD_AT is not None and t - SCN[last]["start"] > END_CARD_AT - 0.3: a = 0.0
    a *= prog(t, 0.2, 0.6)
    text(c, "RÉCITALPHA", CX, 236, BEBAS, 46, GOLD, a * 0.85, spacing=10)
    rule(c, CX - 210, CX - 140, 220, GOLD, a * 0.5, 2); rule(c, CX + 140, CX + 210, 220, GOLD, a * 0.5, 2)
    # progress bar
    c.drawRoundRect(skia.Rect(140, 262, W - 140, 266), 2, 2, P(C(CREAM, 0.12 * a)))
    c.drawRoundRect(skia.Rect(140, 262, 140 + (W - 280) * clamp(t / TOTAL), 266), 2, 2, P(C(GOLD, 0.7 * a)))

# ---------- captions ----------
def captions(c, t):
    cur = None
    for x in WORDS:
        if x["t0"] <= t < x["chunk_end"]:
            cur = x; break
    if cur is None:
        # inside a chunk but between word boundaries -> find chunk by range
        return
    ch = next(ch for ch in CHUNKS if cur in ch)
    size = 72
    f = F(POPB, size)
    words = [y["w"] for y in ch]
    space = f.measureText(" ")
    total = sum(f.measureText(w) for w in words) + space * (len(words) - 1)
    while total > 820 and size > 50:
        size -= 4; f = F(POPB, size); space = f.measureText(" ")
        total = sum(f.measureText(w) for w in words) + space * (len(words) - 1)
    pop = 1 + 0.10 * (1 - eo(prog(t, ch[0]["t0"], 0.12)))
    c.save(); c.translate(CX, 1355); c.scale(pop, pop)
    x = -total / 2
    for y in ch:
        active = y["t0"] <= t
        is_now = y["t0"] <= t < y["t1"]
        rgb = GOLD2 if is_now else (CREAM if active else (205, 198, 182))
        text(c, y["w"], x, 0, POPB, size, rgb, 1.0, align="l", stroke=((8, 7, 6), 13))
        x += f.measureText(y["w"]) + space
    c.restore()

# ---------- scenes ----------
def sc_hook(c, t, D):
    a = eo(prog(t, 0.1, 0.5))
    text(c, "BOSTON · 1920", CX, 430, BEBAS, 96, GOLD, a, spacing=6)
    p = eo(prog(t, wt("hook", "double") - 0.1, 1.6))
    val = int(lerp(100, 200, p) / 1) if p > 0 else 100
    done = p >= 1
    pulse = 1 + 0.12 * math.sin(math.pi * prog(t, wt("hook", "double") + 1.5, 0.35))
    a2 = eo(prog(t, 0.35, 0.5))
    c.save(); c.translate(CX, 820); c.scale(pulse, pulse)
    shadowed(c, lambda: text(c, f"${val}", 0, 0, ANTON, 320, GOLD2 if done else CREAM, a2,
                             glow=30 if done else 0, glow_rgb=GOLD))
    c.restore()
    a3 = eo(prog(t, wt("hook", "90"), 0.4))
    text(c, "IN 90 DAYS", CX, 950, BEBAS, 104, CREAM, a3, spacing=8)
    tb = beat("hook", 1)
    pb = prog(t, wt("hook", "paid") - 0.05, 0.22)
    if pb > 0:
        stamp(c, CX, 1150, "PAID", GOLD2, 84, -10, pb, sc=lerp(1.8, 1.0, eo(pb)))
    # coin burst
    tc = t - (wt("hook", "paid") - 0.05)
    if tc > 0:
        for i in range(34):
            R = random.Random(i)
            ang = R.uniform(-math.pi, 0); sp = R.uniform(500, 1200)
            x = CX + math.cos(ang) * sp * tc
            y = 1150 + math.sin(ang) * sp * tc + 1400 * tc * tc
            if 0 < y < 1260 and tc > 0.12: coin(c, x, y, R.uniform(12, 20), clamp(1.4 - tc))

def ship(c, x, y, t, a):
    c.save(); c.translate(x, y + 7 * math.sin(t * 2.2)); c.rotate(1.6 * math.sin(t * 1.7))
    for i in range(6):  # smoke
        st = (t * 0.7 + i / 6) % 1
        for fx in (-70, 20):
            c.drawCircle(fx + 25 - st * 120, -200 - st * 190, 16 + st * 34, P(C(MUTED, a * 0.35 * (1 - st))))
    hull = skia.Path()
    hull.moveTo(-280, 0); hull.lineTo(270, 0); hull.lineTo(215, 78); hull.lineTo(-235, 78); hull.close()
    c.drawPath(hull, P(C(DARK, a))); c.drawPath(hull, P(C(GOLD, a), stroke=4))
    c.drawRect(skia.Rect(-200, 22, 200, 30), P(C(RED, a * 0.8)))
    sup = skia.Rect(-170, -62, 140, 0)
    c.drawRect(sup, P(C(DARK, a))); c.drawRect(sup, P(C(GOLD, a), stroke=4))
    for wx in range(-150, 130, 36):
        c.drawCircle(wx, -31, 7, P(C(GOLD2, a * 0.8)))
    for fx in (-70, 20):
        fr = skia.Rect(fx, -165, fx + 52, -62)
        c.drawRect(fr, P(C(DARK, a))); c.drawRect(fr, P(C(GOLD, a), stroke=4))
        c.drawRect(skia.Rect(fx, -150, fx + 52, -132), P(C(RED, a * 0.9)))
    c.restore()

def waves(c, t, y0, a):
    for i in range(4):
        path = skia.Path(); yy = y0 + i * 28
        for x in range(0, W + 20, 20):
            yv = yy + 9 * math.sin(x * 0.018 + t * (1.6 + i * 0.3) + i)
            (path.moveTo if x == 0 else path.lineTo)(x, yv)
        c.drawPath(path, P(C(MUTED, a * (0.55 - i * 0.1)), stroke=3))

def man(c, x, y, a, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(0, -40), 330, [C(GOLD, 0.35 * a), C(GOLD, 0)], None))
    c.drawCircle(0, -40, 330, g)
    fill, edge = P(C(INK, a)), P(C(GOLD, a), stroke=5)
    body = skia.Path(); body.moveTo(-235, 210); body.cubicTo(-230, 40, -120, 10, 0, 10); body.cubicTo(120, 10, 230, 40, 235, 210); body.close()
    c.drawPath(body, fill); c.drawPath(body, edge)
    collar = skia.Path(); collar.moveTo(-55, 14); collar.lineTo(0, 110); collar.lineTo(55, 14)
    c.drawPath(collar, P(C(GOLD, a * 0.8), stroke=5))
    c.drawOval(skia.Rect(-78, -190, 78, 10), fill); c.drawOval(skia.Rect(-78, -190, 78, 10), edge)
    brim = skia.Rect(-150, -175, 150, -140)
    c.drawOval(brim, fill); c.drawOval(brim, edge)
    crown = skia.Path(); crown.moveTo(-92, -158); crown.cubicTo(-96, -250, -60, -275, 0, -262); crown.cubicTo(60, -275, 96, -250, 92, -158); crown.close()
    c.drawPath(crown, fill); c.drawPath(crown, edge)
    c.drawRect(skia.Rect(-90, -185, 90, -162), P(C(GOLD, a * 0.85)))
    c.drawCircle(0, -78, 6, P(C(GOLD, 0)))  # placeholder (faceless)
    text(c, "?", 0, -40, PLAY, 120, GOLD, a * 0.55)
    c.restore()

def sc_arrival(c, t, D):
    b1, b2 = beat("arrival", 1), beat("arrival", 2)
    # name card
    out = eo(prog(t, b1 - 0.2, 0.5))
    a = eo(prog(t, 0.0, 0.6)) * (1 - out)
    if a > 0:
        man(c, CX, 760 - 40 * out, a, lerp(0.9, 1.0, eo(prog(t, 0, 1.2))))
        reveal = eo(prog(t, 0.25, 0.8))
        text(c, "CHARLES PONZI", CX, 1100, PLAY, 104, CREAM, a * reveal, spacing=lerp(30, 4, reveal))
        rule(c, CX - 300 * reveal, CX + 300 * reveal, 1140, GOLD, a, 3)
        text(c, "1882 — 1949", CX, 1200, BEBAS, 58, MUTED, a * reveal, spacing=6)
    # voyage
    if t > b1 - 0.3:
        a2 = eo(prog(t, b1 - 0.2, 0.5))
        text(c, "BOSTON · 1903", CX, 440, BEBAS, 96, GOLD, a2, spacing=6)
        waves(c, t, 770, a2)
        sx = lerp(-320, CX, eio(prog(t, b1 - 0.2, 2.4)))
        ship(c, sx, 720, t, a2)
        pc = prog(t, wt("arrival", "$2.50") - 0.15, 0.45)
        if pc > 0:
            sc = back(pc)
            c.save(); c.translate(CX, 1030); c.scale(sc, sc); c.rotate(lerp(-90, 0, eo(pc)))
            shadowed(c, lambda: coin(c, 0, 0, 120, 1.0, "$2.50", 74))
            c.restore()
        pg = eo(prog(t, wt("arrival", "gambled") - 0.05, 0.35))
        if pg > 0:
            text(c, "THE REST? GAMBLED AWAY.", CX, 1205, BEBAS, 64, RED, pg, spacing=3)

def sc_failure(c, t, D):
    a = eo(prog(t, 0.0, 0.4))
    text(c, "YEARS OF", CX, 440, BEBAS, 90, MUTED, a, spacing=10)
    shadowed(c, lambda: text(c, "FAILURE", CX, 600, ANTON, 170, CREAM, a))
    rows = [("ODD JOBS", wt("failure", "Odd"), 790), ("BAD SCHEMES", wt("failure", "Bad"), 935), ("PRISON", wt("failure", "prison."), 1080)]
    for lbl, t0, y in rows:
        p = eo(prog(t, t0 - 0.1, 0.3))
        if p <= 0: continue
        f = F(BEBAS, 118); w = f.measureText(lbl) + 6 * (len(lbl) - 1)
        text(c, lbl, CX + (1 - p) * 60, y, BEBAS, 118, CREAM, p * 0.92, spacing=6)
        s = eo(prog(t, t0 + 0.25, 0.25))
        if s > 0:
            c.drawLine(CX - w / 2 - 24, y - 42, CX - w / 2 - 24 + (w + 48) * s, y - 42, P(C(RED, 0.95), stroke=14))
        if lbl == "PRISON" and s > 0:
            for i in range(6):
                bx = CX - w / 2 - 40 + i * (w + 80) / 5
                c.drawLine(bx, y - 130 - (1 - s) * 200, bx, y + 20, P(C(MUTED, 0.6 * s), stroke=8))

def envelope(c, x, y, a, open_):
    c.save(); c.translate(x, y)
    r = skia.Rect(-270, -170, 270, 170)
    c.drawRoundRect(r, 10, 10, P(C((222, 208, 176), a)))
    fl = skia.Path(); fl.moveTo(-270, -170); fl.lineTo(0, lerp(10, -330, open_)); fl.lineTo(270, -170); fl.close()
    c.drawPath(fl, P(C((205, 188, 152), a))); c.drawPath(fl, P(C((160, 140, 100), a), stroke=3))
    side = skia.Path(); side.moveTo(-270, 170); side.lineTo(0, 10); side.lineTo(270, 170)
    c.drawPath(side, P(C((160, 140, 100), a), stroke=3))
    c.drawRect(skia.Rect(160, -140, 240, -60), P(C(RED, a * 0.9)))
    c.drawRect(skia.Rect(168, -132, 232, -68), P(C((240, 220, 190), a * 0.9), stroke=3))
    text(c, "ITALIA", -40, 110, PLAY, 44, (90, 70, 40), a * 0.7)
    c.restore()

def coupon_card(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.Rect(-210, -125, 210, 125)
    c.drawRect(r, P(C((246, 238, 214), a)))
    for i in range(22):
        xx = -210 + i * 20
        c.drawCircle(xx, -125, 6, P(C(BG, a))); c.drawCircle(xx, 125, 6, P(C(BG, a)))
    for i in range(13):
        yy = -125 + i * 20.8
        c.drawCircle(-210, yy, 6, P(C(BG, a))); c.drawCircle(210, yy, 6, P(C(BG, a)))
    c.drawRect(skia.Rect(-185, -100, 185, 100), P(C((120, 140, 110), a), stroke=4))
    c.drawCircle(-110, 0, 52, P(C((120, 140, 110), a), stroke=4))
    text(c, "IRC", -110, 14, BEBAS, 44, (90, 110, 80), a)
    text(c, "INTERNATIONAL", 55, -38, BEBAS, 34, (90, 110, 80), a, spacing=2)
    text(c, "REPLY", 55, 12, ANTON, 52, (60, 80, 55), a)
    text(c, "COUPON", 55, 66, ANTON, 52, (60, 80, 55), a)
    c.restore()

def arrow(c, x0, x1, y, p, rgb, a):
    xe = lerp(x0, x1, p)
    c.drawLine(x0, y, xe, y, P(C(rgb, a), stroke=8))
    if p > 0.05:
        hp = skia.Path(); hp.moveTo(xe + 6, y); hp.lineTo(xe - 26, y - 22); hp.lineTo(xe - 26, y + 22); hp.close()
        c.drawPath(hp, P(C(rgb, a)))

def sc_coupon(c, t, D):
    b1 = beat("coupon", 1)
    a = eo(prog(t, 0, 0.4))
    text(c, "ITALY · 1919", CX, 440, BEBAS, 96, GOLD, a, spacing=6)
    drop = prog(t, 0.05, 0.8)
    ey = lerp(-300, 800, back(drop, 1.2)) if drop < 1 else 800
    move = eio(prog(t, b1 - 0.2, 0.6))
    open_ = eo(prog(t, wt("coupon", "coupon") - 0.6, 0.5))
    ea = (1 - move)
    if ea > 0: envelope(c, CX, ey + 80 * open_, ea, open_)
    pc = eo(prog(t, wt("coupon", "coupon") - 0.3, 0.7))
    if pc > 0:
        cy = lerp(800, 690, pc); s = lerp(0.6, 1.25, pc)
        cy = lerp(cy, 560, move); s = lerp(s, 0.78, move)
        shadowed(c, lambda: coupon_card(c, CX, cy, s, pc))
    if move > 0:
        p1 = eo(prog(t, b1, 0.4)); p2 = eo(prog(t, wt("coupon", "America.") - 0.25, 0.4))
        text(c, "EUROPE", 270, 860, BEBAS, 96, CREAM, p1, spacing=4)
        text(c, "PAY LESS", 270, 950, BEBAS, 64, MUTED, p1, spacing=3)
        arrow(c, 420, 660, 828, eo(prog(t, wt("coupon", "traded") - 0.2, 0.7)), GOLD, 1.0 * p1)
        text(c, "AMERICA", 810, 860, BEBAS, 96, CREAM, p2, spacing=4)
        text(c, "GET MORE", 810, 950, BEBAS, 64, GOLD2, p2, spacing=3, glow=10 if p2 >= 1 else 0)
        q = eo(prog(t, wt("coupon", "America.") + 0.3, 0.5))
        if q > 0:
            text(c, "THE LOOPHOLE", CX, 1110, ANTON, 92, GOLD2, q, glow=18, glow_rgb=GOLD)

def sc_promise(c, t, D):
    tj = wt("promise", "January")
    b1 = beat("promise", 1)
    # LOOPHOLE flash
    a0 = eo(prog(t, 0, 0.3)) * (1 - eo(prog(t, tj - 0.3, 0.3)))
    if a0 > 0:
        text(c, "HE SAW", CX, 650, BEBAS, 90, MUTED, a0, spacing=10)
        text(c, "A WAY IN.", CX, 830, ANTON, 180, GOLD2, a0, glow=22, glow_rgb=GOLD)
    pc = eo(prog(t, tj - 0.2, 0.7))
    up = eio(prog(t, b1 - 0.2, 0.6))
    if pc > 0:
        c.save(); y = lerp(760, 470, up); s = lerp(1.0, 0.62, up)
        c.translate(CX, y); c.scale(s, s)
        rule(c, -360 * pc, 360 * pc, -150, GOLD, pc, 3); rule(c, -330 * pc, 330 * pc, -138, GOLD, pc * 0.6, 2)
        text(c, "SECURITIES", 0, -40, PLAY, 108, CREAM, pc, spacing=lerp(20, 4, pc))
        text(c, "EXCHANGE CO.", 0, 80, PLAY, 108, CREAM, pc, spacing=lerp(20, 4, pc))
        rule(c, -330 * pc, 330 * pc, 128, GOLD, pc * 0.6, 2); rule(c, -360 * pc, 360 * pc, 140, GOLD, pc, 3)
        text(c, "BOSTON · JANUARY 1920", 0, 215, BEBAS, 60, GOLD, pc * (1 - up), spacing=5)
        c.restore()
    p50 = prog(t, wt("promise", "50%") - 0.1, 0.4)
    if p50 > 0:
        s = back(p50)
        c.save(); c.translate(CX, 890); c.scale(s, s)
        shadowed(c, lambda: text(c, "+50%", 0, 0, ANTON, 330, GOLD2, 1.0, glow=30, glow_rgb=GOLD))
        c.restore()
    pr = prog(t, wt("promise", "45") - 0.1, 0.35)
    if pr > 0:
        ring = eio(prog(t, wt("promise", "45"), 1.4))
        cx, cy, R = CX, 1085, 92
        c.drawCircle(cx, cy, R, P(C(CREAM, 0.15 * pr), stroke=14))
        c.drawArc(skia.Rect(cx - R, cy - R, cx + R, cy + R), -90, 360 * ring, False, P(C(GOLD2, pr), stroke=14))
        text(c, "45", cx, cy + 22, ANTON, 76, CREAM, pr)
        text(c, "DAYS", cx + R + 30, cy + 24, BEBAS, 70, CREAM, pr, align="l", spacing=4)

PYR = []  # (row, x, y, r)
for row, n in enumerate([1, 2, 4, 8, 16]):
    y = 455 + row * 135
    gap = min(220, 880 / n); r = [34, 30, 26, 22, 17][row]
    for i in range(n):
        PYR.append((row, CX + (i - (n - 1) / 2) * gap, y, r))

def pyramid(c, t, rows_t, fall_t=None, yoff=0):
    for k, (row, x, y, r) in enumerate(PYR):
        p = eo(prog(t, rows_t[row], 0.35))
        if p <= 0: continue
        xx, yy, ang = x, y + yoff, 0
        if fall_t is not None and t > fall_t:
            R = random.Random(k); tt = t - fall_t - (4 - row) * 0.06 - R.uniform(0, 0.25)
            if tt > 0:
                xx += R.uniform(-300, 300) * tt; yy += 900 * tt * tt + R.uniform(-80, 0) * tt; ang = R.uniform(-400, 400) * tt
        c.save(); c.translate(xx, yy - (1 - p) * 30); c.rotate(ang)
        person(c, 0, 0, r, GOLD2 if row == 0 else CREAM, p)
        c.restore()

def sc_trick(c, t, D):
    tp, tn = wt("trick", "paid."), wt("trick", "next")
    rows_t = [0.0, 0.3, 0.6, tn - 0.2, tn + 0.05]
    text(c, "PONZI", CX + 80, 420, BEBAS, 44, GOLD, eo(prog(t, 0.2, 0.4)), align="l", spacing=3)
    pyramid(c, t, rows_t)
    # paid checks on early investors
    pk = eo(prog(t, tp - 0.15, 0.3))
    if pk > 0:
        for (row, x, y, r) in PYR:
            if row in (1, 2):
                cx, cy = x + r * 0.9, y - r * 1.05
                c.drawCircle(cx, cy, 15, P(C(GOLD, pk)))
                pth = skia.Path(); pth.moveTo(cx - 7, cy); pth.lineTo(cx - 2, cy + 6); pth.lineTo(cx + 8, cy - 6)
                c.drawPath(pth, P(C(INK, pk), stroke=4))
    # money flows up from new rows
    if t > tn + 0.3:
        tt = t - tn - 0.3
        bottom = [p for p in PYR if p[0] >= 3]; top = [p for p in PYR if p[0] in (1, 2)]
        for i in range(26):
            R = random.Random(i + 50)
            s0 = bottom[R.randrange(len(bottom))]; s1 = top[R.randrange(len(top))]
            ph = (tt * 0.9 + R.random()) % 1
            x = lerp(s0[1], s1[1], eio(ph)); y = lerp(s0[2] - 10, s1[2] + 20, eio(ph))
            coin(c, x, y, 11, math.sin(math.pi * ph) * clamp(tt * 2), "$", 12)
    pn = eo(prog(t, wt("trick", "coupons.") - 0.25, 0.3)) * (1 - eo(prog(t, wt("trick", "money") - 0.2, 0.25)))
    if pn > 0:
        w = text(c, "NOT FROM COUPONS", CX, 1135, ANTON, 84, RED, pn)
        c.drawLine(CX - w / 2 - 10, 1105, CX - w / 2 - 10 + (w + 20) * eo(prog(t, wt("trick", "coupons.") + 0.1, 0.25)), 1105, P(C(RED, pn), stroke=9))
    pm = eo(prog(t, wt("trick", "money") - 0.2, 0.3))
    if pm > 0:
        text(c, "NEW MONEY PAYS OLD INVESTORS", CX, 1135, BEBAS, 72, GOLD2, pm, spacing=2, glow=12 if pm >= 1 else 0, glow_rgb=GOLD)

CROWD = []
for gy in range(13):
    for gx in range(30):
        x = 85 + gx * 31 + (15 if gy % 2 else 0); y = 690 + gy * 30
        if x < 1000:
            d = math.hypot(x - CX, (y - 880) * 1.6)
            CROWD.append((x, y, d, random.Random(gx * 31 + gy).random()))

def sc_frenzy(c, t, D):
    a = eo(prog(t, 0, 0.3))
    th = wt("frenzy", "handed")
    pv = eio(prog(t, th - 0.2, 1.6))
    shadowed(c, lambda: text(c, fmt_money(10_000_000 * pv) + ("+" if pv >= 1 else ""), CX, 520, ANTON, 150, GOLD2 if pv >= 1 else CREAM, a, glow=24 if pv >= 1 else 0, glow_rgb=GOLD))
    text(c, "IN 7 MONTHS", CX, 610, BEBAS, 72, MUTED, eo(prog(t, wt("frenzy", "7") - 0.1, 0.3)), spacing=6)
    radius = lerp(0, 760, eio(prog(t, 0.1, wt("frenzy", "30,000") + 0.6)))
    for (x, y, d, rr) in CROWD:
        if d < radius:
            p = clamp((radius - d) / 60)
            bob = 3 * math.sin(t * 6 + rr * 10)
            person(c, x, y + bob, 11, CREAM if rr > 0.12 else GOLD, p * 0.85)
    p3 = eo(prog(t, wt("frenzy", "30,000") - 0.1, 0.35))
    if p3 > 0:
        c.drawRoundRect(skia.Rect(CX - 300, 1080, CX + 300, 1172), 46, 46, P(C(INK, 0.85 * p3)))
        text(c, "≈ 30,000 INVESTORS", CX, 1150, BEBAS, 76, GOLD2, p3, spacing=3)

def newspaper(c, x, y, s, ang, a):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    r = skia.Rect(-330, -240, 330, 240)
    c.drawRect(r, P(C((232, 224, 204), a)))
    text(c, "EXTRA!", 0, -160, PLAY, 92, INK, a)
    rule(c, -300, 300, -138, INK, a, 4); rule(c, -300, 300, -128, INK, a, 1.5)
    text(c, "CAN PONZI REALLY PAY?", 0, -62, ANTON, 60, INK, a)
    text(c, "EXPERTS QUESTION THE MATH", 0, -14, BEBAS, 36, (90, 80, 60), a, spacing=3)
    for col in range(3):
        x0 = -300 + col * 205
        for ln in range(8):
            ww = 180 if ln % 4 != 3 else 110
            c.drawRect(skia.Rect(x0, 20 + ln * 25, x0 + ww, 30 + ln * 25), P(C((150, 140, 120), a)))
    c.restore()

def sc_math(c, t, D):
    p0 = prog(t, 0.0, 0.9)
    tn = wt("math", "need")
    up = eio(prog(t, tn - 0.5, 0.6))
    ang = lerp(540, -4, eo(p0)); s = lerp(0.1, 1.0, eo(p0))
    y = lerp(780, 450, up); s *= lerp(1.0, 0.42, up); ang = lerp(ang, -2, up)
    shadowed(c, lambda: newspaper(c, CX, y, s, ang, clamp(p0 * 3)))
    if up > 0:
        base = 1080; Hmax = 360
        g = eio(prog(t, wt("math", "160") - 0.1, 1.0))
        bw = 200
        c.drawLine(110, base, 970, base, P(C(CREAM, 0.35 * up), stroke=3))
        c.drawRoundRect(skia.Rect(340 - bw / 2, base - Hmax * g, 340 + bw / 2, base), 10, 10, P(C(GOLD, up)))
        text(c, "160,000,000", 340, base - Hmax * g - 24, ANTON, 72, GOLD2, eo(prog(t, wt("math", "160"), 0.4)))
        text(c, "COUPONS NEEDED", 340, base + 62, BEBAS, 52, CREAM, up, spacing=3)
        p27 = eo(prog(t, wt("math", "27,000") - 0.1, 0.35))
        c.drawRect(skia.Rect(740 - bw / 2, base - 3 * p27, 740 + bw / 2, base), P(C(RED, p27)))
        text(c, "27,000", 740, base - 30, ANTON, 72, RED, p27)
        text(c, "IN CIRCULATION", 740, base + 62, BEBAS, 52, CREAM, p27, spacing=3)
        # magnifier pointing at the tiny bar
        if p27 > 0:
            c.drawCircle(740, base - 130, 46, P(C(RED, p27 * 0.9), stroke=7))
            c.drawLine(772, base - 98, 805, base - 65, P(C(RED, p27 * 0.9), stroke=10))
        pi = eo(prog(t, wt("math", "circulation.") + 0.2, 0.4))
        if pi > 0:
            stamp(c, CX, 1190, "IMPOSSIBLE", RED, 64, -4, pi, sc=lerp(1.5, 1, eo(pi)))

def sc_collapse(c, t, D):
    tr = wt("collapse", "rushed")
    pulse = 0.18 + 0.14 * math.sin(t * 9)
    a = eo(prog(t, 0, 0.2))
    shake = 8 * math.sin(t * 40) * (1 - prog(t, 0, 0.8))
    text(c, "PANIC", CX + shake, 455, ANTON, 170, RED, a, glow=26)
    pyramid(c, t + 10, [0, 0, 0, 0, 0], fall_t=tr + 10 - 0.2, yoff=150)
    ta = wt("collapse", "arrested.") - 0.1
    pa = prog(t, ta, 0.2)
    if pa > 0:
        c.drawRect(skia.Rect(0, 300, W, 1230), P(C(BG, 0.55 * pa)))
        sh = 10 * math.sin(t * 50) * (1 - prog(t, ta + 0.2, 0.4))
        stamp(c, CX + sh, 820, "ARRESTED", RED, 120, -8, pa, sc=lerp(2.2, 1.0, eo(pa)))
        text(c, "AUGUST 12, 1920", CX, 1040, BEBAS, 84, CREAM, eo(prog(t, ta + 0.25, 0.35)), spacing=6)
    vp = skia.Paint(); vp.setShader(skia.GradientShader.MakeRadial(skia.Point(CX, 800), 1100, [C(RED, 0), C(RED, pulse)], [0.5, 1.0]))
    c.drawRect(skia.Rect(0, 0, W, H), vp)

def bank(c, x, y, t, tf, a):
    cols = [-180, -90, 0, 90, 180]
    c.save(); c.translate(x, y)
    fall = max(0.0, t - tf)
    # base
    c.drawRect(skia.Rect(-260, 150, 260, 180), P(C(CREAM, a * 0.9)))
    c.drawRect(skia.Rect(-290, 180, 290, 210), P(C(CREAM, a * 0.8)))
    for i, cx in enumerate(cols):
        R = random.Random(i + 300); d = max(0.0, fall - R.uniform(0, 0.25))
        ang = (R.choice([-1, 1]) * 75) * clamp(d * d * 3.2)
        c.save(); c.translate(cx, 150); c.rotate(ang)
        c.drawRect(skia.Rect(-26, -230, 26, 0), P(C(CREAM, a)))
        for k in (-12, 0, 12): c.drawLine(k, -220, k, -10, P(C(MUTED, a * 0.6), stroke=2))
        c.restore()
    dy = 400 * clamp(fall - 0.25) ** 2 * 6; rot = 14 * clamp(fall - 0.25)
    c.save(); c.translate(0, -80 + dy); c.rotate(rot)
    ped = skia.Path(); ped.moveTo(-290, 0); ped.lineTo(0, -150); ped.lineTo(290, 0); ped.close()
    c.drawRect(skia.Rect(-280, 0, 280, 26), P(C(CREAM, a)))
    c.drawPath(ped, P(C(CREAM, a)));
    text(c, "BANK", 0, -32, ANTON, 64, INK, a)
    c.restore()
    if fall > 0:
        cr = skia.Path(); cr.moveTo(-40, -80); cr.lineTo(-10, -20); cr.lineTo(-50, 40); cr.lineTo(-15, 120)
        c.drawPath(cr, P(C(RED, a * clamp(fall * 4)), stroke=5))
    c.restore()

def sc_damage(c, t, D):
    p = eio(prog(t, 0.05, 1.3))
    shadowed(c, lambda: text(c, "-" + fmt_money(20_000_000 * p), CX, 520, ANTON, 150, RED, eo(prog(t, 0, 0.2)), glow=22 if p >= 1 else 0))
    text(c, "LOST BY INVESTORS", CX, 610, BEBAS, 72, CREAM, eo(prog(t, 0.3, 0.3)), spacing=5)
    bank(c, CX, 900, t, wt("damage", "Banks") - 0.05, eo(prog(t, 0.2, 0.4)))
    pc = eo(prog(t, wt("damage", "collapsed.") - 0.05, 0.3))
    if pc > 0:
        text(c, "BANKS FAILED", CX, 1190, ANTON, 92, RED, pc)

def sc_ending(c, t, D):
    td, tb, tn = wt("ending", "deported"), wt("ending", "Brazil"), wt("ending", "name")
    dim = 1 - eo(prog(t, tn - 0.3, 0.4))
    ax, ay, bx, by, kx, ky = 250, 900, 830, 1010, 540, 560
    if dim > 0:
        pa = eo(prog(t, td - 0.1, 0.4))
        text(c, "DEPORTED", ax, ay - 160, BEBAS, 74, CREAM, pa * dim, spacing=3)
        text(c, "ITALY · 1934", ax, ay - 92, BEBAS, 58, GOLD, pa * dim, spacing=3)
        c.drawCircle(ax, ay, 18 * pa, P(C(GOLD2, dim)))
        c.drawCircle(ax, ay, 36 * pa, P(C(GOLD, 0.4 * dim), stroke=3))
        pr = eio(prog(t, td + 0.3, tb - td))
        n = 40
        for i in range(int(n * pr)):
            u = i / n
            x = (1 - u) ** 2 * ax + 2 * (1 - u) * u * kx + u * u * bx
            y = (1 - u) ** 2 * ay + 2 * (1 - u) * u * ky + u * u * by
            c.drawCircle(x, y, 5, P(C(GOLD, 0.8 * dim)))
        pb = eo(prog(t, tb - 0.1, 0.4))
        c.drawCircle(bx, by, 18 * pb, P(C(RED, dim)))
        c.drawCircle(bx, by, 36 * pb, P(C(RED, 0.4 * dim), stroke=3))
        text(c, "DIED POOR", bx, by + 100, ANTON, 76, RED, pb * dim)
        text(c, "BRAZIL · 1949", bx, by + 160, BEBAS, 58, CREAM, pb * dim, spacing=3)
    pn = eo(prog(t, tn - 0.2, 0.4))
    if pn > 0:
        text(c, "BUT HIS NAME", CX, 700, BEBAS, 100, CREAM, pn, spacing=8)
        s = lerp(1.3, 1.0, eo(prog(t, wt("ending", "never") - 0.1, 0.35)))
        c.save(); c.translate(CX, 900); c.scale(s, s)
        text(c, "NEVER DIED.", 0, 0, ANTON, 170, GOLD2, eo(prog(t, wt("ending", "never") - 0.1, 0.3)), glow=30, glow_rgb=GOLD)
        c.restore()

def sc_legacy(c, t, D):
    tp, tf = wt("legacy", "Ponzi"), beat("legacy", 1)
    out = eo(prog(t, tf - 0.3, 0.35))
    if out < 1:
        a = 1 - out
        p1 = eo(prog(t, 0.1, 0.4))
        text(c, "TODAY, EVERY SCAM THAT PAYS", CX, 470, BEBAS, 64, CREAM, a * p1, spacing=3)
        text(c, "OLD INVESTORS WITH NEW MONEY", CX, 545, BEBAS, 64, CREAM, a * eo(prog(t, wt("legacy", "old") - 0.1, 0.4)), spacing=3)
        text(c, "HAS ONE NAME:", CX, 625, BEBAS, 64, MUTED, a * eo(prog(t, wt("legacy", "one") - 0.1, 0.3)), spacing=3)
        pp = prog(t, tp - 0.15, 0.28)
        if pp > 0:
            s = lerp(1.9, 1.0, eo(pp))
            c.save(); c.translate(CX, 905); c.scale(s, s)
            shadowed(c, lambda: text(c, "PONZI", 0, 0, ANTON, 270, GOLD2, a * clamp(pp * 2), glow=34, glow_rgb=GOLD))
            c.restore()
        ps = prog(t, tp + 0.25, 0.28)
        if ps > 0:
            s = lerp(1.9, 1.0, eo(ps))
            c.save(); c.translate(CX, 1150); c.scale(s, s)
            shadowed(c, lambda: text(c, "SCHEME", 0, 0, ANTON, 230, CREAM, a * clamp(ps * 2)))
            c.restore()
        fl = 1 - prog(t, tp - 0.13, 0.25)
        if 0 < fl < 1: c.drawRect(skia.Rect(0, 0, W, H), P(C(CREAM, 0.35 * fl)))
    if out > 0:
        text(c, "RÉCITALPHA", CX, 720, PLAY, 128, GOLD2, out, spacing=lerp(26, 6, out), glow=20, glow_rgb=GOLD)
        rule(c, CX - 330 * out, CX + 330 * out, 770, GOLD, out, 3)
        text(c, "TRUE STORIES BEHIND MONEY", CX, 850, BEBAS, 62, CREAM, out, spacing=5)
        pf = prog(t, tf + 0.4, 0.4)
        if pf > 0:
            s = back(pf); c.save(); c.translate(CX, 1010); c.scale(s, s)
            c.drawRoundRect(skia.Rect(-300, -62, 300, 62), 62, 62, P(C(GOLD2, 1)))
            text(c, "FOLLOW  @recitalpha6", 0, 18, POPB, 50, INK, 1)
            c.restore()
            text(c, "NEXT: THE CON MAN WHO SOLD THE EIFFEL TOWER", CX, 1150, BEBAS, 50, MUTED, eo(prog(t, tf + 0.9, 0.5)), spacing=2)

DRAW = dict(hook=sc_hook, arrival=sc_arrival, failure=sc_failure, coupon=sc_coupon, promise=sc_promise, trick=sc_trick,
            frenzy=sc_frenzy, math=sc_math, collapse=sc_collapse, damage=sc_damage, ending=sc_ending, legacy=sc_legacy)

def scene_at(t):
    for s in SCENES:
        if t < s["end"]: return s
    return SCENES[-1]

def frame(c, fi):
    t = fi / FPS
    sc = scene_at(t)
    lt, D = t - sc["start"], sc["end"] - sc["start"]
    if sc is SCENES[0]: lt = t - 0.0; D = sc["end"]
    if sc is not SCENES[0]: lt = t - sc["start"]
    background(c, t, sc["id"])
    if not FX:
        fade_out = 1 - prog(lt, D - 0.16, 0.16) if sc is not SCENES[-1] else 1.0
        fade_in = prog(lt, 0, 0.12)
        layer_alpha(c, min(fade_in, fade_out) if sc is not SCENES[0] else fade_out)
        z = 1.0 + 0.035 * eio(prog(lt, 0, D))
        c.save(); c.translate(CX, 780); c.scale(z, z); c.translate(-CX, -780)
        DRAW[sc["id"]](c, lt, D)
        c.restore(); c.restore()
    else:
        fx_background(c, t, sc["id"], lt)
        TR = 0.2
        po = prog(lt, D - TR, TR) if sc is not SCENES[-1] else 0.0
        pi = (1 - prog(lt, 0, TR)) if sc is not SCENES[0] else 0.0
        dx = -W * 0.42 * eio(po) + W * 0.42 * eio(pi)
        blur = 46 * max(po, pi)
        k = hit_k(t)
        z = (1.0 + 0.04 * eio(prog(lt, 0, D))) * (1.0 + 0.075 * k)
        sx = 16 * k * math.sin(t * 95.0); sy = 12 * k * math.cos(t * 81.0)
        lay = skia.Paint()
        if blur > 0.5: lay.setImageFilter(skia.ImageFilters.Blur(blur, 2.0))
        lay.setAlphaf(1.0 - 0.35 * max(po, pi))
        c.saveLayer(None, lay)
        c.save(); c.translate(dx + sx, sy); c.translate(CX, 780); c.scale(z, z); c.translate(-CX, -780)
        DRAW[sc["id"]](c, lt, D)
        c.restore(); c.restore()
        if k > 0.55:
            fp = skia.Paint(Color=C((255, 245, 225), 0.33 * (k - 0.55) / 0.45)); fp.setBlendMode(skia.BlendMode.kScreen)
            c.drawRect(skia.Rect(0, 0, W, H), fp)
        if max(po, pi) > 0:
            q = max(po, pi)
            sp = skia.Paint(); sp.setBlendMode(skia.BlendMode.kScreen)
            x0 = W * (1 - q) if po > 0 else W * q
            sp.setShader(skia.GradientShader.MakeLinear([skia.Point(x0 - 260, 0), skia.Point(x0 + 260, 0)],
                         [C(GOLD2, 0), C(GOLD2, 0.30 * math.sin(math.pi * q)), C(GOLD2, 0)], [0, 0.5, 1]))
            c.drawRect(skia.Rect(0, 0, W, H), sp)
    brand(c, t, sc["id"])
    if not CLEAN: captions(c, t)
    overlays(c, fi)

def main():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    n = int(math.ceil(TOTAL * FPS))
    if PREVIEW:
        for fi in PREVIEW:
            frame(c, fi); surf.makeImageSnapshot().save(f"{ROOT}/prev_{fi:05d}.png", skia.kPNG)
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", f"{ROOT}/video_only.mp4" if not CLEAN else f"{ROOT}/video_only_clean.mp4"],
                          stdin=subprocess.PIPE)
    for fi in range(n):
        frame(c, fi)
        ff.stdin.write(surf.makeImageSnapshot().toarray().tobytes())
        if fi % 300 == 0: print("frame", fi, "/", n, flush=True)
    ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    main()
