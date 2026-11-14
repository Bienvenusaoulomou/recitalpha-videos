import os, sys, math, random
os.environ.setdefault("REC_ROOT", "/home/claude/ep44")
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

def ch_fn(ch, t, talk=0.0, face=1, a=1.0):
    def f(c, x, y, s, al):
        ch.draw(c, x, y, s, face, a=al * a, blink=bl(t + x * 0.01), mouth=talk * (0.5 + 0.5 * math.sin(t * 15 + x)), arm_f=(10, -20))
    return f

def mobile(c, x, y, s, a, t=0, title="CHAT"):
    """smartphone with chat app; returns nothing"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-170, -320, 170, 320), 36, 36, P(C((30, 32, 38), a)))
    c.drawRoundRect(skia.Rect(-170, -320, 170, 320), 36, 36, P(C(INK, a), stroke=6))
    c.drawRect(skia.Rect(-150, -290, 150, 290), P(C((18, 24, 34), a)))
    c.drawRect(skia.Rect(-150, -290, 150, -230), P(C((40, 110, 170), a)))
    text(c, title, 0, -248, BEBAS, 38, CREAM, a, spacing=2)
    c.restore()

def bubble(c, x, y, w, label, a, mine=False, size=34):
    if a <= 0: return
    rgb = (60, 140, 90) if mine else (60, 66, 80)
    c.drawRoundRect(skia.Rect(x - w / 2, y - 34, x + w / 2, y + 22), 18, 18, P(C(rgb, a)))
    text(c, label, x, y + 4, BEBAS, size, CREAM, a, spacing=1)

def mute_icon(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 70, P(C(RED, a)))
    c.drawRoundRect(skia.Rect(-16, -40, 16, 14), 16, 16, P(C(CREAM, a)))
    c.drawArc(skia.Rect(-30, -20, 30, 34), 0, 180, False, P(C(CREAM, a), stroke=6))
    c.drawLine(0, 34, 0, 48, P(C(CREAM, a), stroke=6))
    c.drawLine(-44, -44, 44, 44, P(C(CREAM, a), stroke=9))
    c.restore()

def rec_badge(c, x, y, a, t):
    if a <= 0: return
    c.drawRoundRect(skia.Rect(x - 70, y - 26, x + 70, y + 20), 10, 10, P(C(INK, a * 0.8)))
    c.drawCircle(x - 40, y - 3, 11, P(C(RED, a * (0.5 + 0.5 * math.sin(t * 8)))))
    text(c, "REC", x + 12, y + 10, BEBAS, 36, RED, a, spacing=2)

def video_call(c, cx, cy, w, h, a, t, talk=0.0, fake=0.0, glitch=0.0, label="YOUR CONTACT"):
    inner = screen(c, cx, cy, w, h, a, label="INVESTMENT MEETING")
    big = skia.Rect(inner.left() + 8, inner.top() + 60, inner.right() - 8, inner.bottom() - 8)
    tile(c, big, a, ch_fn(CH.CFO, t, talk), label, glitch=glitch, t=t, fake=fake > 0.5)
    me = skia.Rect(big.right() - 200, big.bottom() - 150, big.right() - 10, big.bottom() - 10)
    tile(c, me, a, ch_fn(CH.EMPLOYEE, t, 0), "YOU", t=t)
    return big

def sc_hook(c, t, D):
    b1 = B("hook", 1)
    big = video_call(c, CX, 910, 900, 560, 1.0, t, talk=0.7, fake=1.0 if t > 1.2 else 0, glitch=0.25 if t > 1.2 else 0)
    counter(c, int(400e6 * eo(prog(t, 0.0, 1.4))) if t > 0.05 else 400000000, CX, 470, 120, GOLD2, 1.0, prefix="$", glow=22)
    text(c, "STOLEN WITH FAKE VIDEO CALLS", CX, 575, BEBAS, 58, CREAM, 1.0, spacing=3)
    if t > b1 - 0.2:
        p = eo(prog(t, b1 - 0.2, 0.3))
        stamp(c, CX + 160, 760, "FBI · NOV 12", RED, 80, -6, p, sc=lerp(2.0, 1, p))

def sc_hijack(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("hijack", 1)
    pop_text(c, "STEP 1: TAKE OVER AN ACCOUNT", CX, 430, ANTON, 72, CREAM, prog(t, 0, 0.25))
    mobile(c, 760, 870, 1.0, a, t, title="TRUSTED CONTACT")
    swap = clamp((t - 1.0) / 0.5)
    CH.CFO.draw(c, 760, 1060, 0.48, -1, a=a * (1 - swap), blink=bl(t))
    if swap > 0: CH.HACKER.draw(c, 760, 1060, 0.48, -1, a=a * swap)
    CH.HACKER.draw(c, 250, 1240, 0.95, 1, a=a, arm_f=(-70 + 8 * math.sin(t * 10), -60), arm_b=(-40, -50))
    laptop(c, 400, 1160, 0.5, a, t)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        for i, lab in enumerate(["FOUNDER", "INVESTOR", "SOMEONE YOU KNOW"]):
            name_chip(c, 760, 600 + i * 0 + (i - 1) * 0, "", 0)
            bubble(c, 760, 680 + i * 80, 280, lab, eo(prog(t, b1 - 0.3 + i * 0.35, 0.3)))

def sc_invite(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("invite", 1)
    pop_text(c, "STEP 2: THE INVITE", CX, 430, ANTON, 88, CREAM, prog(t, 0, 0.25))
    mobile(c, 300, 900, 1.0, a, t, title="TRUSTED CONTACT")
    bubble(c, 300, 720, 270, "LET'S TALK", eo(prog(t, 0.3, 0.3)))
    bubble(c, 300, 800, 270, "INVESTMENT?", eo(prog(t, 0.7, 0.3)))
    p3 = eo(prog(t, 1.2, 0.3))
    if p3 > 0:
        c.drawRoundRect(skia.Rect(185, 860, 415, 1010), 14, 14, P(C(CREAM, p3)))
        text(c, "MEETING INVITE", 300, 910, BEBAS, 36, INK, p3, spacing=2)
        text(c, "JOIN CALL", 300, 975, ANTON, 50, (40, 110, 170), p3)
    for i in range(5):
        pi = eo(prog(t, 0.6 + i * 0.25, 0.4))
        if pi <= 0: continue
        x, y = 820, 600 + i * 140
        arrow(c, 470, 900, lerp(470, x - 90, pi), lerp(900, y, pi), 1.0, a * 0.6)
        CH.EMPLOYEE.draw(c, x, y + 50, 0.32, -1, a=pi, blink=bl(t + i))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, 470, 1180, 440, 100, p, "ZOOM · TEAMS", rgb=(40, 70, 110), size=60)

def sc_call(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("call", 1)
    fake = t > b1 - 0.1
    big = video_call(c, CX, 860, 900, 700, a, t, talk=0.6, fake=1.0 if fake else 0, glitch=0.15 if fake else 0)
    pop_text(c, "YOU SEE A FACE YOU KNOW", CX, 430, ANTON, 80, CREAM, prog(t, 0, 0.25))
    if fake:
        p = prog(t, b1 - 0.1, 0.22)
        rec_badge(c, big.left() + 90, big.top() + 40, a, t)
        stamp(c, CX, 1000, "A RECORDING", RED, 100, -4, p, sc=lerp(2.2, 1, eo(p)))

def sc_fix(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("fix", 1)
    pop_text(c, "THE \"FIX\"", CX, 430, ANTON, 110, CREAM, prog(t, 0, 0.25))
    screen(c, CX, 760, 760, 420, a, label="AUDIO NOT WORKING?")
    mute_icon(c, 280, 760, 0.8, a)
    pl = eo(prog(t, 0.6, 0.4))
    c.drawRoundRect(skia.Rect(400, 700, 820, 780), 14, 14, P(C((40, 110, 170), a * pl)))
    text(c, "CLICK TO FIX AUDIO", 610, 755, BEBAS, 44, CREAM, a * pl, spacing=2)
    c.drawRect(skia.Rect(400, 800, 820, 860), P(C((8, 14, 12), a * pl)))
    text(c, "$ paste this command_", 420, 842, BEBAS, 36, GREEN, a * pl, align="l")
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        stamp(c, CX, 1060, "MALWARE", RED, 120, -6, prog(t, b1 - 0.3, 0.22), sc=lerp(2.2, 1, p))
        for i in range(5):
            pc = prog(t, b1 + 0.4 + i * 0.25, 0.9)
            if pc > 0: crypto_coin(c, lerp(200 + i * 170, 900, eo(pc)), lerp(1220, 1180 - 120 * math.sin(pc * 3.14), pc), 50, a * (1 - pc * 0.6), t)
        CH.HACKER.draw(c, 920, 1250, 0.6, -1, a=p, arm_f=(-60, -50))

def sc_videos(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("videos", 1)
    n = int(900 * eo(prog(t, 0.1, 1.4)))
    counter(c, n, CX, 500, 150, GOLD2, a, prefix="", suffix="+", glow=22)
    text(c, "WEBCAM VIDEOS SEIZED BY THE FBI", CX, 580, BEBAS, 54, CREAM, a, spacing=3)
    for i in range(24):
        r = skia.Rect(100 + (i % 6) * 148, 650 + (i // 6) * 120, 100 + (i % 6) * 148 + 136, 650 + (i // 6) * 120 + 108)
        pi = prog(t, 0.1 + i * 0.05, 0.2)
        if pi > 0:
            chs = [CH.CFO, CH.EMPLOYEE, CH.COLLEAGUE, CH.CLERK]
            tile(c, r, a * pi, ch_fn(chs[i % 4], t), "", t=t)
            c.drawCircle(r.left() + 16, r.top() + 16, 7, P(C(RED, a * pi)))
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1185, 820, 100, p, "BLAMED ON NORTH KOREAN HACKERS", rgb=(70, 34, 30), size=54)

def sc_seize(c, t, D):
    a = eo(prog(t, 0, 0.3)); b1 = B("seize", 1)
    pop_text(c, "COURT ORDERS TO SEIZE", CX, 430, ANTON, 84, CREAM, prog(t, 0, 0.25))
    counter(c, int(1.2e9 * eo(prog(t, 0.2, 1.3))), CX, 570, 120, GOLD2, a, prefix="$", suffix="+", glow=22)
    building(c, 300, 1100, 0.8, a, label="COURT")
    for i in range(6):
        crypto_coin(c, 640 + (i % 3) * 120, 860 + (i // 3) * 130, 52, a, t + i)
    if t > b1 - 0.3:
        p = eo(prog(t, b1 - 0.3, 0.3))
        box(c, CX, 1190, 760, 100, p, "LINKED TO THE BINANCE HACK", rgb=(40, 46, 60), size=58)
        ps = prog(t, b1 - 0.1, 0.22)
        if ps > 0: stamp(c, 760, 1060, "SEIZED", RED, 90, -8, ps, sc=lerp(2.2, 1, eo(ps)))

def sc_quote(c, t, D):
    a = eo(prog(t, 0, 0.3))
    CH.OFFICIAL.draw(c, 250, 1250, 0.9, 1, a=a, blink=bl(t), mouth=0.0, arm_f=(-40, -50))
    paper_doc(c, 760, 1060, 0.45, 4, a, "US JUSTICE DEPT", "NOV 2026", "STATEMENT", lines=6)
    lines = ["\"...WILL USE EVERY TOOL", "AT ITS DISPOSAL TO SEIZE", "AND RETURN NORTH KOREA'S", "ILL-GOTTEN GAINS.\""]
    for i, ln in enumerate(lines):
        text(c, ln, CX, 480 + i * 80, ANTON, 64, GOLD2 if i == 3 else CREAM, eo(prog(t, 0.2 + i * 0.6, 0.3)))
    name_chip(c, CX, 820, "US JUSTICE DEPARTMENT OFFICIAL · NOV 2026", a * 0.9, rgb=GOLD2, size=32)

def sc_question(c, t, D):
    a = eo(prog(t, 0, 0.3))
    video_call(c, CX, 950, 720, 420, a, t, talk=0.5, fake=1.0, glitch=0.2 * (0.5 + 0.5 * math.sin(t * 3)))
    pop_text(c, "REAL FRIEND", CX, 430, ANTON, 96, CREAM, prog(t, 0.0, 0.25))
    pop_text(c, "OR RECORDING?", CX, 535, ANTON, 96, GOLD2, prog(t, 0.3, 0.25), glow=20, glow_rgb=GOLD)
    follow_pill(c, W_("question", "Tell") - 0.1, t, 665)

E.DRAW = dict(hook=sc_hook, hijack=sc_hijack, invite=sc_invite, call=sc_call, fix=sc_fix, videos=sc_videos,
              seize=sc_seize, quote=sc_quote, question=sc_question, rehook=make_rehook("rehook", *S.REHOOK, danger=True))
E.RED_SCENES = {"fix"}
_IMP = [("hook", "FBI", -0.2, 0.4), ("call", "recording", -0.2, 0.45), ("rehook", "sound", -0.2, 0.4), ("fix", "malware", -0.2, 0.45),
        ("videos", "North", -0.2, 0.35), ("seize", "Binance", -0.2, 0.4)]
IMPACTS = [x for x in _IMP if x[0] in SID]
CLINKS = [("hook", "$400", 0.0), ("seize", "$1.2", 0.0)]
E.set_hits(IMPACTS)
ROOT = E.ROOT

if __name__ == "__main__":
    E.main()
