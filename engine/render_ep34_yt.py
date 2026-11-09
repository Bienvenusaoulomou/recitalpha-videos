import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep34")
sys.path.insert(0, os.environ["REC_ROOT"])
import skia
import engine as E
from props import *
from kit import *
from kit2 import *
from kit3 import *
from kit4 import *
import script as S

E.FX = True
SID = {s["id"] for s in E.SCENES}
def W_(sid, w, nth=0):
    try: return wt(sid, w, nth)
    except KeyError: return 999
def B(sid, i):
    try: return beat(sid, i)
    except Exception: return 999
import chars as CH

def bl(t, per=3.1): return 1.0 if (t % per) < 0.12 else 0.0

def ch_fn(ch, t, talk=0.0, face=1):
    def f(c, x, y, s, al):
        ch.draw(c, x, y, s, face, a=al, blink=bl(t + x * 0.01), mouth=talk * (0.5 + 0.5 * math.sin(t * 15 + x)), arm_f=(10, -20))
    return f

def call_grid(c, cx, cy, w, h, a, t, glitch=0.0, fake=False, talk=0.0, labels=("CFO", "COLLEAGUE", "COLLEAGUE", "YOU")):
    inner = screen(c, cx, cy, w, h, a)
    gw, gh = inner.width() / 2, inner.height() / 2
    chars = [CH.CFO, CH.COLLEAGUE, CH.RECRUITER, CH.CLERK]
    for i in range(4):
        r = skia.Rect(inner.left() + (i % 2) * gw + 6, inner.top() + (i // 2) * gh + 6, inner.left() + (i % 2 + 1) * gw - 6, inner.top() + (i // 2 + 1) * gh - 6)
        me = i == 3
        tile(c, r, a, ch_fn(chars[i], t, 0 if me else (talk if i == 0 else talk * 0.3)), labels[i], glitch=0 if me else glitch, t=t, fake=fake and not me)
    return inner

def opera(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-330, -40, 330, 0), P(C((150, 136, 110), a)))
    for i, (ox, hgt, wd) in enumerate([(-220, 230, 170), (-90, 300, 200), (60, 260, 180), (190, 190, 150)]):
        p = skia.Path(); p.moveTo(ox - wd / 2, -40); p.quadTo(ox - wd * 0.1, -hgt * 1.3, ox + wd / 2, -40); p.close()
        c.drawPath(p, P(C((240, 236, 226), a))); c.drawPath(p, P(C(INK, a), stroke=5))
        c.drawLine(ox - wd * 0.1, -hgt * 0.62, ox + wd * 0.2, -40, P(C((190, 186, 176), a), stroke=3))
    c.restore()

def email(c, x, y, s, a, frm="FROM: UK OFFICE"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect(-260, -170, 260, 170), 20, 20)
    c.drawRRect(r, P(C((236, 230, 214), a)))
    v = skia.Path(); v.moveTo(-260, -170); v.lineTo(0, 30); v.lineTo(260, -170)
    c.drawPath(v, P(C(INK, a * 0.6), stroke=6))
    c.drawRRect(r, P(C(INK, a), stroke=6))
    text(c, frm, 0, 130, BEBAS, 48, INK, a, spacing=3)
    c.restore()

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    call_grid(c, CX, 950, 800, 480, 1.0, t, talk=1.0 if t > b1 else 0.0)
    counter(c, 25000000, CX, 470, 140 * lerp(1.12, 1.0, eo(prog(t, 0, 0.5))), GOLD2, 1.0, glow=24)
    text(c, "SENT TO CRIMINALS", CX, 550, BEBAS, 64, CREAM, 1.0, spacing=6)
    pv = prog(t, W_("hook", "video") - 0.3, 0.22)
    if pv > 0: stamp(c, CX, 650, "ON A VIDEO CALL", RED, 70, -4, pv, sc=lerp(2.2, 1, eo(pv)))

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("who", 1)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pop_text(c, "ARUP", CX, 450, ANTON, 150, GOLD2, prog(t, W_("who", "Arup,") - 0.2, 0.25) * o1, glow=22, glow_rgb=GOLD)
        pill(c, "BRITISH ENGINEERING FIRM", 580, eo(prog(t, W_("who", "British") - 0.2, 0.3)) * o1, CREAM, 56, 700)
        po = eo(prog(t, W_("who", "Sydney") - 0.3, 0.4))
        opera(c, CX, 1120, 1.2, po * o1)
        text(c, "WORKED ON THE SYDNEY OPERA HOUSE", CX, 1200, BEBAS, 50, CREAM, po * o1, spacing=3)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        building(c, 780, 1130, 0.45, p, "HONG KONG", cols=4)
        CH.CLERK.draw(c, 280, 1230, 1.0, 1, a=p, blink=bl(t))
        pop_text(c, "HONG KONG OFFICE", CX, 450, ANTON, 104, CREAM, p)

def sc_message(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("message", 1)
    CH.CLERK.draw(c, 260, 1230, 1.0, 1, a=a, blink=bl(t), brow=0.6 if t > b1 else 0.0, arm_f=(-60, -60) if t > b1 else (10, -20), look=(1, -0.5))
    k = eo(prog(t, 0.1, 0.5))
    email(c, lerp(1200, 720, k), 760, 0.8, a, "FROM: UK OFFICE")
    pop_text(c, "A MESSAGE", CX, 450, ANTON, 110, CREAM, prog(t, 0, 0.25))
    ps = prog(t, W_("message", "scam.") - 0.4, 0.22)
    if ps > 0:
        stamp(c, 720, 1050, "SUSPICIOUS", RED, 90, -6, ps, sc=lerp(2.2, 1, eo(ps)))
        text(c, "?", 420, 560, ANTON, 160, GOLD2, ps)

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("call", 1)
    call_grid(c, CX, 820, 820, 480, a, t, talk=1.0)
    pop_text(c, "THE VIDEO CALL", CX, 440, ANTON, 104, CREAM, prog(t, 0, 0.25))
    for i, (w, lab, x) in enumerate([("looked", "LOOKED REAL", 300), ("sounded", "SOUNDED REAL", 780)]):
        p = prog(t, W_("call", w) - 0.3, 0.22)
        if p > 0: stamp(c, x, 1190, lab, (90, 220, 140), 58, -4, p, sc=lerp(2, 1, eo(p)))

def sc_transfers(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("transfers", 1)
    n = int(clamp(prog(t, 0.2, max(0.5, b1 - 0.4))) * 15)
    pop_text(c, "TRANSFERS", CX, 440, ANTON, 100, CREAM, prog(t, 0, 0.25))
    text(c, str(max(1, n)), CX, 640, ANTON, 170, GOLD2, a, glow=22, glow_rgb=GOLD)
    for i in range(15):
        on = i < n
        c.drawRoundRect(skia.Rect(120 + (i % 5) * 172, 720 + (i // 5) * 70, 260 + (i % 5) * 172, 770 + (i // 5) * 70), 10, 10, P(C(GOLD2 if on else (60, 56, 48), a)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        k = eo(prog(t, b1, 1.0))
        counter(c, 200000000 * k, CX, 1050, 110, GOLD2, p, prefix="HK$", glow=18)
        pu = prog(t, W_("transfers", "US$25.6") - 0.3, 0.22)
        if pu > 0: stamp(c, CX, 1185, "~US$25.6 MILLION", RED, 72, -4, pu, sc=lerp(2, 1, eo(pu)))

def sc_confirm(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("confirm", 1)
    pill(c, "ARUP CONFIRMED:", 440, a, GOLD2, 66, 560)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        call_grid(c, CX, 900, 760, 500, a * o1, t, glitch=1.0, fake=True, labels=("FAKE", "FAKE", "FAKE", "YOU"))
        pf = prog(t, W_("confirm", "fake") - 0.3, 0.22)
        if pf > 0: stamp(c, CX, 600, "FAKE VOICES & IMAGES", RED, 84, -4, pf * o1, sc=lerp(2.2, 1, eo(pf)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        shield(c, CX, 780, 0.85, p, None)
        pop_text(c, "FINANCES: NOT AFFECTED", CX, 1080, ANTON, 72, CREAM, prog(t, W_("confirm", "finances") - 0.2, 0.25))
        pop_text(c, "SYSTEMS: NOT COMPROMISED", CX, 1190, ANTON, 72, CREAM, prog(t, W_("confirm", "internal") - 0.3, 0.25))

def sc_police(c, t, D):
    a = eo(prog(t, 0, 0.3))
    building(c, 360, 1180, 0.5, a, "HONG KONG POLICE", cols=4)
    calendar(c, 820, 900, 0.6, eo(prog(t, W_("police", "January") - 0.3, 0.3)), "2024", "JANUARY")
    pop_text(c, "REPORTED", CX, 450, ANTON, 120, GOLD2, prog(t, W_("police", "reported") - 0.2, 0.25), glow=18, glow_rgb=GOLD)

def sc_twist(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("twist", 1)
    pop_text(c, "THE TWIST", CX, 440, ANTON, 110, GOLD2, prog(t, 0, 0.25), glow=18, glow_rgb=GOLD)
    laptop(c, CX, 960, 1.0, a, t, label="NO HACK")
    pn = prog(t, W_("twist", "computer.") - 0.4, 0.22)
    if pn > 0: stamp(c, CX, 620, "NO COMPUTER HACKED", CREAM, 80, -4, pn * (1 - eo(prog(t, b1 - 0.2, 0.2))), sc=lerp(2, 1, eo(pn)))
    pt = prog(t, W_("twist", "trust.") - 0.4, 0.22)
    if pt > 0: stamp(c, CX, 620, "THEY HACKED TRUST", RED, 100, -5, pt, sc=lerp(2.2, 1, eo(pt)))

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("quote", 1)
    pill(c, "ROB GREIG · ARUP TECH CHIEF", 440, a, CREAM, 56, 720)
    o1 = 1 - eo(prog(t, b1 - 0.3, 0.3))
    if o1 > 0:
        pop_text(c, "“AN INDUSTRY,", CX, 640, PLAY, 84, GOLD2, prog(t, W_("quote", "industry,") - 0.3, 0.25) * o1)
        pop_text(c, "BUSINESS AND", CX, 760, PLAY, 84, GOLD2, prog(t, W_("quote", "business") - 0.3, 0.25) * o1)
        pop_text(c, "SOCIAL ISSUE”", CX, 880, PLAY, 84, GOLD2, prog(t, W_("quote", "social") - 0.3, 0.25) * o1)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3)); k = eo(prog(t, b1, 1.2))
        for i in range(6):
            h = (60 + i * 55) * clamp(k * 1.4 - i * 0.12)
            c.drawRect(skia.Rect(170 + i * 130, 1180 - h, 270 + i * 130, 1180), P(C(RED, p)))
        arrow(c, 180, 1050, 900, 720, k, p, GOLD2, 12)
        pop_text(c, "ATTACKS: RISING SHARPLY", CX, 620, ANTON, 80, CREAM, prog(t, W_("quote", "rising") - 0.3, 0.25))

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    call_grid(c, CX, 940, 760, 480, a, t, glitch=0.5 + 0.5 * math.sin(t * 3), talk=1.0, labels=("BOSS?", "?", "?", "YOU"))
    pop_text(c, "TRUST YOUR BOSS", CX, 430, ANTON, 104, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "ON A VIDEO CALL?", CX, 550, ANTON, 104, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 1240)

E.DRAW = dict(hook=sc_hook, who=sc_who, message=sc_message, call=sc_call, transfers=sc_transfers, confirm=sc_confirm,
              police=sc_police, twist=sc_twist, quote=sc_quote, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK))
E.RED_SCENES = {"confirm"}
_IMP = [("hook", "video", -0.3, 0.45), ("who", "Sydney", -0.3, 0.35), ("message", "scam.", -0.4, 0.4),
        ("call", "sounded", -0.3, 0.35), ("rehook", "deepfakes.", -0.2, 0.45), ("transfers", "US$25.6", -0.3, 0.4),
        ("confirm", "fake", -0.3, 0.4), ("twist", "trust.", -0.4, 0.45), ("quote", "rising", -0.3, 0.35)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("transfers", "HK$200", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
