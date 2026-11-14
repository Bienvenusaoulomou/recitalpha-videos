import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep45")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
from kit3 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999
def B(sid, i):
    try: return beat(sid, i)
    except Exception: return 999
from kit4 import *
import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0
def name_chip(c, x, y, label, a, rgb=CREAM, size=36):
    if a <= 0: return
    f = F(BEBAS, size); w = f.measureText(label) + 30
    c.drawRoundRect(skia.Rect(x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.35), 10, 10, P(C((20, 18, 14), a * 0.85)))
    text(c, label, x, y, BEBAS, size, rgb, a, spacing=1)

AFR = [(-0.30, -0.95), (0.05, -1.0), (0.30, -0.88), (0.42, -0.62), (0.70, -0.40), (0.95, -0.38), (0.62, 0.05), (0.50, 0.30),
       (0.30, 0.62), (0.12, 0.98), (-0.05, 0.95), (-0.15, 0.55), (-0.22, 0.20), (-0.30, -0.05), (-0.62, -0.10), (-0.92, -0.30),
       (-0.95, -0.55), (-0.70, -0.85)]
def africa(c, x, y, r, a, rgb=(70, 64, 50), ol=GOLD2):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x + AFR[0][0] * r, y + AFR[0][1] * r)
    for px, py in AFR[1:]: p.lineTo(x + px * r, y + py * r)
    p.close(); c.drawPath(p, P(C(rgb, a))); c.drawPath(p, P(C(ol, a), stroke=6))

KE_RED, KE_GREEN = (190, 40, 40), (30, 120, 60)
def browser(c, cx, cy, w, h, a, url="president.go.ke", hacked=0.0, t=0):
    """browser window; hacked 0..1 swaps the official page for a black ransom page; returns inner rect"""
    if a <= 0: return None
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    c.drawRoundRect(r, 18, 18, P(C((40, 42, 50), a)))
    c.drawRoundRect(skia.Rect(r.left() + 120, r.top() + 14, r.right() - 20, r.top() + 58), 20, 20, P(C((230, 230, 226), a)))
    text(c, url, r.left() + 145, r.top() + 48, BEBAS, 36, INK, a, align="l", spacing=1)
    for i, col in enumerate([(230, 80, 70), (230, 190, 60), (90, 190, 90)]): c.drawCircle(r.left() + 30 + i * 30, r.top() + 36, 9, P(C(col, a)))
    inner = skia.Rect(r.left() + 14, r.top() + 72, r.right() - 14, r.bottom() - 14)
    c.save(); c.clipRect(inner)
    if hacked < 1:
        aa = a * (1 - hacked)
        c.drawRect(inner, P(C((236, 232, 222), aa)))
        band = (inner.bottom() - inner.top()) / 3
        c.drawRect(skia.Rect(inner.left(), inner.top(), inner.right(), inner.top() + 70), P(C((20, 20, 20), aa)))
        c.drawRect(skia.Rect(inner.left(), inner.top() + 70, inner.right(), inner.top() + 84), P(C(KE_RED, aa)))
        c.drawRect(skia.Rect(inner.left(), inner.top() + 84, inner.right(), inner.top() + 98), P(C(KE_GREEN, aa)))
        text(c, "STATE HOUSE · KENYA", inner.centerX(), inner.top() + 50, BEBAS, 44, CREAM, aa, spacing=4)
        for i in range(5):
            c.drawRect(skia.Rect(inner.left() + 40, inner.top() + 140 + i * 50, inner.left() + 40 + (inner.width() - 80) * (0.9 if i % 2 else 0.6), inner.top() + 160 + i * 50), P(C((170, 160, 140), aa)))
    if hacked > 0:
        aa = a * hacked
        c.drawRect(inner, P(C((6, 8, 8), aa)))
        rng = random.Random(int(t * 10))
        for i in range(4):
            yy = rng.uniform(inner.top(), inner.bottom())
            c.drawRect(skia.Rect(inner.left(), yy, inner.right(), yy + rng.uniform(3, 10)), P(C(RED, aa * 0.3)))
    c.restore()
    return inner

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    inner = browser(c, CX, 800, 880, 640, 1.0, hacked=1.0, t=t)
    pop_text(c, "THE PRESIDENT'S WEBSITE", CX, 420, ANTON, 84, CREAM, 1.0)
    text(c, "HACKED", inner.centerX(), inner.top() + 150, ANTON, 120, RED, 1.0, glow=18, glow_rgb=RED)
    if t > b1 - 0.2:
        for i in range(5):
            p = eo(prog(t, b1 - 0.2 + i * 0.15, 0.3))
            crypto_coin(c, inner.left() + 140 + i * 150, inner.top() + 330, 58 * p if p > 0 else 1, p, t + i)
        p = eo(prog(t, b1, 0.3))
        text(c, "5 BITCOINS", inner.centerX(), inner.bottom() - 40, ANTON, 90, GOLD2, p, glow=16, glow_rgb=GOLD)
    CH.HACKER.draw(c, 900, 1260, 0.55, -1, a=1.0, arm_f=(-60 + 8 * math.sin(t * 10), -60))

def sc_price(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("price", 1)
    for i in range(5): crypto_coin(c, 180 + i * 180, 500, 70, a, t + i)
    text(c, "5 BTC =", CX, 680, BEBAS, 80, CREAM, a, spacing=4)
    counter(c, int(41e6 * eo(prog(t, 0.1, 1.2))), CX, 820, 120, GOLD2, a, prefix="~KSh ", glow=20)
    text(c, "SHILLINGS", CX, 890, BEBAS, 54, CREAM, a, spacing=6)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        counter(c, int(320000 * eo(prog(t, b1 - 0.2, 1.0))), CX, 1030, 110, CREAM, p, prefix="~$")
        for i in range(6): bills(c, 140 + i * 160, 1150 + 12 * math.sin(t * 2 + i), p, n=2, rot=8 * math.sin(t * 2 + i))

def sc_message(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("message", 1)
    calendar(c, 200, 520, 0.6, a, "18", "JUL 2026")
    pop_text(c, "THE HOMEPAGE", CX + 120, 470, ANTON, 96, CREAM, prog(t, 0.1, 0.25))
    inner = browser(c, CX, 930, 860, 560, a, hacked=1.0 if t > b1 - 0.3 else clamp((t - 0.8) / 0.3), t=t)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        text(c, "TO PRESIDENT RUTO:", inner.centerX(), inner.top() + 90, ANTON, 64, CREAM, p)
        for i in range(3):
            c.drawRect(skia.Rect(inner.left() + 70, inner.top() + 140 + i * 44, inner.right() - 70 - (i % 2) * 120, inner.top() + 156 + i * 44), P(C((120, 120, 120), p)))
        pw = eo(prog(t, W_("message", "wallet") - 0.3, 0.3))
        if pw > 0:
            c.drawRoundRect(skia.Rect(inner.left() + 60, inner.bottom() - 120, inner.right() - 60, inner.bottom() - 40), 12, 12, P(C(GOLD2, pw)))
            text(c, "BTC WALLET: bc1q · · · · · · · ·", inner.centerX(), inner.bottom() - 66, BEBAS, 44, INK, pw, spacing=2)

def sc_deadline(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("deadline", 1); b2 = B("deadline", 2)
    clock(c, 280, 700, 160, a, t_h=lerp(15.0, 17.9, eo(prog(t, 0, 2.0))), label="6 PM")
    pop_text(c, "DEADLINE: 6 PM", CX, 430, ANTON, 100, RED, prog(t, 0, 0.25), glow=16, glow_rgb=RED)
    lines = ["\"DO A PAYMENT OF", "5 BITCOINS... IF YOU", "WANT PEACE BEFORE", "6 O'CLOCK THIS EVENING\""]
    for i, ln in enumerate(lines):
        text(c, ln, 730, 600 + i * 62, BEBAS, 50, CREAM, eo(prog(t, 0.4 + i * 0.35, 0.3)))
    name_chip(c, 730, 880, "HACKERS' MESSAGE, QUOTED BY ITWEB AFRICA", a * 0.9, rgb=GOLD2, size=28)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 990, 880, 100, p, "\"...BEFORE WE LEAK EVERYTHING ABOUT YOU\"", rgb=(70, 34, 30), size=44)
    if t > b2 - 0.3:
        p = eo(prog(t, b2 - 0.3, 0.3))
        box(c, CX, 1100, 880, 100, p, "\"THIS MESSAGE IS THE THIRD TIME FOR YOU\"", rgb=(70, 34, 30), size=44)
        ps = prog(t, W_("deadline", "third") - 0.1, 0.22)
        if ps > 0: stamp(c, CX, 1220, "3RD WARNING", RED, 76, -5, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_before(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("before", 1)
    calendar(c, 200, 520, 0.6, a, "NOV", "2025")
    pop_text(c, "MANY SITES AT ONCE", CX + 120, 470, ANTON, 84, CREAM, prog(t, 0.1, 0.25))
    labs = ["INTERIOR", "HEALTH", "EDUCATION", "LABOUR", "MINISTRY", "STATE HOUSE"]
    for i, lab in enumerate(labs):
        x = 220 + (i % 3) * 320; y = 720 + (i // 3) * 330
        hk = clamp((t - 0.6 - i * 0.25) / 0.2)
        last = i == 5
        if last and t < b1 - 0.3: hk = 0
        inner = browser(c, x, y, 290, 250, a, url=".go.ke", hacked=hk, t=t)
        text(c, lab, x, y + 20, BEBAS, 42, RED if hk > 0.5 else INK, a, spacing=2)
        if last and hk > 0: stamp(c, x, y + 90, "HIT", RED, 60, -8, hk, sc=lerp(2, 1, eo(hk)))

def sc_confirm(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("confirm", 1)
    pop_text(c, "STATE HOUSE CONFIRMED", CX, 430, ANTON, 90, CREAM, prog(t, 0, 0.25))
    ps = prog(t, 0.5, 0.22)
    inner = browser(c, CX, 790, 820, 460, a, hacked=1.0 if t < b1 - 0.2 else 0.0, t=t)
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        c.drawRect(inner, P(C((20, 22, 26), a)))
        text(c, "WE'LL BE BACK SOON", inner.centerX(), inner.centerY() + 20, ANTON, 72, CREAM, p)
        for i in range(3):
            shield(c, 260 + i * 280, 1150, 0.4, p * eo(prog(t, b1 + i * 0.3, 0.3)), label="CYBER", rgb=(60, 120, 90))
    if ps > 0: stamp(c, CX + 150, 620, "BREACH", RED, 90, -6, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_minister(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("minister", 1); b2 = B("minister", 2)
    CH.OFFICIAL.draw(c, 250, 1250, 0.95, 1, a=a, blink=bl(t), arm_f=(-40, -50))
    name_chip(c, CX, 420, "ICT MINISTER WILLIAM KABOGO (STYLISED)", a, rgb=GOLD2, size=36)
    if t < b1 - 0.2:
        q = ["\"OUR CYBER TEAM", "IS ON TOP OF", "THE SITUATION\""]
        for i, ln in enumerate(q):
            text(c, ln, 680, 560 + i * 90, ANTON, 80, GOLD2 if i == 2 else CREAM, eo(prog(t, 0.6 + i * 0.4, 0.3)))
        name_chip(c, 680, 860, "QUOTED BY ANADOLU AGENCY", a * 0.9, rgb=GOLD2, size=30)
    else:
        lines = ["\"NO EVIDENCE OF", "UNAUTHORIZED ACCESS", "TO SENSITIVE DATA, DATA", "EXFILTRATION, OR LOSS", "OF INFORMATION\""]
        for i, ln in enumerate(lines):
            text(c, ln, 680, 520 + i * 66, ANTON, 58, CREAM if i < 4 else GOLD2, eo(prog(t, b1 - 0.2 + i * 0.3, 0.3)))
    if t > b2 - 0.3:
        p = eo(prog(t, b2 - 0.3, 0.3))
        browser(c, 700, 1000, 480, 260, p, hacked=0.0, t=t)
        box(c, 700, 1180, 420, 80, p, "BACK ONLINE", rgb=(30, 90, 60), size=56)

def sc_nobody(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("nobody", 1)
    CH.HACKER.draw(c, CX, 1080, 0.75, 1, a=a * 0.85)
    text(c, "?", CX, 610, ANTON, 220, GOLD2, a * (0.7 + 0.3 * math.sin(t * 5)))
    pop_text(c, "WHO DID IT?", CX, 430, ANTON, 110, CREAM, prog(t, 0, 0.25))
    ps = prog(t, 0.7, 0.22)
    if ps > 0: stamp(c, CX, 1060, "NO CLAIM", RED, 96, -5, ps, sc=lerp(2.2, 1, eo(ps)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1185, 820, 100, p, "PAID? NO PUBLIC REPORT", rgb=(40, 46, 60), size=56)

def sc_billions(c, t, D):
    a = eo(prog(t, 0, 0.3))
    africa(c, 270, 800, 230, a)
    pin(c, 400, 790, 0.6, a, rgb=GOLD2)
    text(c, "KENYA", 470, 760, BEBAS, 50, GOLD2, a, align="l", spacing=3)
    pop_text(c, "BILLIONS", 760, 640, ANTON, 120, RED, prog(t, 0.3, 0.25), glow=18, glow_rgb=RED)
    text(c, "OF ATTEMPTED ATTACKS", 760, 720, BEBAS, 50, CREAM, a, spacing=3)
    rng = random.Random(5)
    for i in range(26):
        f = (t * 0.8 + i / 26) % 1.0
        sx, sy = rng.uniform(80, 1000), rng.uniform(380, 520)
        x = lerp(sx, 400, f); y = lerp(sy if i % 2 else 1250, 790, f)
        c.drawCircle(x, y, 9, P(C(RED, a * (1 - f))))
    shield(c, 400, 1080, 0.7, a, label="GOV", rgb=(60, 120, 90))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    browser(c, CX, 960, 700, 400, a, hacked=1.0, t=t)
    for i in range(5): crypto_coin(c, 300 + i * 120, 990, 50, a, t + i)
    pop_text(c, "SHOULD A GOVERNMENT", CX, 430, ANTON, 90, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "EVER PAY HACKERS?", CX, 540, ANTON, 96, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 680)

E.DRAW = dict(hook=sc_hook, price=sc_price, message=sc_message, deadline=sc_deadline, before=sc_before, confirm=sc_confirm, minister=sc_minister,
              nobody=sc_nobody, billions=sc_billions, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"deadline"}
_IMP = [("hook", "5", -0.2, 0.4), ("price", "$320000", -0.2, 0.35), ("deadline", "third", -0.2, 0.45), ("rehook", "close.", -0.2, 0.4),
        ("before", "presidency's", -0.2, 0.4), ("confirm", "confirmed", -0.2, 0.35), ("nobody", "claimed", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "5", 0.0), ("price", "41", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
