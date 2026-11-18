#!/usr/bin/env python3
"""Generate animated SVG assets for the DEMONKINGKAI profile README."""
import os, math
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# ---- palette: void base + 3 accents ----
BG = "#07080D"
PANEL = "#0C0E16"
PANEL2 = "#10131D"
LINE = "#1C2133"
TEXT = "#E8EAF2"
SOFT = "#A3AAC0"
MUTED = "#626A82"
CY = "#00E5FF"   # cyan   - data / signal
VI = "#9B5CFF"   # violet - models / structure
AM = "#FFB020"   # amber  - evidence / highlight

MONO = "'JetBrains Mono','Fira Code','Cascadia Code','SF Mono',Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI','Inter','Helvetica Neue',Arial,'DejaVu Sans',sans-serif"
W = 900


def svg(h, body, defs="", style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" fill="none">
<defs>
<linearGradient id="brand" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
<stop offset="0" stop-color="{CY}"/><stop offset="0.5" stop-color="{VI}"/><stop offset="1" stop-color="{AM}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;{W//2} 0;0 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
{defs}
</defs>
<style>
text{{font-family:{SANS};}}
.mono{{font-family:{MONO};}}
{style}
</style>
{body}
</svg>
'''


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def frame(h, accent=None, rx=14):
    stroke = accent if accent else LINE
    op = "0.35" if accent else "1"
    return f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="{rx}" fill="{PANEL}" stroke="{stroke}" stroke-opacity="{op}"/>'


def runner(h, color, rx=14, dur=7):
    """A light segment that travels around the card border."""
    return (f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{color}" '
            f'stroke-width="1.6" pathLength="100" stroke-dasharray="10 90" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" values="0;-100" dur="{dur}s" repeatCount="indefinite"/></rect>')


# =====================================================================
# HEADER
# =====================================================================
def header():
    H = 340
    nodes = {
        "A": (600, 86, CY), "B": (712, 58, VI), "C": (830, 92, AM),
        "D": (640, 172, VI), "E": (772, 160, CY),
        "G": (596, 268, AM), "H": (716, 256, CY), "I": (838, 262, VI),
    }
    edges = [("A", "D"), ("B", "D"), ("B", "E"), ("C", "E"), ("D", "G"), ("D", "H"),
             ("E", "H"), ("E", "I"), ("C", "I"), ("A", "B")]
    labels = {"B": "do(x)", "H": "y", "G": "z", "C": "claim", "A": "evidence"}
    g = []
    for i, (a, b) in enumerate(edges):
        x1, y1, c1 = nodes[a]; x2, y2, _ = nodes[b]
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1.5"/>')
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c1}" stroke-opacity="0.55" stroke-width="1.5" stroke-dasharray="3 9">'
                 f'<animate attributeName="stroke-dashoffset" values="24;0" dur="{1.2 + (i % 3) * 0.4:.1f}s" repeatCount="indefinite"/></line>')
        dur = 2.2 + (i % 4) * 0.5
        g.append(f'<circle r="2.6" fill="{c1}" filter="url(#glow)"><animateMotion dur="{dur}s" begin="{i*0.37:.2f}s" repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.8;1" dur="{dur}s" begin="{i*0.37:.2f}s" repeatCount="indefinite"/></circle>')
    for i, (k, (x, y, c)) in enumerate(nodes.items()):
        g.append(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{c}" stroke-opacity="0.7">'
                 f'<animate attributeName="r" values="9;22" dur="2.8s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values="0.6;0" dur="2.8s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/></circle>')
        g.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{c}" stroke-width="2"/>')
        g.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c}" filter="url(#glow)"/>')
        if k in labels:
            g.append(f'<text class="mono" x="{x + 15}" y="{y + 4}" font-size="11" fill="{MUTED}">{esc(labels[k])}</text>')
    graph = "\n".join(g)

    tagline = "I build AI that shows its work."
    cw = 11.0
    n = len(tagline)
    typed = [f"{i*cw:.1f}" for i in range(n + 1)]
    vals = typed + [typed[-1]] * 12 + list(reversed(typed))[::3] + ["0"]
    kt = [f"{i/(len(vals)-1):.4f}" for i in range(len(vals))]
    vals_x = [f"{48 + float(v):.1f}" for v in vals]

    defs = f'''
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#ffffff" stroke-opacity="0.035"/></pattern>
<radialGradient id="g1" cx="0.18" cy="0.2" r="0.6"><stop offset="0" stop-color="{CY}" stop-opacity="0.16"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="0.85" cy="0.75" r="0.55"><stop offset="0" stop-color="{VI}" stop-opacity="0.20"/><stop offset="1" stop-color="{VI}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="0.5" stop-color="{CY}" stop-opacity="0.07"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
<linearGradient id="namegrad" x1="44" y1="0" x2="310" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
<stop offset="0" stop-color="{CY}"/><stop offset="0.5" stop-color="{VI}"/><stop offset="1" stop-color="{AM}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;266 0;0 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<clipPath id="typeclip"><rect x="48" y="236" height="32" width="0">
<animate attributeName="width" values="{';'.join(vals)}" keyTimes="{';'.join(kt)}" dur="9s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'''
    style = f'''
.g1{{animation:gl1 5s infinite steps(1);}} .g2{{animation:gl2 5s infinite steps(1);}}
@keyframes gl1{{0%,88%,100%{{opacity:0;transform:translate(0,0)}} 89%{{opacity:.85;transform:translate(-4px,1px)}} 91%{{opacity:.6;transform:translate(3px,-1px)}} 93%{{opacity:0}}}}
@keyframes gl2{{0%,88%,100%{{opacity:0;transform:translate(0,0)}} 90%{{opacity:.85;transform:translate(4px,-1px)}} 92%{{opacity:.6;transform:translate(-3px,1px)}} 94%{{opacity:0}}}}
.blink{{animation:bl 1s infinite steps(1);}} @keyframes bl{{50%{{opacity:0}}}}
.rise{{animation:rise 1s ease-out both;}} @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}'''
    body = f'''<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#g1)"/>
<rect width="{W}" height="{H}" fill="url(#g2)"/>
{graph}
<rect x="0" y="-90" width="{W}" height="90" fill="url(#scan)"><animate attributeName="y" values="-90;{H}" dur="6s" repeatCount="indefinite"/></rect>

<text class="mono rise" x="48" y="68" font-size="14" fill="{MUTED}"><tspan fill="{CY}">❯</tspan> whoami <tspan fill="{LINE}">│</tspan> <tspan fill="{VI}">archit_sharma</tspan></text>

<text class="g1" x="44" y="168" font-size="112" font-weight="800" letter-spacing="10" fill="{CY}">KAI</text>
<text class="g2" x="44" y="168" font-size="112" font-weight="800" letter-spacing="10" fill="{AM}">KAI</text>
<text x="44" y="168" font-size="112" font-weight="800" letter-spacing="10" fill="url(#namegrad)">KAI</text>

<text class="rise" x="48" y="208" font-size="20" fill="{TEXT}" style="animation-delay:.3s">AI / ML Engineer <tspan fill="{MUTED}">·</tspan> <tspan fill="{SOFT}">MSc @ TU Darmstadt</tspan></text>

<g clip-path="url(#typeclip)"><text class="mono" x="48" y="258" font-size="18" fill="{AM}">{esc(tagline)}</text></g>
<rect y="242" width="10" height="21" fill="{AM}" class="blink"><animate attributeName="x" values="{';'.join(vals_x)}" keyTimes="{';'.join(kt)}" dur="9s" calcMode="discrete" repeatCount="indefinite"/></rect>

<text class="mono rise" x="48" y="304" font-size="12.5" fill="{MUTED}" style="animation-delay:.6s"><tspan fill="{CY}">causal inference</tspan>  ·  <tspan fill="{VI}">probabilistic graphical models</tspan>  ·  <tspan fill="{AM}">grounded generative AI</tspan></text>
<text class="mono" x="{W-24}" y="30" font-size="11" fill="{MUTED}" text-anchor="end">darmstadt, de <tspan fill="{CY}">●</tspan></text>
<rect x="0" y="{H-3}" width="{W}" height="3" fill="url(#brand)"/>
</g>'''
    save("header.svg", svg(H, body, defs, style))


# =====================================================================
# SECTION TITLES
# =====================================================================
def section(name, label, color, num):
    H = 58
    body = f'''<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>
<clipPath id="tc"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<text class="mono" x="24" y="35" font-size="13" fill="{MUTED}">{num}</text>
<text class="mono" x="56" y="36" font-size="21" font-weight="700" fill="{TEXT}"><tspan fill="{color}">//</tspan> {esc(label)}</text>
<g clip-path="url(#tc)"><rect x="-180" y="{H-3}" width="180" height="3" rx="1.5" fill="{color}" filter="url(#glow)"><animate attributeName="x" values="-180;{W}" dur="4.5s" repeatCount="indefinite"/></rect></g>
<circle cx="{W-28}" cy="29" r="4" fill="{color}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>'''
    save(f"title-{name}.svg", svg(H, body))


# =====================================================================
# ABOUT TERMINAL
# =====================================================================
def about():
    lines = [
        [(CY, "❯ "), (TEXT, "cat about.yml")],
        [(CY, "name"), (MUTED, ": "), (AM, 'Archit "Kai" Sharma')],
        [(CY, "study"), (MUTED, ": "), (TEXT, "MSc AI & ML @ TU Darmstadt  "), (MUTED, "# grad 2027")],
        [(CY, "before"), (MUTED, ": "), (TEXT, "Product Engineer @ EffiGO "), (MUTED, "— "), (TEXT, "GenAI apps + MLOps on GCP/AWS/Azure")],
        [(CY, "focus"), (MUTED, ": "), (VI, "["), (TEXT, "causal inference, PGMs, grounded GenAI, neuro-symbolic"), (VI, "]")],
        [(CY, "now"), (MUTED, ": "), (TEXT, "visual hallucinations in multimodal reasoning traces")],
        [(CY, "rule"), (MUTED, ": "), (AM, '"every claim traced back to its evidence"')],
        [(CY, "open_to"), (MUTED, ": "), (VI, "["), (TEXT, "werkstudent (thesis-compatible), full-time 2027"), (VI, "]")],
    ]
    H = 72 + len(lines) * 27 + 34
    out = []
    for i, segs in enumerate(lines):
        y = 74 + i * 27
        ts = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for c, t in segs)
        num = f'<text class="mono ln" x="26" y="{y}" font-size="12" fill="{LINE}" style="animation-delay:{0.25 + i*0.45:.2f}s">{i+1:02d}</text>'
        out.append(num + f'<text class="mono ln" x="58" y="{y}" font-size="14.5" style="animation-delay:{0.25 + i*0.45:.2f}s">{ts}</text>')
    yc = 74 + len(lines) * 27
    body = f'''{frame(H)}
<rect x="0.5" y="0.5" width="{W-1}" height="36" rx="14" fill="{PANEL2}"/><rect x="0.5" y="22" width="{W-1}" height="15" fill="{PANEL2}"/>
<line x1="0" y1="37" x2="{W}" y2="37" stroke="{LINE}"/>
<circle cx="24" cy="19" r="6" fill="{CY}"/><circle cx="44" cy="19" r="6" fill="{VI}"/><circle cx="64" cy="19" r="6" fill="{AM}"/>
<text class="mono" x="{W/2}" y="23" font-size="12" fill="{MUTED}" text-anchor="middle">kai@darmstadt: ~/about</text>
{chr(10).join(out)}
<text class="mono ln" x="58" y="{yc}" font-size="14.5" fill="{CY}" style="animation-delay:{0.25 + len(lines)*0.45:.2f}s">❯ <tspan fill="{AM}" class="blink">█</tspan></text>
{runner(H, CY, dur=9)}'''
    style = '''.ln{opacity:0;animation:ln .5s ease-out forwards;} @keyframes ln{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
.blink{animation:bl 1s infinite steps(1);} @keyframes bl{50%{opacity:0}}'''
    save("about.svg", svg(H, body, style=style))


# =====================================================================
# PROJECT CARDS
# =====================================================================
def chip(x, y, text, color):
    w = len(text) * 7.9 + 22
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.45"/>'
            f'<text class="mono" x="{x + 11}" y="{y + 17.5}" font-size="12.5" fill="{color}">{esc(text)}</text>', w)


def card(name, num, kind, color, title, desc, chips, stack, visual):
    H = 236
    parts = [frame(H, color)]
    parts.append(f'<rect x="0" y="22" width="4" height="{H-44}" rx="2" fill="{color}" filter="url(#glow)"/>')
    parts.append(f'<text class="mono" x="36" y="44" font-size="12" letter-spacing="2" fill="{color}">{num} / {esc(kind)}</text>')
    parts.append(f'<text x="36" y="84" font-size="32" font-weight="800" fill="{TEXT}">{esc(title)}</text>')
    for i, d in enumerate(desc):
        parts.append(f'<text x="36" y="{114 + i*21}" font-size="14.5" fill="{SOFT}">{esc(d)}</text>')
    x = 36
    yc = 114 + len(desc) * 21 - 2
    for c in chips:
        s, w = chip(x, yc, c, color)
        parts.append(s); x += w + 10
    parts.append(f'<text class="mono" x="36" y="{H-22}" font-size="12" fill="{MUTED}">{esc(stack)}</text>')
    parts.append(f'<rect x="556" y="20" width="324" height="{H-40}" rx="10" fill="{BG}" stroke="{LINE}"/>')
    parts.append(visual)
    parts.append(runner(H, color, dur=8))
    parts.append(f'<text class="mono" x="532" y="{H-22}" font-size="12" fill="{color}" text-anchor="end">view repo ↗</text>')
    style = '''.blink{animation:bl 1s infinite steps(1);} @keyframes bl{50%{opacity:0}}'''
    save(f"card-{name}.svg", svg(H, "\n".join(parts), style=style))


def vis_adfontes():
    c = CY
    rows = [("claim_1", "chunk#12", True), ("claim_2", "chunk#47", True), ("claim_3", "—", False)]
    s = [f'<text class="mono" x="574" y="44" font-size="11" fill="{MUTED}">verify(claim) <tspan fill="{c}">→</tspan> 3 checks</text>']
    D = 6
    for r, (cl, ch, ok) in enumerate(rows):
        y = 68 + r * 42
        s.append(f'<text class="mono" x="574" y="{y}" font-size="12" fill="{TEXT}">{cl} <tspan fill="{MUTED}">→</tspan> <tspan fill="{VI if ok else MUTED}">{esc(ch)}</tspan></text>')
        for k, lab in enumerate(["struct", "NLI", "num"]):
            px = 574 + k * 66
            t0 = (r * 3 + k) * 0.45
            col = c if ok else AM
            mark = "✓" if ok else "✗"
            s.append(f'<g opacity="0.18"><animate attributeName="opacity" values="0.18;0.18;1;1;0.18" keyTimes="0;{t0/D:.3f};{(t0+0.2)/D:.3f};0.92;1" dur="{D}s" repeatCount="indefinite"/>'
                     f'<rect x="{px}" y="{y+8}" width="58" height="20" rx="10" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>'
                     f'<text class="mono" x="{px+29}" y="{y+22}" font-size="11" fill="{col}" text-anchor="middle">{mark} {lab}</text></g>')
        if not ok:
            t0 = (r * 3 + 2) * 0.45 + 0.3
            s.append(f'<text class="mono" x="776" y="{y+22}" font-size="11" font-weight="700" fill="{AM}" opacity="0">FLAGGED'
                     f'<animate attributeName="opacity" values="0;0;1;0.3;1;0" keyTimes="0;{t0/D:.3f};{(t0+0.15)/D:.3f};{(t0+0.5)/D:.3f};0.92;1" dur="{D}s" repeatCount="indefinite"/></text>')
    s.append(f'<text class="mono" x="574" y="204" font-size="11" fill="{MUTED}">metric: <tspan fill="{c}">unsupported claims / 100 answers</tspan></text>')
    return "\n".join(s)


def vis_pharma():
    c = VI
    cols = {"demo": 600, "indic.": 678, "drug": 756, "event": 840}
    s = []
    for lab, x in cols.items():
        s.append(f'<text class="mono" x="{x}" y="44" font-size="10.5" fill="{MUTED}" text-anchor="middle">{lab}</text>')
        s.append(f'<line x1="{x}" y1="54" x2="{x}" y2="186" stroke="{LINE}" stroke-dasharray="2 4"/>')
    N = {"a1": (600, 82), "a2": (600, 150), "b1": (678, 100), "b2": (678, 165),
         "c1": (756, 78), "c2": (756, 132), "c3": (756, 176), "d1": (840, 98), "d2": (840, 160)}
    E = [("a1", "b1"), ("a2", "b2"), ("a1", "c2"), ("b1", "c1"), ("b2", "c3"), ("b1", "c2"), ("c2", "d2"), ("c3", "d2")]
    for a, b in E:
        (x1, y1), (x2, y2) = N[a], N[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{VI}" stroke-opacity="0.35" stroke-width="1.3"/>')
    # spurious confounded edge that gets pruned
    (x1, y1), (x2, y2) = N["c1"], N["d2"]
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AM}" stroke-width="1.5" stroke-dasharray="4 4">'
             f'<animate attributeName="opacity" values="0.9;0.9;0;0;0.9" keyTimes="0;0.35;0.5;0.95;1" dur="7s" repeatCount="indefinite"/></line>')
    s.append(f'<text class="mono" x="790" y="122" font-size="10" fill="{AM}">confounded<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.35;0.5;0.95;1" dur="7s" repeatCount="indefinite"/></text>')
    # highlighted causal edge
    (x1, y1), (x2, y2) = N["c1"], N["d1"]
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CY}" stroke-width="2.4" stroke-dasharray="5 6" filter="url(#glow)">'
             f'<animate attributeName="stroke-dashoffset" values="22;0" dur="1s" repeatCount="indefinite"/></line>')
    s.append(f'<circle r="3" fill="{CY}" filter="url(#glow)"><animateMotion dur="1.6s" repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/></circle>')
    for k, (x, y) in N.items():
        col = CY if k in ("c1", "d1") else VI
        s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BG}" stroke="{col}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="2.5" fill="{col}"/>')
    s.append(f'<text class="mono" x="574" y="206" font-size="11" fill="{TEXT}">rosuvastatin <tspan fill="{CY}">→</tspan> myalgia  <tspan fill="{CY}">✓ SIDER</tspan></text>')
    return "\n".join(s)


def vis_evidentia():
    labs = ["URTI", "Pneum.", "Bronch.", "Influ.", "GERD"]
    steps = [[.2, .2, .2, .2, .2], [.24, .26, .1, .35, .05], [.18, .38, .14, .28, .02], [.07, .74, .09, .09, .01]]
    seq = [0, 1, 2, 3, 3, 0]
    kt = "0;0.22;0.44;0.66;0.92;1"
    base, maxh = 178, 112
    s = []
    for i, lab in enumerate(labs):
        x = 584 + i * 58
        hs = [steps[j][i] * maxh for j in seq]
        col = AM if i == 1 else (VI if i % 2 else CY)
        op = "1" if i == 1 else "0.55"
        s.append(f'<rect x="{x}" width="36" rx="4" fill="{col}" fill-opacity="{op}" y="{base-hs[0]:.1f}" height="{hs[0]:.1f}">'
                 f'<animate attributeName="height" values="{";".join(f"{h:.1f}" for h in hs)}" keyTimes="{kt}" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines="{";".join(["0.4 0 0.2 1"]*5)}"/>'
                 f'<animate attributeName="y" values="{";".join(f"{base-h:.1f}" for h in hs)}" keyTimes="{kt}" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines="{";".join(["0.4 0 0.2 1"]*5)}"/></rect>')
        s.append(f'<text class="mono" x="{x+18}" y="{base+16}" font-size="10" fill="{MUTED}" text-anchor="middle">{lab}</text>')
    s.append(f'<line x1="576" y1="{base}" x2="862" y2="{base}" stroke="{LINE}"/>')
    ev = ["+ fever", "+ cough", "+ chest pain"]
    x = 574
    for k, e in enumerate(ev):
        vals = ["0"] * 6
        for j in range(6):
            if 1 + k <= seq[j] and j < 5:
                vals[j] = "1"
        w = len(e) * 7 + 16
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{kt}" dur="8s" repeatCount="indefinite"/>'
                 f'<rect x="{x}" y="34" width="{w}" height="20" rx="10" fill="{AM}" fill-opacity="0.12" stroke="{AM}" stroke-opacity="0.6"/>'
                 f'<text class="mono" x="{x+8}" y="48" font-size="11" fill="{AM}">{e}</text></g>')
        x += w + 8
    s.append(f'<text class="mono" x="574" y="212" font-size="11" fill="{MUTED}">P(dx | evidence) · every shift attributed</text>')
    return "\n".join(s)


def vis_fons():
    s = [f'<rect x="580" y="36" width="140" height="160" rx="6" fill="{PANEL2}" stroke="{LINE}"/>',
         f'<text class="mono" x="592" y="56" font-size="10.5" fill="{CY}">GDPR · Art. 6</text>']
    ys = [72, 84, 96, 112, 124, 136, 152, 164, 176]
    for i, y in enumerate(ys):
        w = [110, 96, 104, 112, 88, 100, 108, 92, 70][i]
        s.append(f'<rect x="592" y="{y}" width="{w}" height="5" rx="2.5" fill="{SOFT}" fill-opacity="0.25"/>')
    # scanning highlight that lands on paragraph (1)(a)
    s.append(f'<rect x="586" width="128" height="22" rx="4" fill="{AM}" fill-opacity="0.16" stroke="{AM}" stroke-opacity="0.7" y="66">'
             f'<animate attributeName="y" values="66;104;146;105;105;66" keyTimes="0;0.15;0.3;0.42;0.92;1" dur="7s" repeatCount="indefinite"/></rect>')
    s.append(f'<path d="M716 116 C 740 116, 740 84, 760 84" stroke="{AM}" stroke-width="1.5" stroke-dasharray="3 4"/>')
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.42;0.5;0.92;1" dur="7s" repeatCount="indefinite"/>'
             f'<rect x="740" y="60" width="128" height="50" rx="8" fill="{CY}" fill-opacity="0.08" stroke="{CY}" stroke-opacity="0.6"/>'
             f'<text class="mono" x="750" y="80" font-size="10.5" fill="{TEXT}">"consent is a</text>'
             f'<text class="mono" x="750" y="96" font-size="10.5" fill="{TEXT}">lawful basis" <tspan fill="{CY}">✓</tspan></text></g>')
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.62;0.92;1" dur="7s" repeatCount="indefinite"/>'
             f'<rect x="740" y="126" width="128" height="50" rx="8" fill="{AM}" fill-opacity="0.08" stroke="{AM}" stroke-opacity="0.6"/>'
             f'<text class="mono" x="750" y="146" font-size="10.5" fill="{TEXT}">"Art. 6(7)..."</text>'
             f'<text class="mono" x="750" y="162" font-size="10.5" fill="{AM}">✗ not entailed</text></g>')
    s.append(f'<text class="mono" x="574" y="212" font-size="11" fill="{MUTED}">cite → retrieve → NLI-verify</text>')
    return "\n".join(s)


# =====================================================================
# STACK
# =====================================================================
def stack():
    groups = [
        ("MODELS & ML", CY, ["PyTorch", "Transformers", "TRL · PEFT", "QLoRA", "causal-learn", "sentence-transformers"]),
        ("SERVING & DATA", VI, ["FastAPI", "Docker", "llama.cpp", "ChromaDB", "pytest", "Jupyter"]),
        ("CLOUD & WEB", AM, ["GCP", "AWS", "Azure", "React", "TypeScript", "Vite"]),
    ]
    parts = []
    y = 40
    idx = 0
    for gname, col, items in groups:
        parts.append(f'<text class="mono" x="28" y="{y+18}" font-size="11.5" letter-spacing="2" fill="{col}">{esc(gname)}</text>')
        x = 200
        for it in items:
            w = len(it) * 8.4 + 30
            if x + w > W - 28:
                x = 200; y += 38
            d = idx * 0.18
            parts.append(f'<g class="pill" style="animation-delay:{d:.2f}s">'
                         f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="0.4">'
                         f'<animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="3.6s" begin="{d:.2f}s" repeatCount="indefinite"/></rect>'
                         f'<circle cx="{x+14}" cy="{y+14}" r="3" fill="{col}"/>'
                         f'<text class="mono" x="{x+24}" y="{y+18.5}" font-size="13" fill="{TEXT}">{esc(it)}</text></g>')
            x += w + 10
            idx += 1
        y += 48
    parts.append(f'<line x1="28" y1="{y+2}" x2="{W-28}" y2="{y+2}" stroke="{LINE}"/>')
    y += 30
    parts.append(f'<text class="mono" x="28" y="{y}" font-size="12.5" fill="{MUTED}"><tspan fill="{CY}">core ▸</tspan> causal discovery · Bayesian networks · RAG verification · RLHF/DPO · <tspan fill="{VI}">CLIP · BLIP-2 · LLaVA</tspan></text>')
    H = y + 26
    style = '''.pill{opacity:0;animation:pin .6s ease-out forwards;} @keyframes pin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}'''
    body = frame(H) + "\n" + "\n".join(parts) + "\n" + runner(H, AM, dur=10)
    save("stack.svg", svg(H, body, style=style))


# =====================================================================
# CURRENTLY
# =====================================================================
def now():
    rows = [
        (CY, "RESEARCH", "Visual hallucinations in multimodal reasoning traces", "TU Darmstadt · MAI project lab"),
        (VI, "TRAINING", "ad-fontes DPO stage: base vs. tuned faithfulness", "QLoRA · TRL"),
        (AM, "OPEN TO", "Werkstudent ML/AI roles, full-time from 2027", "thesis-compatible · Darmstadt / remote"),
    ]
    parts = []
    y = 46
    for i, (col, lab, main, sub) in enumerate(rows):
        parts.append(f'<circle cx="34" cy="{y-5}" r="5" fill="{col}" filter="url(#glow)"/>'
                     f'<circle cx="34" cy="{y-5}" r="5" fill="none" stroke="{col}"><animate attributeName="r" values="5;14" dur="2s" begin="{i*0.6}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.8;0" dur="2s" begin="{i*0.6}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<text class="mono" x="56" y="{y}" font-size="12" letter-spacing="2" fill="{col}">{lab}</text>')
        parts.append(f'<text x="170" y="{y}" font-size="16" font-weight="600" fill="{TEXT}">{esc(main)}</text>')
        parts.append(f'<text class="mono" x="170" y="{y+20}" font-size="11.5" fill="{MUTED}">{esc(sub)}</text>')
        parts.append(f'<rect x="170" y="{y+30}" width="{W-200}" height="3" rx="1.5" fill="{LINE}"/>')
        parts.append(f'<rect y="{y+30}" width="140" height="3" rx="1.5" fill="{col}" filter="url(#glow)" x="170">'
                     f'<animate attributeName="x" values="170;{W-170};170" dur="{4+i}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></rect>')
        y += 66
    H = y - 6
    body = frame(H) + "\n" + "\n".join(parts) + "\n" + runner(H, VI, dur=9)
    save("now.svg", svg(H, body))


# =====================================================================
# FOOTER
# =====================================================================
def footer():
    H = 130
    def wave(amp, period, phase, y0):
        pts = []
        for x in range(-period, W + period * 2, 6):
            pts.append(f"{x},{y0 + amp*math.sin((x/period)*2*math.pi + phase):.1f}")
        return "M" + " L".join(pts)
    parts = []
    for (col, amp, per, ph, dur) in [(CY, 10, 300, 0, 7), (VI, 14, 300, 2.1, 9), (AM, 7, 300, 4.2, 6)]:
        parts.append(f'<path d="{wave(amp, per, ph, 58)}" stroke="{col}" stroke-opacity="0.65" stroke-width="1.6">'
                     f'<animateTransform attributeName="transform" type="translate" values="0 0;-{per} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    parts.append(f'<text class="mono" x="{W/2}" y="108" font-size="13" fill="{MUTED}" text-anchor="middle"><tspan fill="{CY}">ad</tspan> <tspan fill="{VI}">fontes</tspan> <tspan fill="{LINE}">·</tspan> back to the sources <tspan fill="{AM}">●</tspan></text>')
    defs = f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.15" stop-color="#fff"/><stop offset="0.85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
    body = frame(H) + f'<g mask="url(#m)">' + "\n".join(parts[:3]) + "</g>\n" + parts[3]
    save("footer.svg", svg(H, body, defs))


if __name__ == "__main__":
    header(); about(); stack(); now(); footer()
    section("about", "about", CY, "01")
    section("work", "featured_work", VI, "02")
    section("stack", "toolkit", AM, "03")
    section("now", "currently", CY, "04")
    card("adfontes", "01", "RAG · CLAIM VERIFICATION · DPO", CY, "ad-fontes",
         ["A portfolio assistant that isn't allowed to exaggerate.",
          "Every claim must cite a chunk and pass 3 checks."],
         ["93.9% hit@6", "MRR 0.74", "DPO in progress"],
         "Qwen2.5-1.5B · QLoRA · TRL · ChromaDB · FastAPI", vis_adfontes())
    card("pharmacausal", "02", "CAUSAL DISCOVERY · PHARMACOVIGILANCE", VI, "pharmacausal",
         ["PC + FCI causal discovery on FDA adverse-event reports,",
          "with time-ordered tiers so confounders get pruned."],
         ["422k reports", "67% FCI precision", "SIDER-validated"],
         "causal-learn · pandas · pytest", vis_pharma())
    card("evidentia", "03", "BAYESIAN NETWORKS · EXPLAINABILITY", AM, "evidentia",
         ["An 895-node Bayesian-network symptom checker where",
          "every probability shift is traced to its evidence."],
         ["ECE 0.0036", "134,529 test patients"],
         "Python · FastAPI · React · Cytoscape", vis_evidentia())
    card("fonsiuris", "04", "LEGAL RAG · NLI VERIFICATION", CY, "fons-iuris",
         ["GDPR & EU AI Act Q&A that cites the exact paragraph",
          "and flags any claim its source doesn't entail."],
         ["EUR-Lex corpus", "NLI-verified"],
         "FastAPI · Chroma · Transformers · React", vis_fons())
    print("ok", sorted(os.listdir(OUT)))
