import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep27")
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

PH = dict(old=load_photo("sutton_01.jpg"), fbi=load_photo("sutton_02.jpg"))
CR_O = "WILLIE SUTTON, 1972 · BERNARD GOTFRYD / LOC · PUBLIC DOMAIN"
CR_F = "WILLIE SUTTON · PUBLIC DOMAIN"

def quote_card(c, s_, y, a, rgb=CREAM, size=92, cross=0.0):
    sz = size
    while text_w(s_, F(PLAY, sz)) > 940 and sz > 40: sz -= 4
    text(c, s_, CX, y, PLAY, sz, rgb, a)
    if cross > 0:
        w = text_w(s_, F(PLAY, sz)); c.drawLine(CX - w / 2 - 10, y - sz * 0.3, CX - w / 2 - 10 + (w + 20) * cross, y - sz * 0.3, P(C(RED, a), stroke=12))

def sc_hook(c, t, D):
    photo_card(c, PH["fbi"], CX, 830, 470, 620, t / D, 1.0, 1.0, 1.14, focus=(0.5, 0.3), rot=-1.5, credit=CR_F)
    text(c, "AMERICA'S MOST FAMOUS", CX, 360, BEBAS, 72, CREAM, 1.0, spacing=4)
    pop_text(c, "BANK ROBBER", CX, 450, ANTON, 100, GOLD2, max(0.6, prog(t, 0.0, 0.22)), glow=18, glow_rgb=GOLD)
    pn = prog(t, W_("hook", "never") - 0.2, 0.22)
    if pn > 0: stamp(c, CX, 1160, "NEVER SAID IT", RED, 120, -6, pn, sc=lerp(2.2, 1, eo(pn)))

def sc_line(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("line", 1)
    building(c, CX, 1220, 0.6, a * 0.5, "BANK", cols=5)
    quote_card(c, "\"Why do you rob banks?\"", 560, eo(prog(t, 0.0, 0.3)), CREAM, 80)
    pq = prog(t, b1 - 0.1, 0.3)
    if pq > 0: pop_text(c, "\"BECAUSE THAT'S WHERE", CX, 760, ANTON, 92, GOLD2, pq, glow=18, glow_rgb=GOLD)
    pq2 = prog(t, W_("line", "money") - 0.3, 0.3)
    if pq2 > 0: pop_text(c, "THE MONEY IS.\"", CX, 870, ANTON, 112, GOLD2, pq2, glow=18, glow_rgb=GOLD)

def sc_who(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("who", 1)
    pop_text(c, "WILLIE SUTTON", CX, 400, ANTON, 120, CREAM, prog(t, 0.0, 0.25))
    for i in range(6):
        p = eo(prog(t, 0.3 + i * 0.25, 0.3))
        building(c, 150 + i * 156, 760, 0.22, p, "BANK", cols=2)
    k = eo(prog(t, W_("who", "$2") - 0.3, 0.9))
    if k > 0: counter(c, 2000000 * k, CX, 1010, 150, GOLD2, a, prefix="~$", glow=22)
    pill(c, "BY HIS OWN ESTIMATE", 1190, eo(prog(t, W_("who", "estimate.") - 0.4, 0.3)), CREAM, 56, 640)

def sc_actor(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("actor", 1)
    pop_text(c, "\"WILLIE THE ACTOR\"", CX, 400, ANTON, 112, GOLD2, prog(t, W_("actor", "Willie") - 0.2, 0.25), glow=18, glow_rgb=GOLD)
    roles = [("policeman,", "POLICEMAN", (40, 60, 110)), ("messenger,", "MESSENGER", (120, 90, 50)), ("cleaner.", "WINDOW CLEANER", (60, 100, 90))]
    for i, (w, lab, rgb) in enumerate(roles):
        p = eo(prog(t, W_("actor", w) - 0.4, 0.3))
        id_card(c, CX + (i - 1) * 40, 650 + i * 190, 0.8, (-4, 3, -2)[i], p, lab, "DISGUISE #" + str(i + 1), tag_="FAKE", rgb=(232, 222, 200))

def sc_escape(c, t, D):
    a = eo(prog(t, 0, 0.3))
    k = clamp(t / max(0.5, D - 0.3))
    bars(c, a * (1 - 0.6 * k), y0=330, y1=1240)
    for i in range(3):
        p = prog(t, 0.4 + i * 0.6, 0.22)
        if p > 0: stamp(c, CX, 560 + i * 230, "ESCAPED", RED if i % 2 == 0 else GOLD2, 130, (-6, 5, -4)[i], p, sc=lerp(2.2, 1, eo(p)))

def sc_denial(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("denial", 1)
    book(c, CX, 720, 0.9, a, t, title="MEMOIR")
    text(c, "\"WHERE THE MONEY WAS\"", CX, 990, BEBAS, 64, GOLD2, a, spacing=4)
    pop_text(c, "HIS 1976 AUTOBIOGRAPHY", CX, 390, ANTON, 92, CREAM, prog(t, 0.0, 0.25))
    pq = prog(t, W_("denial", "never") - 0.3, 0.22)
    if pq > 0: stamp(c, CX, 1130, "\"I NEVER SAID IT.\"", RED, 104, -5, pq * (1 - eo(prog(t, b1 - 0.3, 0.3))), sc=lerp(2.2, 1, eo(pq)))
    if t > b1 - 0.3:
        pill(c, "\"SOME ENTERPRISING REPORTER\"", 1170, eo(prog(t, W_("denial", "enterprising") - 0.3, 0.3)), GOLD2, 56, 900)

def sc_ad(c, t, D):
    a = eo(prog(t, 0, 0.3))
    # retro TV
    c.drawRoundRect(skia.Rect(CX - 380, 520, CX + 380, 1060), 40, 40, P(C((70, 52, 36), a)))
    c.drawRoundRect(skia.Rect(CX - 340, 560, CX + 200, 1020), 60, 60, P(C((24, 26, 28), a)))
    for i in range(2): c.drawCircle(CX + 290, 680 + i * 140, 36, P(C(GOLD, a)))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(CX - 340, 560, CX + 200, 1020), 60, 60), doAntiAlias=True)
    photo_card(c, PH["old"], CX - 70, 790, 400, 440, t / D, a, 1.0, 1.1, focus=(0.5, 0.35))
    c.restore()
    pop_text(c, "1970: A BANK'S TV AD", CX, 400, ANTON, 104, GOLD2, prog(t, 0.0, 0.25), glow=18, glow_rgb=GOLD)
    text(c, CR_O, W - 60, 1110, BEBAS, 30, MUTED, a * 0.9, align="r", spacing=2)
    pw = prog(t, W_("ad", "commercial.") - 0.3, 0.22)
    if pw > 0: stamp(c, CX, 1200, "STARRING WILLIE SUTTON", RED, 80, -4, pw, sc=lerp(2.2, 1, eo(pw)))

def sc_loopend(c, t, D):
    photo_card(c, PH["fbi"], CX, 780, 500, 680, t / D, 1.0, 1.0, 1.1, focus=(0.5, 0.3), rot=-1.5, credit=CR_F, dim=0.3)
    pop_text(c, "SO REMEMBER:", CX, 400, ANTON, 120, GOLD2, prog(t, 0.0, 0.22), s0=1.3, glow=20, glow_rgb=GOLD)

E.DRAW = dict(hook=sc_hook, line=sc_line, who=sc_who, actor=sc_actor, escape=sc_escape, denial=sc_denial, ad=sc_ad,
              loopend=sc_loopend, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"escape"}
_IMP = [("hook", "never", -0.2, 0.4), ("line", "money", -0.3, 0.35), ("who", "$2", -0.2, 0.3),
        ("actor", "Actor.", -0.2, 0.3), ("escape", "again,", -0.2, 0.3), ("rehook", "line?", -0.2, 0.35),
        ("denial", "never", -0.3, 0.45), ("ad", "commercial.", -0.3, 0.35), ("loopend", "So", -0.05, 0.3)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("who", "$2", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
