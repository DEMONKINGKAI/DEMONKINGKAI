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
VI = "#FF3B5C"   # crimson - models / structure
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


def frame(h, accent=None, rx=4):
    stroke = accent if accent else LINE
    op = "0.35" if accent else "1"
    return f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="{rx}" fill="{PANEL}" stroke="{stroke}" stroke-opacity="{op}"/>'


def runner(h, color, rx=4, dur=7):
    """A light segment that travels around the card border."""
    return (f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{color}" '
            f'stroke-width="1.6" pathLength="100" stroke-dasharray="10 90" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" values="0;-100" dur="{dur}s" repeatCount="indefinite"/></rect>')


# =====================================================================
# HEADER
# =====================================================================

GLYPHS = {
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
}


def pixel_kai(x0=48, y0=80, step=16, px=14):
    import random
    rnd = random.Random(7)
    rows = {r: {"shadow": [], "main": [], "cy": [], "cr": []} for r in range(7)}
    col_off = 0
    for ch in "KAI":
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit != "1":
                    continue
                cc = col_off + c
                x, y = x0 + cc * step, y0 + r * step
                pop = 0.35 + cc * 0.06 + r * 0.015
                sweep = 3.0 + cc * 0.07 + r * 0.03
                R = rows[r]
                R["shadow"].append(f'<rect class="pxs" x="{x+3}" y="{y+3}" width="{px}" height="{px}" fill="{VI}" style="animation-delay:{pop+0.15:.2f}s"/>')
                R["main"].append(f'<rect class="px" x="{x}" y="{y}" width="{px}" height="{px}" fill="{TEXT}" style="animation-delay:{pop:.2f}s,{sweep:.2f}s"/>')
                R["cy"].append(f'<rect x="{x-6}" y="{y}" width="{px}" height="{px}" fill="{CY}"/>')
                R["cr"].append(f'<rect x="{x+6}" y="{y}" width="{px}" height="{px}" fill="{VI}"/>')
        col_off += len(g[0]) + 1
    width = col_off * step
    out = []
    # rgb split layers (flash only during glitch)
    out.append('<g class="gsplit-c">' + "".join(x for r in rows.values() for x in r["cy"]) + "</g>")
    out.append('<g class="gsplit-r">' + "".join(x for r in rows.values() for x in r["cr"]) + "</g>")
    # each row tears independently
    keyf = []
    for r, R in rows.items():
        d1 = rnd.choice([-1, 1]) * rnd.randint(6, 22)
        d2 = rnd.choice([-1, 1]) * rnd.randint(4, 14)
        d3 = rnd.choice([-1, 1]) * rnd.randint(2, 30)
        keyf.append(f"@keyframes tear{r}{{0%,86%,100%{{transform:none}} 87%{{transform:translateX({d1}px)}} "
                    f"89%{{transform:translateX({d2}px)}} 90%{{transform:none}} 95%{{transform:translateX({d3}px)}} 96%{{transform:none}}}}")
        out.append(f'<g class="row" style="animation-name:tear{r}">' + "".join(R["shadow"]) + "".join(R["main"]) + "</g>")
    # noise pixels
    noise = []
    for i in range(14):
        nx = x0 + rnd.randint(-2, col_off + 2) * step
        ny = y0 + rnd.randint(-1, 7) * step
        col = rnd.choice([CY, VI, AM, TEXT])
        sz = rnd.choice([px // 2, px, px])
        when = rnd.choice(["n1", "n2"])
        noise.append(f'<rect class="{when}" x="{nx}" y="{ny}" width="{sz}" height="{sz}" fill="{col}"/>')
    out.append("".join(noise))
    # dark slice bar that cuts through
    out.append(f'<rect class="gbar" x="{x0-10}" y="{y0 + 2*step}" width="{width+30}" height="{step//2}" fill="{BG}"/>')
    out.append(f'<rect class="gbar2" x="{x0-10}" y="{y0 + 5*step}" width="{width+30}" height="3" fill="{CY}"/>')
    cx = x0 + col_off * step
    out.append(f'<g class="pxc"><rect x="{cx}" y="{y0 + 5*step}" width="{px}" height="{px}" fill="{AM}"/>'
               f'<rect x="{cx}" y="{y0 + 6*step}" width="{px}" height="{px}" fill="{AM}"/>'
               f'<rect x="{cx+step}" y="{y0 + 6*step}" width="{px}" height="{px}" fill="{AM}"/></g>')
    GLITCH_CSS[0] = "\n".join(keyf)
    return "\n".join(out)


GLITCH_CSS = [""]

def header():
    H = 420
    # ---------- typing helpers ----------
    def typer(n, cw, x0, dur, start_frac, hold_to):
        """discrete reveal widths: hidden until start_frac, types n chars, holds until hold_to, then hides."""
        vals, kts = ["0"], ["0"]
        type_span = 0.12
        for i in range(n + 1):
            vals.append(f"{i*cw:.1f}"); kts.append(f"{start_frac + type_span*i/n:.4f}")
        vals.append(f"{n*cw:.1f}"); kts.append(f"{hold_to:.4f}")
        vals.append("0"); kts.append("1")
        return vals, kts

    cmd = "whoami"
    tag = "I build AI that shows its work."
    D = 12  # master loop seconds
    cv, ck = typer(len(cmd), 9.0, 0, D, 0.02, 0.97)
    tv, tk = typer(len(tag), 10.8, 0, D, 0.30, 0.97)
    cx_vals = [f"{82 + float(v):.1f}" for v in cv]
    tx_vals = [f"{48 + float(v):.1f}" for v in tv]

    # ---------- do(x) graph surgery ----------
    GD = 10  # loop seconds
    P = {"Z": (690, 100), "X": (566, 236), "Y": (820, 236)}
    hs = 20  # node half size

    def seg(p, q, pad=hs + 8):
        (x1, y1), (x2, y2) = P[p], P[q]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        return x1 + ux * pad, y1 + uy * pad, x2 - ux * pad, y2 - uy * pad

    def vis(values, kt="0;0.40;0.44;0.95;1"):
        return f'<animate attributeName="opacity" values="{values}" keyTimes="{kt}" dur="{GD}s" repeatCount="indefinite"/>'

    orb = []
    orb.append(f'<rect x="488" y="34" width="390" height="286" rx="2" fill="{BG}" fill-opacity="0.55" stroke="{LINE}"/>')
    orb.append(f'<text class="mono" x="506" y="58" font-size="11" fill="{MUTED}">causal_graph.surgery()</text>')
    orb.append(f'<circle cx="858" cy="54" r="4" fill="{VI}"><animate attributeName="fill" values="{CY};{CY};{VI};{VI};{CY}" keyTimes="0;0.40;0.44;0.95;1" dur="{GD}s" repeatCount="indefinite"/></circle>')
    # edges ---------------------------------------------------------
    def edge(p, q, col, width=2, extra=""):
        x1, y1, x2, y2 = seg(p, q)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return (f'<g {extra}><line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{width}"/>'
                f'<polygon points="0,-5 10,0 0,5" fill="{col}" transform="translate({x2:.1f},{y2:.1f}) rotate({ang:.1f})"/></g>')

    def particles(p, q, col, dur, n=2, gate=None):
        x1, y1, x2, y2 = seg(p, q)
        out = []
        for k in range(n):
            out.append(f'<rect width="6" height="6" x="-3" y="-3" fill="{col}" filter="url(#glow)">'
                       f'<animateMotion dur="{dur}s" begin="-{k*dur/n:.2f}s" repeatCount="indefinite" path="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/></rect>')
        body = "".join(out)
        return f'<g>{gate}{body}</g>' if gate else body

    # Z -> Y : confounder path, always on
    orb.append(edge("Z", "Y", CY, 1.6, 'opacity="0.55"'))
    orb.append(particles("Z", "Y", CY, 1.8))
    # Z -> X : present, flashes, then cut
    orb.append(edge("Z", "X", CY, 1.6, f'opacity="0.55">{vis("0.55;0.55;0;0;0.55")}<g') + "</g>")
    orb.append(edge("Z", "X", VI, 2.4, f'opacity="0">{vis("0;0;1;0;0", "0;0.40;0.42;0.46;1")}<g') + "</g>")
    zx = seg("Z", "X")
    orb.append(f'<line x1="{zx[0]:.1f}" y1="{zx[1]:.1f}" x2="{zx[2]:.1f}" y2="{zx[3]:.1f}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 6" opacity="0">{vis("0;0;0.6;0.6;0")}</line>')
    orb.append(particles("Z", "X", CY, 1.4, 2, f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.40;0.42;0.97;1" dur="{GD}s" repeatCount="indefinite"/>'))
    # cut mark
    mx, my = (zx[0] + zx[2]) / 2, (zx[1] + zx[3]) / 2
    orb.append(f'<g opacity="0">{vis("0;0;1;1;0")}'
               f'<line x1="{mx-11}" y1="{my-11}" x2="{mx+11}" y2="{my+11}" stroke="{VI}" stroke-width="3"/>'
               f'<line x1="{mx-11}" y1="{my+11}" x2="{mx+11}" y2="{my-11}" stroke="{VI}" stroke-width="3"/>'
               f'<text class="mono" x="{mx-74}" y="{my-12}" font-size="10.5" fill="{VI}">edge cut</text></g>')
    # X -> Y : normal, then isolated effect in amber
    orb.append(edge("X", "Y", CY, 1.6, f'opacity="0.55">{vis("0.55;0.55;0.15;0.15;0.55")}<g') + "</g>")
    orb.append(edge("X", "Y", AM, 2.6, f'opacity="0">{vis("0;0;1;1;0")}<g') + "</g>")
    orb.append(particles("X", "Y", CY, 1.6, 2, f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.40;0.44;0.95;1" dur="{GD}s" repeatCount="indefinite"/>'))
    orb.append(particles("X", "Y", AM, 0.8, 3, f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.44;0.46;0.95;1" dur="{GD}s" repeatCount="indefinite"/>'))
    # nodes ----------------------------------------------------------
    names = {"Z": "confounder", "X": "treatment", "Y": "outcome"}
    for k, (x, y) in P.items():
        orb.append(f'<rect x="{x-hs+3}" y="{y-hs+3}" width="{2*hs}" height="{2*hs}" fill="{VI}" opacity="0.5"/>')
        orb.append(f'<rect x="{x-hs}" y="{y-hs}" width="{2*hs}" height="{2*hs}" fill="{PANEL2}" stroke="{CY}" stroke-width="2"/>')
        orb.append(f'<text class="mono" x="{x}" y="{y+6}" font-size="17" font-weight="700" fill="{TEXT}" text-anchor="middle">{k}</text>')
        if k == "Z":
            orb.append(f'<text class="mono" x="{x+hs+10}" y="{y+4}" font-size="10.5" fill="{MUTED}">{names[k]}</text>')
        else:
            orb.append(f'<text class="mono" x="{x}" y="{y+hs+20}" font-size="10.5" fill="{MUTED}" text-anchor="middle">{names[k]}</text>')
    # X becomes the intervened node
    x, y = P["X"]
    orb.append(f'<g opacity="0">{vis("0;0;1;1;0")}'
               f'<rect x="{x-hs}" y="{y-hs}" width="{2*hs}" height="{2*hs}" fill="{AM}"/>'
               f'<text class="mono" x="{x}" y="{y+6}" font-size="17" font-weight="700" fill="{BG}" text-anchor="middle">X</text>'
               f'<rect x="{x-hs}" y="{y-hs}" width="{2*hs}" height="{2*hs}" fill="none" stroke="{AM}" stroke-width="2">'
               f'<animate attributeName="x" values="{x-hs};{x-hs-16}" dur="1.2s" repeatCount="indefinite"/>'
               f'<animate attributeName="y" values="{y-hs};{y-hs-16}" dur="1.2s" repeatCount="indefinite"/>'
               f'<animate attributeName="width" values="{2*hs};{2*hs+32}" dur="1.2s" repeatCount="indefinite"/>'
               f'<animate attributeName="height" values="{2*hs};{2*hs+32}" dur="1.2s" repeatCount="indefinite"/>'
               f'<animate attributeName="stroke-opacity" values="0.9;0" dur="1.2s" repeatCount="indefinite"/></rect>'
               f'<rect x="{x-52}" y="{y-hs-34}" width="60" height="20" fill="{AM}" fill-opacity="0.12" stroke="{AM}"/>'
               f'<text class="mono" x="{x-22}" y="{y-hs-20}" font-size="12" font-weight="700" fill="{AM}" text-anchor="middle">do(x)</text></g>')
    # Y lights up with the isolated effect
    x, y = P["Y"]
    orb.append(f'<rect x="{x-hs}" y="{y-hs}" width="{2*hs}" height="{2*hs}" fill="none" stroke="{AM}" stroke-width="2.5" filter="url(#glow)" opacity="0">{vis("0;0;0;1;0", "0;0.44;0.5;0.95;1")}</rect>')
    # caption ---------------------------------------------------------
    orb.append(f'<text class="mono" x="506" y="304" font-size="13" fill="{TEXT}" opacity="1">{vis("1;1;0;0;1")}<tspan fill="{MUTED}">observe </tspan>P(y <tspan fill="{CY}">|</tspan> x)</text>')
    orb.append(f'<text class="mono" x="506" y="304" font-size="13" fill="{TEXT}" opacity="0">{vis("0;0;1;1;0")}<tspan fill="{MUTED}">intervene </tspan>P(y <tspan fill="{AM}">|</tspan> <tspan fill="{AM}">do(x)</tspan>)</text>')

    # ---------- stats strip ----------
    stats = [(CY, "422k", "FDA reports, causal discovery"),
             (VI, "895", "node Bayesian network, ECE 0.0036"),
             (AM, "99%", "precision, decision extraction")]
    st = [f'<line x1="0" y1="330" x2="{W}" y2="330" stroke="{LINE}"/>']
    cw = W / 3
    for i, (col, big, small) in enumerate(stats):
        x = i * cw + 48
        if i:
            st.append(f'<line x1="{i*cw:.0f}" y1="344" x2="{i*cw:.0f}" y2="404" stroke="{LINE}"/>')
        st.append(f'<g class="stat" style="animation-delay:{1.6 + i*0.25:.2f}s">'
                  f'<text class="mono" x="{x}" y="378" font-size="30" font-weight="700" fill="{col}">{big}</text>'
                  f'<text class="mono" x="{x}" y="398" font-size="11" fill="{MUTED}">{esc(small)}</text></g>')

    defs = f'''
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#ffffff" stroke-opacity="0.035"/></pattern>
<radialGradient id="g1" cx="0.12" cy="0.15" r="0.6"><stop offset="0" stop-color="{CY}" stop-opacity="0.14"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="0.78" cy="0.4" r="0.45"><stop offset="0" stop-color="{VI}" stop-opacity="0.13"/><stop offset="1" stop-color="{VI}" stop-opacity="0"/></radialGradient>
<radialGradient id="coreglow"><stop offset="0" stop-color="{AM}" stop-opacity="0.35"/><stop offset="1" stop-color="{AM}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="0.5" stop-color="{CY}" stop-opacity="0.06"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
<linearGradient id="namegrad" x1="44" y1="0" x2="310" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
<stop offset="0" stop-color="{CY}"/><stop offset="0.5" stop-color="{VI}"/><stop offset="1" stop-color="{AM}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;266 0;0 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="namegrad2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CY}"/><stop offset="0.5" stop-color="{VI}"/><stop offset="1" stop-color="{AM}"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="4"/></clipPath>
<clipPath id="cmdclip"><rect x="82" y="46" height="24" width="0"><animate attributeName="width" values="{';'.join(cv)}" keyTimes="{';'.join(ck)}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="tagclip"><rect x="48" y="252" height="28" width="0"><animate attributeName="width" values="{';'.join(tv)}" keyTimes="{';'.join(tk)}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'''
    style = '''
.g1{animation:gl1 5s infinite steps(1);} .g2{animation:gl2 5s infinite steps(1);}
@keyframes gl1{0%,88%,100%{opacity:0;transform:translate(0,0)} 89%{opacity:.85;transform:translate(-4px,1px)} 91%{opacity:.6;transform:translate(3px,-1px)} 93%{opacity:0}}
@keyframes gl2{0%,88%,100%{opacity:0;transform:translate(0,0)} 90%{opacity:.85;transform:translate(4px,-1px)} 92%{opacity:.6;transform:translate(-3px,1px)} 94%{opacity:0}}
.blink{animation:bl 1s infinite steps(1);} @keyframes bl{50%{opacity:0}}
.rgb{opacity:0;animation:fadein 1s ease-out 1.9s forwards, rgbj 6s 3s infinite steps(1);}
@keyframes rgbj{0%,90%,100%{transform:none} 91%{transform:translate(-3px,0)} 93%{transform:translate(4px,1px)} 95%{transform:none}}
.slice{opacity:0;animation:sl 6s 3s infinite steps(1);} @keyframes sl{0%,90%,100%{opacity:0;transform:none} 91%{opacity:1;transform:translateY(0)} 93%{opacity:1;transform:translateY(26px)} 95%{opacity:0}}
.slice2{animation:sl2 6s 3s infinite steps(1);} @keyframes sl2{0%,91%,100%{opacity:0} 92%{opacity:.7} 94%{opacity:0}}
.px{opacity:0;transform-box:fill-box;transform-origin:center;animation:pxin .35s cubic-bezier(.3,1.6,.5,1) forwards, pxsw 5s infinite;}
@keyframes pxin{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
@keyframes pxsw{0%,100%{fill:#E8EAF2} 3%{fill:#00E5FF} 7%{fill:#E8EAF2}}
.pxs{opacity:0;animation:pxsh .4s ease-out forwards;} @keyframes pxsh{to{opacity:.85}}
.pxc{opacity:0;animation:fadein .2s 1.6s forwards, pxb 1.2s 1.8s infinite steps(1);} @keyframes pxb{50%{opacity:0}}
.row{animation-duration:4.5s;animation-delay:2.4s;animation-iteration-count:infinite;animation-timing-function:steps(1);}
.gsplit-c,.gsplit-r{opacity:0;animation:gsp 4.5s 2.4s infinite steps(1);}
@keyframes gsp{0%,86%,100%{opacity:0} 87%{opacity:.75} 90%{opacity:0} 95%{opacity:.6} 96%{opacity:0}}
.gsplit-r{animation-name:gspr;} @keyframes gspr{0%,86%,100%{opacity:0;transform:none} 88%{opacity:.75;transform:translate(3px,-2px)} 90%{opacity:0} 95%{opacity:.6;transform:translate(-2px,1px)} 96%{opacity:0}}
.n1{opacity:0;animation:n1 4.5s 2.4s infinite steps(1);} @keyframes n1{0%,86%,100%{opacity:0} 87%{opacity:1} 89%{opacity:0}}
.n2{opacity:0;animation:n2 4.5s 2.4s infinite steps(1);} @keyframes n2{0%,88%,100%{opacity:0} 89%{opacity:1} 90%{opacity:0} 95%{opacity:.9} 96%{opacity:0}}
.gbar{opacity:0;animation:gb 4.5s 2.4s infinite steps(1);} @keyframes gb{0%,87%,100%{opacity:0;transform:none} 88%{opacity:1} 89%{opacity:1;transform:translateY(32px)} 90%{opacity:0}}
.gbar2{opacity:0;animation:gb2 4.5s 2.4s infinite steps(1);} @keyframes gb2{0%,94%,100%{opacity:0} 95%{opacity:.8} 96%{opacity:0}}
.draw{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 2.2s ease-out .4s forwards;}
@keyframes draw{to{stroke-dashoffset:0}}
.fillin{opacity:0;animation:fadein 1s ease-out 1.9s forwards;}
.fade{opacity:0;animation:fadein .8s ease-out forwards;}
@keyframes fadein{to{opacity:1}}
.stat{opacity:0;animation:statin .8s ease-out forwards;}
@keyframes statin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'''
    out_frac = 0.16  # when whoami output appears
    body = f'''<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#g1)"/>
<rect width="{W}" height="{H}" fill="url(#g2)"/>
<rect x="0" y="-90" width="{W}" height="90" fill="url(#scan)"><animate attributeName="y" values="-90;{H}" dur="7s" repeatCount="indefinite"/></rect>

<text class="mono" x="48" y="64" font-size="15" fill="{CY}">❯</text>
<text class="mono" x="64" y="64" font-size="15" fill="{MUTED}">~</text>
<g clip-path="url(#cmdclip)"><text class="mono" x="82" y="64" font-size="15" fill="{TEXT}">{cmd}</text></g>
<rect y="50" width="8" height="17" fill="{AM}" class="blink"><animate attributeName="x" values="{';'.join(cx_vals)}" keyTimes="{';'.join(ck)}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/></rect>

{pixel_kai()}
<text class="fade" x="48" y="222" font-size="20" fill="{TEXT}" style="animation-delay:1.2s">Archit Sharma <tspan fill="{MUTED}">·</tspan> AI / ML Engineer</text>
<text class="mono fade" x="48" y="243" font-size="12.5" fill="{MUTED}" style="animation-delay:1.4s">MSc AI &amp; ML @ TU Darmstadt <tspan fill="{LINE}">│</tspan> ex-Product Engineer @ EffiGO</text>

<g clip-path="url(#tagclip)"><text class="mono" x="48" y="273" font-size="18" fill="{AM}">{esc(tag)}</text></g>
<rect y="257" width="10" height="21" fill="{AM}" class="blink"><animate attributeName="x" values="{';'.join(tx_vals)}" keyTimes="{';'.join(tk)}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/></rect>

<text class="mono fade" x="48" y="309" font-size="12" fill="{MUTED}" style="animation-delay:1.8s"><tspan fill="{CY}">●</tspan> open to werkstudent roles  <tspan fill="{VI}">●</tspan> darmstadt, de</text>

{chr(10).join(orb)}
{chr(10).join(st)}
<rect x="0" y="{H-3}" width="{W}" height="3" fill="url(#brand)"/>
</g>'''
    save("header.svg", svg(H, body, defs, style + GLITCH_CSS[0]))


# =====================================================================
# PIXEL FONT + GLITCH ENGINE (shared by titles and cards)
# =====================================================================
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    " ": ["000", "000", "000", "000", "000", "000", "000"],
}


def pixel_text(text, x0, y0, px, uid, fill=TEXT, shadow=VI, period=5.5, delay=1.2, pop=True, seed=1):
    """Pixel text with crimson drop shadow, pop-in and periodic glitch (row tear + rgb split + noise).
    Returns (svg, css, width)."""
    import random
    rnd = random.Random(seed)
    step = px + (max(1, px // 6) if px >= 8 else 0)
    so = max(2, px // 2)
    rows = {r: [] for r in range(7)}
    shad = {r: [] for r in range(7)}
    cy_l, cr_l = [], []
    col = 0
    for ch in text.upper():
        g = FONT[ch]
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit != "1":
                    continue
                x, y = x0 + (col + c) * step, y0 + r * step
                d = 0.1 + (col + c) * 0.025 + r * 0.01
                pcls = f' class="pp" style="animation-delay:{d:.2f}s"' if pop else ""
                shad[r].append(f'<rect x="{x + so}" y="{y + so}" width="{px}" height="{px}" fill="{shadow}" opacity="0.9"/>')
                rows[r].append(f'<rect{pcls} x="{x}" y="{y}" width="{px}" height="{px}" fill="{fill}"/>')
                cy_l.append(f'<rect x="{x - px//2 - 1}" y="{y}" width="{px}" height="{px}" fill="{CY}"/>')
                cr_l.append(f'<rect x="{x + px//2 + 1}" y="{y}" width="{px}" height="{px}" fill="{VI}"/>')
        col += len(g[0]) + 1
    width = col * step
    out = [f'<g class="{uid}c">{"".join(cy_l)}</g>', f'<g class="{uid}r">{"".join(cr_l)}</g>']
    css = [f".{uid}row{{animation-duration:{period}s;animation-delay:{delay}s;animation-iteration-count:infinite;animation-timing-function:steps(1);}}",
           f".{uid}c,.{uid}r{{opacity:0;animation:{uid}sp {period}s {delay}s infinite steps(1);}}",
           f"@keyframes {uid}sp{{0%,90%,100%{{opacity:0}} 91%{{opacity:.7}} 93%{{opacity:0}} 96%{{opacity:.55}} 97%{{opacity:0}}}}"]
    for r, items in rows.items():
        a, b = rnd.choice([-1, 1]) * rnd.randint(px, px * 3), rnd.choice([-1, 1]) * rnd.randint(px // 2 + 1, px * 2)
        css.append(f"@keyframes {uid}t{r}{{0%,90%,100%{{transform:none}} 91%{{transform:translateX({a}px)}} 92%{{transform:translateX({b}px)}} 93%{{transform:none}} 96%{{transform:translateX({-b}px)}} 97%{{transform:none}}}}")
        out.append(f'<g class="{uid}row" style="animation-name:{uid}t{r}">{"".join(shad[r])}</g>')
    for r, items in rows.items():
        out.append(f'<g class="{uid}row" style="animation-name:{uid}t{r}">{"".join(items)}</g>')
    noise = []
    for i in range(8):
        nx = x0 + rnd.randint(-1, col + 1) * step
        ny = y0 + rnd.randint(-1, 7) * step
        noise.append(f'<rect x="{nx}" y="{ny}" width="{px}" height="{px}" fill="{rnd.choice([CY, VI, AM])}"/>')
    out.append(f'<g class="{uid}n">{"".join(noise)}</g>')
    css.append(f".{uid}n{{opacity:0;animation:{uid}nz {period}s {delay}s infinite steps(1);}} @keyframes {uid}nz{{0%,90%,100%{{opacity:0}} 91%{{opacity:1}} 92%{{opacity:0}} 96%{{opacity:1}} 97%{{opacity:0}}}}")
    return "\n".join(out), "\n".join(css), width


PIXEL_CSS = """.pp{opacity:0;transform-box:fill-box;transform-origin:center;animation:ppin .3s cubic-bezier(.3,1.6,.5,1) forwards;}
@keyframes ppin{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.blink{animation:bl 1s infinite steps(1);} @keyframes bl{50%{opacity:0}}"""


def sq(x, y, s, color, extra=""):
    return f'<rect x="{x - s/2:.1f}" y="{y - s/2:.1f}" width="{s}" height="{s}" fill="{color}" {extra}/>'


def pixel_bar(x, y, w, h, color, uid, dur=4.0, seg=10, lit=8):
    """Segmented progress bar with a block of lit segments scanning back and forth."""
    n = int(w // seg)
    out = []
    for i in range(n):
        out.append(f'<rect x="{x + i*seg}" y="{y}" width="{seg-2}" height="{h}" fill="{LINE}"/>')
    vals = list(range(0, n - lit + 1)) + list(range(n - lit, -1, -1))
    xs = ";".join(f"{x + v*seg}" for v in vals)
    for k in range(lit):
        op = 0.35 + 0.65 * (k + 1) / lit
        out.append(f'<rect y="{y}" width="{seg-2}" height="{h}" fill="{color}" opacity="{op:.2f}" x="{x + k*seg}">'
                   f'<animate attributeName="x" values="{";".join(f"{x + (v+k)*seg}" for v in vals)}" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return "\n".join(out)


# =====================================================================
# SECTION TITLES
# =====================================================================
def section(name, label, color, num, seed):
    H = 70
    pt, css, w = pixel_text(label, 92, 16, 5, f"s{name}", period=6 + seed % 3, delay=1.5 + seed * 0.7, seed=seed)
    body = f'''<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="4" fill="{PANEL}" stroke="{LINE}"/>
<clipPath id="tc"><rect width="{W}" height="{H}" rx="4"/></clipPath>
<rect x="24" y="20" width="48" height="30" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.6"/>
<text class="mono" x="48" y="40" font-size="14" font-weight="700" fill="{color}" text-anchor="middle">{num}</text>
{pt}
<rect x="{92 + w + 4}" y="41" width="15" height="10" fill="{AM}" class="blink"/>
<g clip-path="url(#tc)">{pixel_bar(0, H-4, W, 4, color, "tb", dur=5, seg=12, lit=10)}</g>
{sq(W-34, 35, 9, color)}<rect x="{W-42}" y="27" width="16" height="16" fill="none" stroke="{color}"><animate attributeName="opacity" values="1;0;1" dur="1.6s" repeatCount="indefinite"/></rect>'''
    save(f"title-{name}.svg", svg(H, body, style=PIXEL_CSS + "\n" + css))


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
        gl = ' gl' if i in (3, 6) else ''
        out.append(f'<g class="ln{gl}" style="animation-delay:{0.25 + i*0.45:.2f}s{";animation-delay:%.2fs,%.2fs" % (0.25 + i*0.45, 4 + i) if gl else ""}">'
                   f'<text class="mono" x="26" y="{y}" font-size="12" fill="{LINE}">{i+1:02d}</text>'
                   f'<text class="mono" x="58" y="{y}" font-size="14.5">{ts}</text></g>')
    yc = 74 + len(lines) * 27
    body = f'''{frame(H)}
<rect x="0.5" y="0.5" width="{W-1}" height="36" rx="4" fill="{PANEL2}"/>
<line x1="0" y1="37" x2="{W}" y2="37" stroke="{LINE}"/>
<rect x="18" y="13" width="12" height="12" fill="{CY}"/><rect x="38" y="13" width="12" height="12" fill="{VI}"/><rect x="58" y="13" width="12" height="12" fill="{AM}"/>
<text class="mono" x="{W/2}" y="23" font-size="12" fill="{MUTED}" text-anchor="middle">kai@darmstadt: ~/about</text>
{chr(10).join(out)}
<text class="mono ln" x="58" y="{yc}" font-size="14.5" fill="{CY}" style="animation-delay:{0.25 + len(lines)*0.45:.2f}s">❯ <tspan fill="{AM}" class="blink">█</tspan></text>
<rect class="scan" x="0" y="38" width="{W}" height="3" fill="{CY}" opacity="0"/>
{runner(H, CY, dur=9)}'''
    style = PIXEL_CSS + '''
.ln{opacity:0;animation:ln .5s ease-out forwards;} @keyframes ln{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
.gl{animation:ln .5s ease-out forwards, gj 7s infinite steps(1);}
@keyframes gj{0%,92%,100%{transform:none} 93%{transform:translateX(-6px)} 94%{transform:translateX(5px)} 95%{transform:none}}
.scan{animation:scan 7s 4s infinite steps(1);} @keyframes scan{0%,92%,100%{opacity:0;transform:none} 93%{opacity:.5;transform:translateY(90px)} 94%{opacity:.4;transform:translateY(160px)} 95%{opacity:0}}'''
    save("about.svg", svg(H, body, style=style))


# =====================================================================
# PROJECT CARDS
# =====================================================================
def chip(x, y, text, color):
    w = len(text) * 7.9 + 30
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.5"/>'
            f'<rect x="{x+9}" y="{y+10}" width="6" height="6" fill="{color}"/>'
            f'<text class="mono" x="{x + 21}" y="{y + 17.5}" font-size="12.5" fill="{color}">{esc(text)}</text>', w)


def card(name, num, kind, color, title, desc, chips, stack, visual, seed):
    H = 236
    pt, css, tw = pixel_text(title, 36, 54, 4, f"c{name}", period=7 + seed, delay=2 + seed * 1.3, seed=seed + 10)
    parts = [frame(H, color)]
    for i in range(0, H - 44, 12):  # segmented accent bar
        parts.append(f'<rect x="0" y="{22 + i}" width="5" height="9" fill="{color}" opacity="{0.35 + 0.65*((i//12) % 4 == 0):.2f}">'
                     f'<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" begin="{i/120:.2f}s" repeatCount="indefinite"/></rect>')
    parts.append(f'<text class="mono" x="36" y="40" font-size="12" letter-spacing="2" fill="{color}">{num} / {esc(kind)}</text>')
    parts.append(pt)
    for i, d in enumerate(desc):
        parts.append(f'<text x="36" y="{114 + i*21}" font-size="14.5" fill="{SOFT}">{esc(d)}</text>')
    x = 36
    yc = 114 + len(desc) * 21 - 2
    for c in chips:
        s, w = chip(x, yc, c, color)
        parts.append(s); x += w + 10
    parts.append(f'<text class="mono" x="36" y="{H-22}" font-size="12" fill="{MUTED}">{esc(stack)}</text>')
    parts.append(f'<rect x="556" y="20" width="324" height="{H-40}" rx="2" fill="{BG}" stroke="{LINE}"/>')
    parts.append(visual)
    parts.append(runner(H, color, dur=8))
    parts.append(f'<text class="mono" x="532" y="{H-22}" font-size="12" fill="{color}" text-anchor="end">view repo ▸</text>')
    save(f"card-{name}.svg", svg(H, "\n".join(parts), style=PIXEL_CSS + "\n" + css))


def vis_adfontes():
    c = CY
    rows = [("claim_1", "chunk#12", True), ("claim_2", "chunk#47", True), ("claim_3", "—", False)]
    s = [f'<text class="mono" x="574" y="44" font-size="11" fill="{MUTED}">verify(claim) <tspan fill="{c}">▸</tspan> 3 checks</text>']
    D = 6
    for r, (cl, ch, ok) in enumerate(rows):
        y = 68 + r * 42
        s.append(f'<text class="mono" x="574" y="{y}" font-size="12" fill="{TEXT}">{cl} <tspan fill="{MUTED}">▸</tspan> <tspan fill="{VI if ok else MUTED}">{esc(ch)}</tspan></text>')
        for k, lab in enumerate(["struct", "NLI", "num"]):
            px_ = 574 + k * 66
            t0 = (r * 3 + k) * 0.45
            col = c if ok else AM
            mark = "✓" if ok else "✗"
            s.append(f'<g opacity="0.18"><animate attributeName="opacity" values="0.18;0.18;1;1;0.18" keyTimes="0;{t0/D:.3f};{(t0+0.2)/D:.3f};0.92;1" dur="{D}s" repeatCount="indefinite"/>'
                     f'<rect x="{px_}" y="{y+8}" width="58" height="20" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.7"/>'
                     f'<text class="mono" x="{px_+29}" y="{y+22}" font-size="11" fill="{col}" text-anchor="middle">{mark} {lab}</text></g>')
        if not ok:
            t0 = (r * 3 + 2) * 0.45 + 0.3
            s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0.3;1;0" keyTimes="0;{t0/D:.3f};{(t0+0.15)/D:.3f};{(t0+0.5)/D:.3f};0.92;1" dur="{D}s" repeatCount="indefinite"/>'
                     f'<rect x="774" y="{y+8}" width="76" height="20" fill="{AM}"/>'
                     f'<text class="mono" x="812" y="{y+22}" font-size="11" font-weight="700" fill="{BG}" text-anchor="middle">FLAGGED</text></g>')
    s.append(f'<text class="mono" x="574" y="204" font-size="11" fill="{MUTED}">metric: <tspan fill="{c}">unsupported claims / 100 answers</tspan></text>')
    return "\n".join(s)


def vis_pharma():
    cols = {"demo": 600, "indic.": 678, "drug": 756, "event": 840}
    s = []
    for lab, x in cols.items():
        s.append(f'<text class="mono" x="{x}" y="44" font-size="10.5" fill="{MUTED}" text-anchor="middle">{lab}</text>')
        for yy in range(56, 186, 8):
            s.append(f'<rect x="{x-1}" y="{yy}" width="2" height="3" fill="{LINE}"/>')
    N = {"a1": (600, 82), "a2": (600, 150), "b1": (678, 100), "b2": (678, 165),
         "c1": (756, 78), "c2": (756, 132), "c3": (756, 176), "d1": (840, 98), "d2": (840, 160)}
    E = [("a1", "b1"), ("a2", "b2"), ("a1", "c2"), ("b1", "c1"), ("b2", "c3"), ("b1", "c2"), ("c2", "d2"), ("c3", "d2")]
    for a, b in E:
        (x1, y1), (x2, y2) = N[a], N[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{VI}" stroke-opacity="0.35" stroke-width="1.3"/>')
    (x1, y1), (x2, y2) = N["c1"], N["d2"]
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AM}" stroke-width="1.5" stroke-dasharray="4 4">'
             f'<animate attributeName="opacity" values="0.9;0.9;0;0;0.9" keyTimes="0;0.35;0.5;0.95;1" dur="7s" repeatCount="indefinite"/></line>')
    s.append(f'<text class="mono" x="790" y="122" font-size="10" fill="{AM}">confounded<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.35;0.5;0.95;1" dur="7s" repeatCount="indefinite"/></text>')
    (x1, y1), (x2, y2) = N["c1"], N["d1"]
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CY}" stroke-width="2.4" stroke-dasharray="5 6" filter="url(#glow)">'
             f'<animate attributeName="stroke-dashoffset" values="22;0" dur="1s" repeatCount="indefinite"/></line>')
    s.append(f'<rect width="6" height="6" x="-3" y="-3" fill="{CY}" filter="url(#glow)"><animateMotion dur="1.6s" repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/></rect>')
    for k, (x, y) in N.items():
        col = CY if k in ("c1", "d1") else VI
        s.append(f'<rect x="{x-6}" y="{y-6}" width="14" height="14" fill="{VI}" opacity="0.4"/>')
        s.append(f'<rect x="{x-7}" y="{y-7}" width="14" height="14" fill="{BG}" stroke="{col}" stroke-width="2"/>{sq(x, y, 4, col)}')
    s.append(f'<text class="mono" x="574" y="206" font-size="11" fill="{TEXT}">rosuvastatin <tspan fill="{CY}">▸</tspan> myalgia  <tspan fill="{CY}">✓ SIDER</tspan></text>')
    return "\n".join(s)


def vis_evidentia():
    labs = ["URTI", "Pneum.", "Bronch.", "Influ.", "GERD"]
    steps = [[.2, .2, .2, .2, .2], [.24, .26, .1, .35, .05], [.18, .38, .14, .28, .02], [.07, .74, .09, .09, .01]]
    seq = [0, 1, 2, 3, 3, 0]
    kt = "0;0.22;0.44;0.66;0.92;1"
    base, maxh, seg = 178, 112, 8
    s = [f'<pattern id="segs" width="8" height="{seg}" patternUnits="userSpaceOnUse"><rect y="{seg-2}" width="8" height="2" fill="{BG}"/></pattern>']
    for i, lab in enumerate(labs):
        x = 584 + i * 58
        hs_ = [round(steps[j][i] * maxh / seg) * seg for j in seq]
        col = AM if i == 1 else (VI if i % 2 else CY)
        op = "1" if i == 1 else "0.55"
        s.append(f'<rect x="{x}" width="36" fill="{col}" fill-opacity="{op}" y="{base-hs_[0]}" height="{hs_[0]}">'
                 f'<animate attributeName="height" values="{";".join(str(h) for h in hs_)}" keyTimes="{kt}" dur="8s" repeatCount="indefinite" calcMode="discrete"/>'
                 f'<animate attributeName="y" values="{";".join(str(base-h) for h in hs_)}" keyTimes="{kt}" dur="8s" repeatCount="indefinite" calcMode="discrete"/></rect>')
        s.append(f'<text class="mono" x="{x+18}" y="{base+16}" font-size="10" fill="{MUTED}" text-anchor="middle">{lab}</text>')
    s.append(f'<rect x="580" y="60" width="290" height="{base-60}" fill="url(#segs)"/>')
    s.append(f'<rect x="576" y="{base}" width="286" height="2" fill="{LINE}"/>')
    ev = ["+ fever", "+ cough", "+ chest pain"]
    x = 574
    for k, e in enumerate(ev):
        vals = ["0"] * 6
        for j in range(6):
            if 1 + k <= seq[j] and j < 5:
                vals[j] = "1"
        w = len(e) * 7 + 16
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{kt}" dur="8s" calcMode="discrete" repeatCount="indefinite"/>'
                 f'<rect x="{x}" y="34" width="{w}" height="20" fill="{AM}" fill-opacity="0.12" stroke="{AM}" stroke-opacity="0.7"/>'
                 f'<text class="mono" x="{x+8}" y="48" font-size="11" fill="{AM}">{e}</text></g>')
        x += w + 8
    s.append(f'<text class="mono" x="574" y="212" font-size="11" fill="{MUTED}">P(dx | evidence) · every shift attributed</text>')
    return "\n".join(s)


def vis_fons():
    s = [f'<rect x="580" y="36" width="140" height="160" fill="{PANEL2}" stroke="{LINE}"/>',
         f'<text class="mono" x="592" y="56" font-size="10.5" fill="{CY}">GDPR · Art. 6</text>']
    ys = [72, 84, 96, 112, 124, 136, 152, 164, 176]
    for i, y in enumerate(ys):
        w = [110, 96, 104, 112, 88, 100, 108, 92, 70][i]
        for xx in range(592, 592 + w, 8):
            s.append(f'<rect x="{xx}" y="{y}" width="6" height="5" fill="{SOFT}" fill-opacity="0.25"/>')
    s.append(f'<rect x="586" width="128" height="22" fill="{AM}" fill-opacity="0.16" stroke="{AM}" stroke-opacity="0.8" y="66">'
             f'<animate attributeName="y" values="66;104;146;105;105;66" keyTimes="0;0.15;0.3;0.42;0.92;1" dur="7s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    for i, (xx, yy) in enumerate([(718, 114), (726, 106), (734, 98), (742, 90), (750, 84)]):
        s.append(f'<rect x="{xx}" y="{yy}" width="4" height="4" fill="{AM}" opacity="0.8"/>')
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.42;0.5;0.92;1" dur="7s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<rect x="740" y="60" width="128" height="50" fill="{CY}" fill-opacity="0.08" stroke="{CY}" stroke-opacity="0.7"/>'
             f'<text class="mono" x="750" y="80" font-size="10.5" fill="{TEXT}">"consent is a</text>'
             f'<text class="mono" x="750" y="96" font-size="10.5" fill="{TEXT}">lawful basis" <tspan fill="{CY}">✓</tspan></text></g>')
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.62;0.92;1" dur="7s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<rect x="740" y="126" width="128" height="50" fill="{AM}" fill-opacity="0.08" stroke="{AM}" stroke-opacity="0.7"/>'
             f'<text class="mono" x="750" y="146" font-size="10.5" fill="{TEXT}">"Art. 6(7)..."</text>'
             f'<text class="mono" x="750" y="162" font-size="10.5" fill="{AM}">✗ not entailed</text></g>')
    s.append(f'<text class="mono" x="574" y="212" font-size="11" fill="{MUTED}">cite ▸ retrieve ▸ NLI-verify</text>')
    return "\n".join(s)


def vis_overseer():
    """Mini tray widget: sessions whose state squares change over a loop."""
    D = 9
    ST = {"work": (CY, "working"), "move": (TEXT, "your move"), "appr": (AM, "needs approval"),
          "quiet": (VI, "gone quiet"), "end": (MUTED, "ended")}
    rows = [("api-server",  ["work", "work", "appr", "work"]),
            ("thesis-eval", ["work", "move", "move", "work"]),
            ("portfolio",   ["move", "work", "work", "quiet"]),
            ("neuro-graph", ["work", "work", "end", "end"])]
    kt = "0;0.25;0.5;0.75;1"
    s = [f'<rect x="572" y="32" width="12" height="12" fill="{AM}"/><rect x="575" y="35" width="6" height="6" fill="{BG}"/><rect x="577" y="37" width="2" height="2" fill="{AM}"/>',
         f'<text class="mono" x="592" y="42" font-size="11" fill="{TEXT}">overseer <tspan fill="{MUTED}">· 4 sessions</tspan></text>',
         f'<line x1="572" y1="52" x2="864" y2="52" stroke="{LINE}"/>']
    for r, (name, seq) in enumerate(rows):
        y = 74 + r * 30
        s.append(f'<text class="mono" x="594" y="{y}" font-size="11.5" fill="{TEXT}">{name}</text>')
        for st in set(seq):
            col, lab = ST[st]
            vals = ";".join("1" if q == st else "0" for q in seq) + (";1" if seq[0] == st else ";0")
            blink = (f'<animate attributeName="fill-opacity" values="1;0.2;1" dur="0.8s" repeatCount="indefinite"/>' if st == "appr" else "")
            work = ""
            if st == "work":
                work = "".join(f'<rect x="{850 - (2-k)*8}" y="{y-7}" width="5" height="5" fill="{CY}"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.2s" begin="{k*0.3}s" repeatCount="indefinite"/></rect>' for k in range(3))
            s.append(f'<g opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/>'
                     f'<rect x="574" y="{y-10}" width="11" height="11" fill="{col}">{blink}</rect>'
                     f'<text class="mono" x="{826 if st == "work" else 862}" y="{y}" font-size="10.5" fill="{col}" text-anchor="end">{lab}</text>{work}</g>')
    # approval prompt pops when api-server needs approval
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.5;0.52;0.75;1" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<rect x="572" y="194" width="292" height="18" fill="{AM}" fill-opacity="0.12" stroke="{AM}" stroke-opacity="0.7"/>'
             f'<text class="mono" x="580" y="207" font-size="10.5" fill="{AM}">api-server wants to run: npm publish  [y/n]</text></g>')
    return "\n".join(s)


def vis_decisions():
    D = 9
    def node(x, y, w, label, col=CY, extra=""):
        return (f'<g {extra}><rect x="{x+2}" y="{y+2}" width="{w}" height="22" fill="{VI}" opacity="0.35"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="22" fill="{PANEL2}" stroke="{col}" stroke-width="1.5"/>'
                f'<text class="mono" x="{x+8}" y="{y+15}" font-size="10.5" fill="{TEXT}">{esc(label)}</text></g>')
    def gate(vals, kt):
        return f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{D}s" calcMode="discrete" repeatCount="indefinite"/>'
    s = []
    # edges D-1 -> D-3, D-1 -> D-4
    for yy in (44, 86):
        s.append(f'<path d="M678 56 H708 V{yy+11} H736" stroke="{CY}" stroke-opacity="0.6" stroke-width="1.5"/>'
                 f'<polygon points="736,{yy+7} 742,{yy+11} 736,{yy+15}" fill="{CY}"/>')
        s.append(f'<rect width="5" height="5" fill="{CY}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M678 56 H708 V{yy+11} H736"/></rect>')
    # D-1 normal then replaced
    s.append(node(574, 45, 104, "D-1 sqlite", CY, f'opacity="1">{gate("1;1;0;1", "0;0.36;0.36;1")}<g'.replace("<g", "<g") ) + "</g>" if False else "")
    s.append(f'<g>{gate("1;0;0;1", "0;0.36;0.97;1")}' + node(574, 45, 104, "D-1 sqlite") + "</g>")
    s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.36;0.97;1")}'
             f'<rect x="574" y="45" width="104" height="22" fill="none" stroke="{MUTED}" stroke-dasharray="4 3"/>'
             f'<text class="mono" x="582" y="60" font-size="10.5" fill="{MUTED}" text-decoration="line-through">D-1 sqlite</text></g>')
    # D-6 postgres appears and replaces D-1
    s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.3;0.97;1")}' + node(574, 104, 104, "D-6 postgres", AM) +
             f'<path d="M626 104 V71" stroke="{AM}" stroke-width="1.5" stroke-dasharray="3 3"/><polygon points="622,73 626,67 630,73" fill="{AM}"/>'
             f'<text class="mono" x="632" y="90" font-size="9.5" fill="{AM}">replaces</text></g>')
    # D-3 / D-4 go stale
    for (yy, lab) in ((33, "D-3 offline"), (75, "D-4 sync")):
        s.append(node(742, yy, 120, lab))
        s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.44;0.97;1")}'
                 f'<rect x="742" y="{yy}" width="120" height="22" fill="none" stroke="{VI}" stroke-width="2"/>'
                 f'<rect x="846" y="{yy+5}" width="12" height="12" fill="{VI}"><animate attributeName="opacity" values="1;0.2;1" dur="0.9s" repeatCount="indefinite"/></rect>'
                 f'<text class="mono" x="852" y="{yy+15}" font-size="10" font-weight="700" fill="{BG}" text-anchor="middle">!</text></g>')
    s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.44;0.97;1")}<text class="mono" x="742" y="122" font-size="10" fill="{VI}">2 decisions stale</text></g>')
    # contradiction guard in the terminal strip
    s.append(f'<line x1="572" y1="150" x2="864" y2="150" stroke="{LINE}"/>')
    s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.6;0.97;1")}<text class="mono" x="574" y="172" font-size="11" fill="{TEXT}"><tspan fill="{CY}">❯</tspan> npm install jest</text></g>')
    s.append(f'<g opacity="0">{gate("0;1;1;0", "0;0.7;0.97;1")}<rect x="572" y="182" width="292" height="20" fill="{AM}" fill-opacity="0.12" stroke="{AM}" stroke-opacity="0.7"/>'
             f'<text class="mono" x="580" y="196" font-size="10.5" fill="{AM}">⚠ D-2 chose vitest over jest. allow? [y/n]</text></g>')
    return "\n".join(x for x in s if x)


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
        parts.append(f'<rect x="28" y="{y+9}" width="8" height="8" fill="{col}"/>')
        parts.append(f'<text class="mono" x="44" y="{y+18}" font-size="11.5" letter-spacing="2" fill="{col}">{esc(gname)}</text>')
        x = 200
        for it in items:
            w = len(it) * 8.4 + 32
            if x + w > W - 28:
                x = 200; y += 38
            d = idx * 0.18
            parts.append(f'<g class="pill" style="animation-delay:{d:.2f}s">'
                         f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="0.4">'
                         f'<animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="3.6s" begin="{d:.2f}s" repeatCount="indefinite"/></rect>'
                         f'<rect x="{x+10}" y="{y+11}" width="6" height="6" fill="{col}"/>'
                         f'<text class="mono" x="{x+24}" y="{y+18.5}" font-size="13" fill="{TEXT}">{esc(it)}</text></g>')
            x += w + 10
            idx += 1
        y += 48
    for xx in range(28, W - 28, 10):
        parts.append(f'<rect x="{xx}" y="{y+1}" width="6" height="2" fill="{LINE}"/>')
    y += 30
    parts.append(f'<text class="mono" x="28" y="{y}" font-size="12.5" fill="{MUTED}"><tspan fill="{CY}">core ▸</tspan> causal discovery · Bayesian networks · RAG verification · RLHF/DPO · <tspan fill="{VI}">CLIP · BLIP-2 · LLaVA</tspan></text>')
    H = y + 26
    style = '''.pill{opacity:0;animation:pin .4s steps(4) forwards;} @keyframes pin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}'''
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
        parts.append(sq(34, y - 5, 10, col, 'filter="url(#glow)"'))
        parts.append(f'<rect x="29" y="{y-10}" width="10" height="10" fill="none" stroke="{col}">'
                     f'<animate attributeName="x" values="29;21" dur="2s" begin="{i*0.6}s" calcMode="discrete" repeatCount="indefinite"/>'
                     f'<animate attributeName="y" values="{y-10};{y-18}" dur="2s" begin="{i*0.6}s" calcMode="discrete" repeatCount="indefinite"/>'
                     f'<animate attributeName="width" values="10;26" dur="2s" begin="{i*0.6}s" calcMode="discrete" repeatCount="indefinite"/>'
                     f'<animate attributeName="height" values="10;26" dur="2s" begin="{i*0.6}s" calcMode="discrete" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.9;0.3;0" dur="2s" begin="{i*0.6}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
        parts.append(f'<text class="mono" x="56" y="{y}" font-size="12" letter-spacing="2" fill="{col}">{lab}</text>')
        parts.append(f'<text x="170" y="{y}" font-size="16" font-weight="600" fill="{TEXT}">{esc(main)}</text>')
        parts.append(f'<text class="mono" x="170" y="{y+20}" font-size="11.5" fill="{MUTED}">{esc(sub)}</text>')
        parts.append(pixel_bar(170, y + 30, W - 200, 5, col, f"nb{i}", dur=4 + i, seg=10, lit=8))
        y += 66
    H = y - 6
    body = frame(H) + "\n" + "\n".join(parts) + "\n" + runner(H, VI, dur=9)
    save("now.svg", svg(H, body))


# =====================================================================
# FOOTER
# =====================================================================
def footer():
    H = 150
    parts = [frame(H)]
    waves = []
    for (col, amp, per, ph, dur, sz) in [(CY, 12, 240, 0, 6, 6), (VI, 16, 240, 2.1, 8, 6), (AM, 8, 240, 4.2, 5, 6)]:
        rects = []
        for x in range(-per, W + per, 8):
            y = 56 + amp * math.sin((x / per) * 2 * math.pi + ph)
            y = round(y / 4) * 4
            rects.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{col}" opacity="0.7"/>')
        waves.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-{per} 0" dur="{dur}s" repeatCount="indefinite"/>{"".join(rects)}</g>')
    pt, css, w = pixel_text("AD FONTES", 0, 0, 4, "ft", period=8, delay=3, pop=False, seed=4)
    parts.append(f'<g mask="url(#m)">{"".join(waves)}</g>')
    parts.append(f'<g transform="translate({W/2 - w/2:.0f},90)">{pt}</g>')
    parts.append(f'<text class="mono" x="{W/2}" y="{H-12}" font-size="10.5" fill="{MUTED}" text-anchor="middle">back to the sources</text>')
    defs = f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.15" stop-color="#fff"/><stop offset="0.85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
    save("footer.svg", svg(H, "\n".join(parts), defs, PIXEL_CSS + "\n" + css))


if __name__ == "__main__":
    header(); about(); stack(); now(); footer()
    section("about", "about", CY, "01", 1)
    section("work", "featured work", VI, "02", 2)
    section("stack", "toolkit", AM, "03", 3)
    section("now", "currently", CY, "04", 4)
    card("overseer", "01", "DEV TOOLING · CLAUDE CODE · TAURI", AM, "overseer",
         ["A tray widget that watches every local Claude Code",
          "session and flags the ones that need you."],
         ["5 live states", "hook-driven", "Windows + macOS"],
         "Tauri · Rust · Node.js · Claude Code hooks", vis_overseer(), 5)
    card("decisiongraph", "02", "CLAUDE CODE PLUGIN · AGENT MEMORY", CY, "decision graph",
         ["Records the decisions from long sessions as a graph",
          "Claude can query: why, impact, what went stale."],
         ["100% recall", "99% precision", "10-case eval"],
         "Python (stdlib) · Claude Code hooks · Haiku", vis_decisions(), 6)
    card("pharmacausal", "03", "CAUSAL DISCOVERY · PHARMACOVIGILANCE", VI, "pharmacausal",
         ["PC + FCI causal discovery on FDA adverse-event reports,",
          "with time-ordered tiers so confounders get pruned."],
         ["422k reports", "67% FCI precision", "SIDER-validated"],
         "causal-learn · pandas · pytest", vis_pharma(), 2)
    card("evidentia", "04", "BAYESIAN NETWORKS · EXPLAINABILITY", AM, "evidentia",
         ["An 895-node Bayesian-network symptom checker where",
          "every probability shift is traced to its evidence."],
         ["ECE 0.0036", "134,529 test patients"],
         "Python · FastAPI · React · Cytoscape", vis_evidentia(), 3)
    card("fonsiuris", "05", "LEGAL RAG · NLI VERIFICATION", CY, "fons-iuris",
         ["GDPR & EU AI Act Q&A that cites the exact paragraph",
          "and flags any claim its source doesn't entail."],
         ["EUR-Lex corpus", "NLI-verified"],
         "FastAPI · Chroma · Transformers · React", vis_fons(), 4)
    print("ok", sorted(os.listdir(OUT)))
