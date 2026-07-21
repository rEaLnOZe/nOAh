#!/usr/bin/env python3
"""CB1 full edit: word-punch captions + a text-centered viral-broll CARD (the 3
questions) + brand bug. Emits edit.ass. Zoom punches are done in ffmpeg."""
import re

W, H = 1080, 1920
FONT = "Liberation Sans"
BASE = 104
Y = 1430
ORANGE = "&H007AFF&"   # #FF7A00 (BGR)
ODARK = "&H0033CC&"    # #CC3300-ish darker orange accent (BGR of ~#FF3B00 -> 003BFF)
ORANGE2 = "&H003BFF&"  # #FF3B00
WHITE = "&HFFFFFF&"
INK = "&H1A1A1A&"       # near-black text for light cards
GREY = "&HB8B8B8&"

# caption segments (start,end,text,emphasis) — the 13.0-16.8 window is a CARD, skipped here
SEG = [
    (0.00, 3.00, "Influencer Marketing hat kein Reichweitenproblem", {"kein", "reichweitenproblem"}),
    (3.00, 5.00, "es hat ein Infrastrukturproblem", {"infrastrukturproblem"}),
    (5.00, 6.00, "und fast keiner sieht das", {"keiner"}),
    (6.00, 8.00, "wir tun so als wär die Frage welchen Creator", {"welchen", "creator"}),
    (8.00, 10.00, "buch ich aber das ist der einfachste Teil", {"einfachste"}),
    (10.00, 12.00, "den löst du mit zwei Klicks die echten Fragen", {"zwei", "klicks", "echten", "fragen"}),
    (12.00, 13.00, "die kommen danach", {"danach"}),
    # 13.0-16.8 -> CARD (three questions)
    (16.90, 18.00, "und genau da bricht alles zusammen", {"bricht", "zusammen"}),
    (18.00, 19.05, "weil sich keiner dran hält", {"keiner"}),
]

def norm(w):
    return re.sub(r"[^\wäöüßÄÖÜ]", "", w).lower()

def fit_fs(words, base, max_w=1000):
    """Shrink font so the WHOLE uppercase line fits max_w px (bold sans caps
    advance ~0.60*fs, space ~0.32*fs). Fixes wide 3-word lines overflowing."""
    chars = sum(len(w) for w in words)
    spaces = max(0, len(words) - 1)
    per_fs = chars * 0.60 + spaces * 0.32
    return int(min(base, max_w / per_fs)) if per_fs else base

def chunk(words, n=3):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == n or w.endswith("?"):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def ts(t):
    cs = int(round(t*100)); h,cs = divmod(cs,360000); m,cs = divmod(cs,6000); s,cs = divmod(cs,100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

ev = []  # (layer, start, end, style, text)

# ---------- caption cues ----------
for start, end, text, emph in SEG:
    cues = chunk(text.split(), 3)
    weights = [sum(len(w) for w in c) for c in cues]; total = sum(weights) or 1
    t = start
    for c, wt in zip(cues, weights):
        cs_, ce_ = t, t + (end-start)*(wt/total); t = ce_
        fs = fit_fs([w.upper() for w in c], BASE, max_w=1000)
        parts = [f"{{\\c{ORANGE if norm(w) in emph else WHITE}}}{w.upper()}" for w in c]
        eff = f"{{\\an5\\pos({W//2},{Y})\\fs{fs}\\fscx82\\fscy82\\t(0,110,\\fscx100\\fscy100)\\fad(70,60)}}"
        ev.append((0, cs_, ce_, "WP", eff + " ".join(parts)))

# ---------- CARD: the three questions (text-centered viral-broll archetype) ----------
C0, C1 = 13.00, 16.80
# full-frame off-white panel
ev.append((2, C0, C1, "CARD",
    f"{{\\an7\\pos(0,0)\\p1\\c&HF3F5F6&\\bord0\\shad0\\fad(160,180)}}m 0 0 l {W} 0 l {W} {H} l 0 {H}"))
# soft corner shades (blurred dark blobs)
ev.append((2, C0, C1, "CARD",
    f"{{\\an7\\pos(-120,-160)\\p1\\c&H000000&\\alpha&HE6&\\bord0\\shad0\\blur40\\fad(160,180)}}m 0 0 l 620 0 l 620 620 l 0 620"))
ev.append((2, C0, C1, "CARD",
    f"{{\\an7\\pos({W-500},{H-520})\\p1\\c&H000000&\\alpha&HEC&\\bord0\\shad0\\blur40\\fad(160,180)}}m 0 0 l 620 0 l 620 620 l 0 620"))
# faint watermark word behind
ev.append((3, C0, C1, "WM",
    f"{{\\an5\\pos({W//2},960)\\fs300\\c{GREY}\\alpha&HDA&\\fscx100\\fscy100\\fad(180,180)}}FRAGEN"))
# small eyebrow + accent diamonds
ev.append((4, C0, C1, "EB",
    f"{{\\an5\\pos({W//2},560)\\fs48\\c{ORANGE2}\\bord0\\fad(200,160)}}◆  DIE ECHTEN FRAGEN  ◆"))
# three questions, revealed one by one, key word orange
Q = [
    (13.15, "Wird {geliefert}?", 820),
    (14.25, "Ist mein Geld {sicher}?", 1010),
    (15.35, "Ist die Reichweite {echt}?", 1200),
]
def card_line(text):
    out = []
    for w in text.split():
        m = re.match(r"\{(.+)\}([?!.,:]*)", w)
        if m:
            out.append(f"{{\\c{ORANGE}}}{m.group(1)}{m.group(2)}{{\\c{INK}}}")
        else:
            out.append(w)
    return " ".join(out)
for qs, txt, y in Q:
    plain = [re.sub(r"[{}]", "", w) for w in txt.split()]
    qfs = fit_fs(plain, 100, max_w=960)
    ev.append((5, qs, C1, "Q",
        f"{{\\an5\\pos({W//2},{y})\\fs{qfs}\\c{INK}\\fscx86\\fscy86\\t(0,140,\\fscx100\\fscy100)\\fad(120,140)}}"
        + card_line(txt)))

# ---------- brand bug (subtle, throughout) ----------
ev.append((9, 0.0, 19.05, "BUG",
    f"{{\\an7\\pos(46,64)\\fs44\\c{ORANGE}\\alpha&H50&\\bord2\\3c&H000000&}}creatr{{\\c{WHITE}\\alpha&H60&}}labs"))

# ---------- styles ----------
def style(name, fs, primary, outline="&H000000&", bord=4, shad=4, align=5):
    return (f"Style: {name},{FONT},{fs},{primary},{primary},{outline},&H90000000&,"
            f"-1,0,0,0,100,100,1,0,1,{bord},{shad},{align},40,40,60,0")

header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{style("WP", BASE, WHITE, bord=7, shad=4)}
{style("CARD", 40, WHITE, bord=0, shad=0, align=7)}
{style("WM", 300, GREY, bord=0, shad=0)}
{style("EB", 48, ORANGE2, bord=0, shad=0)}
{style("Q", 96, INK, outline="&H00FFFFFF&", bord=0, shad=0)}
{style("BUG", 44, ORANGE, bord=2, shad=0, align=7)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

ev.sort(key=lambda e: (e[1], e[0]))
with open("edit.ass", "w") as f:
    f.write(header)
    for layer, s, e, st, txt in ev:
        f.write(f"Dialogue: {layer},{ts(s)},{ts(e)},{st},,0,0,0,,{txt}\n")
print(f"wrote edit.ass with {len(ev)} events")
