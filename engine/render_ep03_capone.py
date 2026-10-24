import os, sys, math, random
os.environ["REC_ROOT"] = "/home/claude/ep03"
sys.path.insert(0, "/home/claude/ep03")
import skia
import engine as E
from props import *

PH = dict(
    mug=load_photo("capone_mugshot_1931.jpg"),
    portrait=load_photo("capone_1930.jpg", crop=(0, 0, 1920, 1900)),
    time=load_photo("capone_time_1930.jpg"),
    beer=load_photo("beer_destroyed_1923.jpg"),
    chicago=load_photo("chicago_1935.png"),
    alca=load_photo("alcatraz_1930s.jpg"),
)

def tax_form(c, x, y, s, rot, a, k=0.0, stamped=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-300, -380, 300, 380), P(C((234, 225, 202), a)))
    text(c, "FORM 1040", -260, -300, ANTON, 60, INK, a, align="l")
    text(c, "INDIVIDUAL INCOME TAX RETURN", -260, -250, BEBAS, 36, (110, 95, 70), a, align="l", spacing=2)
    rule(c, -260, 260, -228, INK, a, 3)
    for ln in range(8):
        yy = -170 + ln * 60
        c.drawRect(skia.Rect(-260, yy, -60, yy + 10), P(C((160, 148, 125), a)))
        c.drawRect(skia.Rect(60, yy - 22, 260, yy + 12), P(C((160, 148, 125), a), stroke=2))
    text(c, "TAX PAID:", -260, 330, BEBAS, 60, INK, a, align="l", spacing=2)
    text(c, "$0", 230, 335, ANTON, 80, RED, a * clamp(k), align="r")
    c.restore()

def ledger_book(c, x, y, s, a, hl=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-420, -260, 420, 260), 12, 12, P(C((90, 60, 34), a)))
    for side in (-1, 1):
        c.drawRect(skia.Rect(min(0, side * 400), -240, max(0, side * 400), 240), P(C((232, 222, 196), a)))
    c.drawLine(0, -240, 0, 240, P(C((120, 100, 70), a), stroke=4))
    for side in (-1, 1):
        for ln in range(10):
            yy = -200 + ln * 42
            x0 = side * 30 if side > 0 else -380
            c.drawLine(x0, yy, x0 + 350, yy, P(C((170, 150, 120), a), stroke=2))
            c.drawRect(skia.Rect(x0 + 10, yy - 26, x0 + 10 + 120 + (ln * 37 % 90), yy - 14), P(C((60, 60, 90), a * 0.7)))
            text(c, "$" + str(1000 + (ln * 7919 + side * 31) % 9000), x0 + 340, yy - 8, BEBAS, 30, (40, 40, 70), a * 0.8, align="r")
    if hl > 0:
        for ln in (3, 6):
            yy = -200 + ln * 42
            c.drawRect(skia.Rect(30, yy - 36, 30 + 350 * hl, yy + 2), P(C(GOLD2, 0.45 * a)))
        text(c, "\"AL\"", 340, -255, ANTON, 54, RED, a * hl, align="l")
    c.restore()

def gavel(c, x, y, s, a, k):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect(-160, 60, 160, 100), 10, 10, P(C((110, 72, 40), a)))
    ang = lerp(-40, 0, eio(clamp(k)))
    c.save(); c.translate(120, 40); c.rotate(ang)
    c.drawRoundRect(skia.Rect(-260, -14, 0, 14), 7, 7, P(C((130, 86, 48), a)))
    c.drawRoundRect(skia.Rect(-330, -60, -190, 30), 14, 14, P(C((150, 100, 56), a)))
    c.drawRoundRect(skia.Rect(-330, -60, -190, 30), 14, 14, P(C(GOLD, a), stroke=4))
    c.restore()
    c.restore()

def sc_hook(c, t, D):
    a = eo(prog(t, 0, 0.5))
    photo_card(c, PH["mug"], CX, 665, 860, 480, t / D, a, 1.0, 1.1, focus=(0.6, 0.4), rot=-1.5,
               credit="CHICAGO POLICE MUGSHOT, 1931")
    text(c, "CHICAGO · 1931", CX, 385, BEBAS, 72, GOLD, a, spacing=6)
    tm = wt("hook", "Not") - 0.1
    pm = eo(prog(t, tm, 0.25))
    if pm > 0:
        w = text(c, "MURDER", CX, 1040, ANTON, 130, CREAM, pm)
        c.drawLine(CX - w / 2 - 20, 995, CX - w / 2 - 20 + (w + 40) * eo(prog(t, tm + 0.25, 0.25)), 995, P(C(RED, pm), stroke=16))
    pt = prog(t, wt("hook", "taxes.") - 0.1, 0.22)
    if pt > 0: stamp(c, CX, 1165, "TAXES", RED, 100, -8, pt, sc=lerp(2.2, 1.0, eo(pt)))

def sc_rise(c, t, D):
    a = eo(prog(t, 0, 0.5))
    photo_card(c, PH["chicago"], CX, 620, 900, 575, t / D, a, 1.0, 1.15, focus=(0.4, 0.4), rot=1,
               credit="CHICAGO, 1930s · PUBLIC DOMAIN")
    seq_rows(c, t, [("ILLEGAL BEER", wt("rise", "beer,") - 0.1, GOLD2), ("SPEAKEASIES", wt("rise", "speakeasies,"), GOLD2),
                    ("GAMBLING", wt("rise", "gambling.") - 0.1, GOLD2)], 1090, 110)
    text(c, "AL CAPONE", CX, 1190, PLAY, 64, CREAM, eo(prog(t, 0.3, 0.5)), spacing=6)

def sc_money(c, t, D):
    p = eio(prog(t, wt("money", "about") - 0.2, 1.4))
    a = eo(prog(t, 0, 0.3))
    shadowed(c, lambda: text(c, "$" + "{:,.0f}".format(60_000_000 * p), CX, 560, ANTON, 150, GOLD2 if p >= 1 else CREAM, a,
                             glow=24 if p >= 1 else 0, glow_rgb=GOLD))
    text(c, "A YEAR (ESTIMATED)", CX, 650, BEBAS, 66, MUTED, a, spacing=5)
    tz = wt("money", "zero") - 0.4
    pf = eo(prog(t, tz, 0.4))
    if pf > 0: tax_form(c, CX, lerp(1500, 1000, pf), 0.55, -4, 1.0, k=prog(t, tz + 0.5, 0.3))
    for i in range(14):
        R = random.Random(i + 40)
        x = CX + R.uniform(-420, 420); y = 300 + ((t * R.uniform(120, 260) + R.uniform(0, 500)) % 900)
        if y < 820 and pf < 0.5: bills(c, x, y, 0.5 * a * (1 - pf), 1, rot=R.uniform(-30, 30) + t * 40)

def sc_law(c, t, D):
    a = eo(prog(t, 0, 0.4))
    # columns of the court
    c.drawRect(skia.Rect(230, 520, 850, 545), P(C(CREAM, a * 0.9)))
    ped = skia.Path(); ped.moveTo(200, 520); ped.lineTo(CX, 400); ped.lineTo(880, 520); ped.close()
    c.drawPath(ped, P(C(CREAM, a * 0.9)))
    for i in range(6):
        x = 270 + i * 108
        c.drawRect(skia.Rect(x, 560, x + 50, 880), P(C(CREAM, a * 0.85)))
    c.drawRect(skia.Rect(200, 890, 880, 925), P(C(CREAM, a * 0.9)))
    text(c, "U.S. SUPREME COURT · 1927", CX, 990, BEBAS, 64, GOLD, a, spacing=4)
    pr = eo(prog(t, wt("law", "illegal") - 0.3, 0.35))
    pill(c, "ILLEGAL MONEY CAN BE TAXED", 1160, pr, GOLD2, 66, 900)

def sc_boast(c, t, D):
    a = eo(prog(t, 0, 0.5))
    photo_card(c, PH["time"], CX, 650, 520, 685, t / D, a, 1.0, 1.08, focus=(0.5, 0.55), rot=-2,
               credit="TIME MAGAZINE COVER, 1930 · PUBLIC DOMAIN")
    pq = eo(prog(t, wt("boast", "They") - 0.2, 0.4))
    if pq > 0:
        c.drawRoundRect(skia.Rect(80, 1040, 1000, 1225), 30, 30, P(C(INK, 0.9 * pq)))
        text(c, "\"THEY CAN'T COLLECT LEGAL TAXES", CX, 1115, BEBAS, 62, CREAM, pq, spacing=1)
        text(c, "FROM ILLEGAL MONEY.\"", CX, 1190, BEBAS, 62, GOLD2, pq, spacing=1)

def sc_agent(c, t, D):
    a = eo(prog(t, 0, 0.4))
    n = int(lerp(0, 2_000_000, eio(prog(t, wt("agent", "about") - 0.2, 1.6))))
    for i in range(40):
        R = random.Random(i + 300); k = clamp((t - i * 0.06) / 0.5)
        if k <= 0: continue
        x = CX + R.uniform(-380, 380); y = 900 - (i // 8) * 34 + R.uniform(-6, 6)
        c.save(); c.translate(x, y); c.rotate(R.uniform(-12, 12))
        c.drawRect(skia.Rect(-80, -14, 80, 14), P(C((228, 218, 194), a * k))); c.drawRect(skia.Rect(-80, -14, 80, 14), P(C((150, 136, 110), a * k), stroke=2))
        c.restore()
    text(c, "{:,}".format(n), CX, 560, ANTON, 170, CREAM if n < 2_000_000 else GOLD2, a, glow=20 if n >= 2_000_000 else 0, glow_rgb=GOLD)
    text(c, "DOCUMENTS", CX, 650, BEBAS, 70, MUTED, a, spacing=8)
    pw = eo(prog(t, wt("agent", "Frank") - 0.2, 0.4))
    pill(c, "IRS AGENT FRANK WILSON", 1130, pw, GOLD2, 66)

def sc_ledger(c, t, D):
    a = eo(prog(t, 0, 0.4))
    pf = eo(prog(t, wt("ledger", "found") - 0.2, 0.3))
    if pf > 0: pop_text(c, "FOUND IT.", CX, 470, ANTON, 120, GOLD2, pf, glow=22, glow_rgb=GOLD)
    ledger_book(c, CX, 790, lerp(0.8, 1.0, eo(prog(t, 0, 1.0))) * 0.98, a, hl=eo(prog(t, wt("ledger", "payments") - 0.2, 0.8)))
    pn = eo(prog(t, wt("ledger", "never") - 0.2, 0.3))
    pill(c, "PAYMENTS NEVER REPORTED", 1160, pn, CREAM, 66)

def sc_trial(c, t, D):
    a = eo(prog(t, 0, 0.4))
    tr = beat("trial", 1)
    text(c, "U.S. v. ALPHONSE CAPONE", CX, 450, PLAY, 70, CREAM, a)
    pd = eo(prog(t, wt("trial", "deal") - 0.3, 0.4)) * (1 - eo(prog(t, tr - 0.1, 0.2)))
    if pd > 0:
        c.save(); c.translate(CX, 760)
        c.drawRect(skia.Rect(-280, -200, 280, 200), P(C((234, 225, 202), pd)))
        text(c, "PLEA DEAL", 0, -110, ANTON, 80, INK, pd)
        text(c, "2 YEARS", 0, 40, ANTON, 150, INK, pd)
        c.restore()
    pr = prog(t, tr - 0.1, 0.22)
    if pr > 0:
        c.save(); c.translate(CX, 760)
        c.drawRect(skia.Rect(-280, -200, 280, 200), P(C((234, 225, 202), 1)))
        text(c, "PLEA DEAL", 0, -110, ANTON, 80, INK, 1); text(c, "2 YEARS", 0, 40, ANTON, 150, INK, 1)
        c.restore()
        stamp(c, CX, 760, "REJECTED", RED, 120, -12, pr, sc=lerp(2.2, 1.0, eo(pr)))
        text(c, "THE JUDGE SAID NO", CX, 1100, BEBAS, 76, CREAM, eo(prog(t, tr + 0.3, 0.3)), spacing=4)

def sc_verdict(c, t, D):
    a = eo(prog(t, 0, 0.3))
    tg = wt("verdict", "guilty.") - 0.15
    gavel(c, CX, 560, 1.0, a, prog(t, tg - 0.25, 0.25))
    pg = prog(t, tg, 0.2)
    if pg > 0:
        c.drawRect(skia.Rect(0, 300, W, 1230), P(C(CREAM, 0.25 * (1 - prog(t, tg, 0.3)))))
        stamp(c, CX, 820, "GUILTY", RED, 130, -6, pg, sc=lerp(2.2, 1.0, eo(pg)), sub="OCTOBER 17, 1931")
    seq_rows(c, t, [("11 YEARS IN PRISON", wt("verdict", "11") - 0.1, CREAM),
                    ("+ $80,000 FINES & COSTS", wt("verdict", "$80,000") - 0.1, GOLD2)], 1130, 84)

def sc_prison(c, t, D):
    a = eo(prog(t, 0, 0.4))
    photo_card(c, PH["alca"], CX, 640, 900, 533, t / D, a, 1.0, 1.15, focus=(0.42, 0.45), rot=-1, credit="ALCATRAZ, 1930s · U.S. NAVY")
    seq_rows(c, t, [("ATLANTA", wt("prison", "Atlanta,") - 0.1, CREAM), ("ALCATRAZ", wt("prison", "Alcatraz.") - 0.2, RED)], 1080, 130)

def sc_ending(c, t, D):
    b1 = beat("ending", 1)
    out = eo(prog(t, b1 - 0.3, 0.4))
    a = eo(prog(t, 0, 0.5)) * (1 - out)
    photo_card(c, PH["portrait"], CX, 640, 600, 600, t / D, a, 1.0, 1.1, focus=(0.5, 0.25), rot=1.5, credit="AL CAPONE, 1930 · PUBLIC DOMAIN")
    if out < 1:
        layer_alpha(c, 1 - out)
        seq_rows(c, t, [("RELEASED 1939", wt("ending", "1939,") - 0.3, CREAM), ("DIED 1947", wt("ending", "1947.") - 0.2, MUTED)], 1090, 100)
        c.restore()
    if out > 0:
        text(c, "THE MAN WHO BEAT", CX, 640, BEBAS, 100, CREAM, out, spacing=6)
        text(c, "EVERY BULLET", CX, 780, ANTON, 150, CREAM, out * eo(prog(t, wt("ending", "every") - 0.2, 0.3)))
        pb = prog(t, wt("ending", "bookkeeper.") - 0.15, 0.25)
        if pb > 0:
            text(c, "WAS BEATEN BY", CX, 900, BEBAS, 80, MUTED, out, spacing=6)
            pop_text(c, "A BOOKKEEPER.", CX, 1060, ANTON, 150, GOLD2, pb, glow=28, glow_rgb=GOLD)

def sc_cta(c, t, D):
    a = eo(prog(t, 0, 0.4))
    text(c, "NEXT EPISODE", CX, 450, BEBAS, 70, MUTED, a, spacing=10)
    for i in range(5):
        x = 250 + i * 145; p = eo(prog(t, 0.2 + i * 0.1, 0.3))
        c.drawCircle(x, 700, 52, P(C(CREAM, a * p)))
        c.drawCircle(x - 18, 690, 9, P(C(INK, p))); c.drawCircle(x + 18, 690, 9, P(C(INK, p)))
        c.drawArc(skia.Rect(x - 22, 700, x + 22, 730), 0, 180, False, P(C(INK, p), stroke=5))
        c.drawRoundRect(skia.Rect(x - 46, 770, x + 46, 860), 30, 30, P(C((40, 46, 70), a * p)))
    text(c, "11 MEN · HALLOWEEN MASKS", CX, 960, BEBAS, 66, CREAM, eo(prog(t, wt("cta", "Halloween") - 0.3, 0.3)), spacing=3)
    pop_text(c, "$2.7 MILLION", CX, 1090, ANTON, 140, GOLD2, prog(t, wt("cta", "$2.7") - 0.1, 0.25), glow=26, glow_rgb=GOLD)
    follow_pill(c, wt("cta", "Follow") - 0.1, t, 1190)

E.DRAW = dict(hook=sc_hook, rise=sc_rise, money=sc_money, law=sc_law, boast=sc_boast, agent=sc_agent, ledger=sc_ledger,
              trial=sc_trial, verdict=sc_verdict, prison=sc_prison, ending=sc_ending, cta=sc_cta)
E.RED_SCENES = {"verdict", "prison"}
IMPACTS = [("hook", "taxes.", -0.1, 0.35), ("money", "zero", 0.1, 0.25), ("boast", "They", -0.2, 0.2), ("ledger", "found", -0.2, 0.3),
           ("trial", "refused.", -0.3, 0.3), ("verdict", "guilty.", -0.15, 0.45), ("ending", "bookkeeper.", -0.15, 0.35),
           ("cta", "$2.7", -0.1, 0.3)]
CLINKS = [("money", "about", 0.0)]

if __name__ == "__main__":
    E.main()
