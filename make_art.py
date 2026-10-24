"""Builds the SVG art for the Cutscene Labs GitHub profile page.

Mirrors cutscene.me: near-white page, white column, timeline rail with coloured
ring nodes, Geist and Geist Mono embedded so GitHub shows the real type.
Run: python make_art.py <folder holding fonts/ and logo144.png>
"""
import base64, sys, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path(sys.argv[1])
OUT = Path(__file__).parent / "profile" / "art"
OUT.mkdir(parents=True, exist_ok=True)

BG, FG, CARD, MUTED, MUTED_FG = "#f6f7f8", "#121417", "#ffffff", "#eef0f2", "#5b616b"
BORDER, PRIMARY = "#e1e4e8", "#3b6fe0"
LANE = {"clinical": "#0c8599", "education": "#2f9e44", "resources": "#b7791f"}
STATUS = {"live": ("in production", "#2f9e44"), "soon": ("almost ready", "#b7791f"),
          "dev": ("in development", "#9aa0a6")}

ICON = {
    "heart": '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1z"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5"/><path d="M22 9v6"/>',
    "book": '<path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2z"/><path d="M22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "log": '<circle cx="12" cy="12" r="3.5"/><path d="M12 2v6.5M12 15.5V22"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def fonts(*names):
    rules = []
    for fam, weight, file in names:
        rules.append(f'@font-face{{font-family:"{fam}";font-weight:{weight};'
                     f'src:url(data:font/woff2;base64,{b64(SRC / "fonts" / file)}) format("woff2")}}')
    return ("<style>" + "".join(rules) +
            '.s{font-family:"Geist",system-ui,sans-serif}.m{font-family:"Geist Mono",ui-monospace,monospace}'
            "</style>")


SANS = [("Geist", 400, "geist-latin-400-normal.woff2"), ("Geist", 500, "geist-latin-500-normal.woff2"),
        ("Geist", 600, "geist-latin-600-normal.woff2"), ("Geist", 700, "geist-latin-700-normal.woff2"),
        ("Geist Mono", 400, "geist-mono-latin-400-normal.woff2")]


def icon(name, x, y, size, color, sw=1.75):
    k = size / 24
    return (f'<g transform="translate({x} {y}) scale({k})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')


def ring(cx, cy, lane, name, r=22):
    """A lab node: white halo, coloured ring, muted disc, coloured icon."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="{CARD}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 1}" fill="none" stroke="{lane}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 3}" fill="{MUTED}"/>' +
            icon(name, cx - 11, cy - 11, 22, lane))


def dot(cx, cy, lane):
    return (f'<circle cx="{cx}" cy="{cy}" r="8" fill="{lane}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{lane}" stroke="{CARD}" stroke-width="3"/>')


def t(x, y, s, size, weight=400, fill=FG, cls="s", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


# ---------------------------------------------------------------- banner
def banner():
    W, H, SIDE = 1280, 440, 330
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         fonts(*SANS),
         f'<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath><g clip-path="url(#c)">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    # sidebar
    o.append(f'<image href="data:image/png;base64,{b64(SRC / "logo144.png")}" x="40" y="40" width="56" height="56"/>')
    o.append(t(110, 80, "Cutscene Labs", 30, 700, extra='letter-spacing="-0.9"'))
    o.append(t(44, 126, "Clinical, educational and", 16, 400, MUTED_FG))
    o.append(t(44, 148, "productivity tools", 16, 400, MUTED_FG))
    for i, (ic, label) in enumerate([("home", "Welcome"), ("info", "About"), ("log", "Log"), ("mail", "Contact")]):
        y = 192 + i * 42
        col = FG if i == 0 else MUTED_FG
        o.append(icon(ic, 48, y - 15, 20, col))
        o.append(t(82, y, label, 17, 500, col))
    o.append(f'<rect x="36" y="362" width="200" height="40" rx="8" fill="{PRIMARY}"/>')
    o.append(icon("globe", 52, 372, 20, "#fff"))
    o.append(t(84, 388, "Play the atlas", 16, 500, "#fff"))
    # white column
    cx0 = SIDE + 20
    o.append(f'<rect x="{cx0}" y="0" width="{W - cx0}" height="{H}" fill="{CARD}"/>')
    o.append(f'<line x1="{cx0}" y1="0" x2="{cx0}" y2="{H}" stroke="{BORDER}"/>')
    tabs = ["Welcome", "About", "Log"]
    tw = (W - cx0) / 3
    for i, label in enumerate(tabs):
        mx = cx0 + tw * i + tw / 2
        o.append(t(mx, 38, label, 17, 500, FG if i == 0 else MUTED_FG, anchor="middle"))
    o.append(f'<line x1="{cx0}" y1="62" x2="{W}" y2="62" stroke="{BORDER}"/>')
    o.append(f'<rect x="{cx0}" y="59" width="{tw}" height="3" fill="{PRIMARY}"/>')
    o.append(t(cx0 + 48, 150, "Welcome to Cutscene", 64, 700, extra='letter-spacing="-1.9"'))
    o.append(t(cx0 + 50, 196, "We make stuff.", 26, 400, MUTED_FG))
    # the three labs on a rail
    labs = [("clinical", "heart", "Clinical", "4 products"),
            ("education", "cap", "Education", "3 products"),
            ("resources", "book", "Resources", "1 product")]
    y = 310
    xs = [cx0 + 110 + i * 270 for i in range(3)]
    for a, b, (k, _, _, _), (k2, _, _, _) in zip(xs, xs[1:], labs, labs[1:]):
        o.append(f'<defs><linearGradient id="g{k}" x1="0" x2="1"><stop offset="0" stop-color="{LANE[k]}"/>'
                 f'<stop offset="1" stop-color="{LANE[k2]}"/></linearGradient></defs>')
        o.append(f'<rect x="{a}" y="{y - 1}" width="{b - a}" height="2" fill="url(#g{k})"/>')
    o.append(f'<rect x="{xs[-1]}" y="{y - 1}" width="{W - xs[-1]}" height="2" fill="{LANE["resources"]}" opacity=".35"/>')
    for x, (k, ic, label, count) in zip(xs, labs):
        o.append(ring(x, y, LANE[k], ic, 28).replace(icon(ic, x - 11, y - 11, 22, LANE[k]),
                                                      icon(ic, x - 14, y - 14, 28, LANE[k])))
        o.append(t(x, y + 62, label, 18, 600, anchor="middle"))
        o.append(t(x, y + 86, count, 13, 400, MUTED_FG, "m", "middle"))
    o.append("</g>")
    o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{BORDER}"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- lab cards
LABS = [
    ("clinical", "heart", "Our Clinical Products Lab",
     "We help clinicians keep their private practices, and their clients' data, safe and independent. "
     "We help clients stay connected to their care.",
     [("limn", "soon", "Our medical record system. Shipping soon."),
      ("SovereignBoard", "live", "A private keyboard with LLM features, covered by a signed BAA."),
      ("Open Treatment Planner", "dev", "A public treatment planner built on the Power Threat Meaning Framework "
       "and other non-pathologising perspectives. Our answer to the Wiley Treatment Planner."),
      ("One Day at a Time", "dev", "Counts your days and puts the time-honoured tradition of AA in your hand.")]),
    ("education", "cap", "Our Education Lab", "Games and tools that teach.",
     [("Magellan's Disappearing Atlas", "live", "The game we built to teach children world geography and civics."),
      ("Cutscene GIS", "dev", "Our own globe, built from public data and home-grown historical models."),
      ("Quizzical", "dev", "Flash cards you answer out loud, with speech recognition and an LLM's help.")]),
    ("resources", "book", "Our Resources Lab", "Free guides and lists for the people we build for.",
     [("Awesome Technology for Therapists", "live",
       "A public, open list of technology for therapists who want to keep their practices private and independent.")]),
]


def lab(key, ic, title, blurb, products):
    W, RAIL, PAD = 880, 76, 20
    lane = LANE[key]
    wrap = 100
    rows = []  # (kind, height, payload)
    blurb_lines = textwrap.wrap(blurb, wrap)
    head_h = 34 + 22 * len(blurb_lines) + 34
    y = 0
    parts = []
    # head
    cy = 40
    body_x = RAIL
    parts.append(t(body_x, 36, title, 18, 600))
    for i, line in enumerate(blurb_lines):
        parts.append(t(body_x, 62 + 22 * i, line, 15, 400, FG))
    n = len(products)
    parts.append(t(body_x, 62 + 22 * len(blurb_lines) + 6, f"{n} product{'s' if n != 1 else ''}", 12.5, 400,
                   MUTED_FG, "m"))
    y = head_h + 22
    first_dot = None
    last_dot = None
    for i, (name, st, text) in enumerate(products):
        top = y
        if i == 0:
            parts.append(f'<line x1="{body_x}" y1="{top - 8}" x2="{W - PAD}" y2="{top - 8}" stroke="{BORDER}"/>')
        lines = textwrap.wrap(text, wrap)
        dy = top + 20
        parts.append(t(body_x, dy, name, 15.5, 600))
        label, scol = STATUS[st]
        parts.append(f'<circle cx="{W - PAD - 7.2 * len(label) - 14}" cy="{dy - 4.5}" r="4" fill="{scol}"/>')
        parts.append(t(W - PAD, dy, label, 12.5, 400, MUTED_FG, "m", "end"))
        for j, line in enumerate(lines):
            parts.append(t(body_x, dy + 23 + 22 * j, line, 15, 400, FG))
        dot_y = dy - 5
        first_dot = first_dot or dot_y
        last_dot = dot_y
        parts.append(("DOT", dot_y))
        y = dy + 23 + 22 * (len(lines) - 1) + 20
        if i < n - 1:
            parts.append(f'<line x1="{body_x}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{BORDER}"/>')
        y += 14
    H = int(y + 6)
    rx = RAIL / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         fonts(*SANS),
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{CARD}" stroke="{BORDER}"/>',
         f'<rect x="{rx - 1}" y="{cy}" width="2" height="{last_dot - cy}" fill="{lane}"/>',
         ring(rx, cy, lane, ic)]
    for p in parts:
        o.append(dot(rx, p[1], lane) if isinstance(p, tuple) else p)
    o.append("</svg>")
    return "".join(o)


(OUT / "banner.svg").write_text(banner(), encoding="utf-8")
for key, *rest in LABS:
    (OUT / f"lab-{key}.svg").write_text(lab(key, *rest), encoding="utf-8")
print("wrote", sorted(p.name for p in OUT.iterdir()))
