# -*- coding: utf-8 -*-
"""Generate minimalist illustrated case thumbnails (white canvas, pastel data-confetti
scatter, one clean line-art object per project) in the spirit of the original site."""
import os

OUT = os.path.join(os.path.dirname(__file__), "www", "images", "tiles")
os.makedirs(OUT, exist_ok=True)

W, H = 400, 300

# ---- palette ----------------------------------------------------------------
INK   = "#1d1d1f"   # central line-art
SOFT  = "#5b6068"   # secondary line
HAIR  = "#e8e8ed"   # hairline
TEAL  = "#1d607d"   # brand accent
TEALL = "#7faec0"   # light teal
CORAL = "#e6a79e"
AMBER = "#e6bf73"
MINT  = "#8fc7a6"
PERI  = "#9fb2d6"
GREYF = "#f5f5f7"   # ui fill

# ---- decorative scatter: shared vocabulary, varied per tile -----------------
PASTELS = [TEALL, PERI, MINT, AMBER, CORAL]

def m_bars(x, y, c, c2):
    out = ['<g stroke-linecap="round">']
    for dx, h, cc in [(0, 18, c), (9, 30, c2), (18, 14, c), (27, 24, c2)]:
        out.append(f'<line x1="{x+dx}" y1="{y}" x2="{x+dx}" y2="{y-h}" stroke="{cc}" stroke-width="4"/>')
    out.append('</g>')
    return "".join(out)

def m_arcs(x, y, c, c2):
    out = ['<g fill="none">']
    for r, cc in [(9, c), (18, c2), (27, c)]:
        out.append(f'<path d="M {x-r} {y} A {r} {r} 0 0 1 {x+r} {y}" stroke="{cc}" stroke-width="2.4"/>')
    out.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{c2}"/></g>')
    return "".join(out)

def m_line(x, y, c, c2):
    return (f'<g fill="none"><polyline points="{x},{y} {x+22},{y-16} {x+40},{y-7} {x+62},{y-26}" '
            f'stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{x+62}" cy="{y-26}" r="3.2" fill="{c}"/></g>')

def m_dottedarc(x, y, c, c2):
    out = [f'<path d="M {x} {y} A 44 44 0 0 1 {x+62} {y-30}" fill="none" stroke="{c}" '
           f'stroke-width="2.4" stroke-dasharray="2 7" stroke-linecap="round"/>']
    for dx, dy, cc in [(28, 0, c2), (42, -6, c), (54, 2, c2)]:
        out.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.8" fill="{cc}"/>')
    return "".join(out)

def m_tri(x, y, c, c2):
    return f'<path d="M {x} {y-13} l 9 15 l -18 0 z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'

def m_ring(x, y, c, c2):
    return f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="{c}" stroke-width="2"/>'

def m_plus(x, y, c, c2):
    return (f'<g stroke="{c}" stroke-width="2" stroke-linecap="round">'
            f'<line x1="{x-6}" y1="{y}" x2="{x+6}" y2="{y}"/><line x1="{x}" y1="{y-6}" x2="{x}" y2="{y+6}"/></g>')

def m_donut(x, y, c, c2):
    return (f'<g fill="none"><circle cx="{x}" cy="{y}" r="9" stroke="{HAIR}" stroke-width="3.5"/>'
            f'<path d="M {x} {y-9} A 9 9 0 0 1 {x+9} {y}" stroke="{c}" stroke-width="3.5"/></g>')

BIG = [m_bars, m_arcs, m_line, m_dottedarc, m_donut]   # anchor motifs (corners)
SML = [m_tri, m_ring, m_plus]                            # sprinkles (edges)

# corner slots (x,y); arcs/donut read centred, bars/line read from their origin
SLOTS = [(40, 60), (330, 58), (40, 250), (322, 250)]

def scatter(i):
    s = []
    for slot, (x, y) in enumerate(SLOTS):
        motif = BIG[(i + slot * 2) % len(BIG)]
        c = PASTELS[(i + slot) % len(PASTELS)]
        c2 = PASTELS[(i + slot + 2) % len(PASTELS)]
        s.append(f'<g opacity="0.5">{motif(x, y, c, c2)}</g>')
    # two deterministic sprinkles on the side margins
    spr = [(64, 150), (348, 150), (200, 36)]
    for k in range(2):
        sx, sy = spr[(i + k) % len(spr)]
        sm = SML[(i + k) % len(SML)]
        sc = PASTELS[(i + k + 1) % len(PASTELS)]
        s.append(f'<g opacity="0.45">{sm(sx, sy, sc, sc)}</g>')
    return "\n".join(s)

def doc(center, i):
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
            f'{scatter(i)}'
            f'<g fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{center}</g>'
            f'</svg>')

# common helpers for center objects -------------------------------------------
def fill(el): return el  # readability

# ---- center motifs ----------------------------------------------------------
def c_design_program():
    # broadcast screen + play + synced transcript lines + waveform
    return (
      f'<rect x="120" y="92" width="120" height="80" rx="8" fill="{GREYF}"/>'
      f'<path d="M 168 118 l 26 16 l -26 16 z" fill="{TEAL}" stroke="none"/>'
      f'<rect x="252" y="96" width="60" height="6" rx="3" fill="{HAIR}" stroke="none"/>'
      f'<rect x="252" y="112" width="48" height="6" rx="3" fill="{HAIR}" stroke="none"/>'
      f'<rect x="252" y="128" width="56" height="6" rx="3" fill="{HAIR}" stroke="none"/>'
      f'<rect x="252" y="144" width="40" height="6" rx="3" fill="{HAIR}" stroke="none"/>'
      # waveform under screen
      f'<g stroke="{TEAL}" stroke-width="2.6">'
      f'<line x1="128" y1="194" x2="128" y2="186"/><line x1="140" y1="198" x2="140" y2="182"/>'
      f'<line x1="152" y1="200" x2="152" y2="180"/><line x1="164" y1="196" x2="164" y2="184"/>'
      f'<line x1="176" y1="200" x2="176" y2="180"/><line x1="188" y1="194" x2="188" y2="186"/>'
      f'<line x1="200" y1="198" x2="200" y2="182"/><line x1="212" y1="196" x2="212" y2="184"/>'
      f'<line x1="224" y1="194" x2="224" y2="186"/></g>'
    )

def c_design_system():
    # 3x3 component grid + swatch chips + a button pill + token ring
    g=[]
    sw=[TEAL,CORAL,AMBER,MINT]
    x0,y0,cell,gap=140,86,30,8
    k=0
    for r in range(3):
        for col in range(3):
            x=x0+col*(cell+gap); y=y0+r*(cell+gap)
            if (r*3+col) in (0,4,8):
                c=sw[k%len(sw)]; k+=1
                g.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{c}" stroke="none"/>')
            else:
                g.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{GREYF}"/>')
    # button pill bottom
    g.append(f'<rect x="244" y="150" width="58" height="22" rx="11" fill="{TEAL}" stroke="none"/>')
    g.append(f'<rect x="254" y="159" width="38" height="4" rx="2" fill="#ffffff" stroke="none"/>')
    return "".join(g)

def c_supply_chain():
    # connected node flow + a highlighted node + planning bars
    g=[]
    nodes=[(150,110),(210,92),(270,118),(200,150)]
    links=[(0,1),(1,2),(0,3),(3,2)]
    for a,b in links:
        g.append(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{HAIR}" stroke-width="2.4"/>')
    for i,(x,y) in enumerate(nodes):
        if i==1:
            g.append(f'<rect x="{x-16}" y="{y-13}" width="32" height="26" rx="6" fill="{TEAL}" stroke="none"/>')
        else:
            g.append(f'<rect x="{x-16}" y="{y-13}" width="32" height="26" rx="6" fill="#ffffff"/>')
    # planning bars baseline
    bx,by=150,196
    for i,h in enumerate([14,24,18,30,22]):
        c = TEAL if i==3 else HAIR
        g.append(f'<rect x="{bx+i*22}" y="{by-h}" width="12" height="{h}" rx="3" fill="{c}" stroke="none"/>')
    g.append(f'<line x1="146" y1="198" x2="262" y2="198" stroke="{HAIR}" stroke-width="2"/>')
    return "".join(g)

def c_oil_gas():
    # gauge dial + needle + live line panel
    g=[]
    cx,cy=168,150
    g.append(f'<path d="M {cx-44} {cy} A 44 44 0 0 1 {cx+44} {cy}" stroke="{HAIR}" stroke-width="6"/>')
    g.append(f'<path d="M {cx-44} {cy} A 44 44 0 0 1 {cx+6} {cy-43.6}" stroke="{TEAL}" stroke-width="6"/>')
    g.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+22}" y2="{cy-34}" stroke="{INK}" stroke-width="2.8"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{INK}" stroke="none"/>')
    # mini live panel
    g.append(f'<rect x="226" y="110" width="86" height="64" rx="8" fill="{GREYF}"/>')
    g.append(f'<polyline points="234,150 248,138 260,144 274,124 288,134 304,118" stroke="{TEAL}" stroke-width="2.6"/>')
    g.append(f'<circle cx="304" cy="118" r="3.2" fill="{TEAL}" stroke="none"/>')
    return "".join(g)

def c_mobile_health():
    # phone with medical cross + pulse
    g=[]
    g.append(f'<rect x="168" y="78" width="64" height="118" rx="12" fill="{GREYF}"/>')
    g.append(f'<rect x="178" y="92" width="44" height="6" rx="3" fill="{HAIR}" stroke="none"/>')
    # cross
    g.append(f'<rect x="192" y="116" width="16" height="44" rx="4" fill="{CORAL}" stroke="none"/>')
    g.append(f'<rect x="178" y="130" width="44" height="16" rx="4" fill="{CORAL}" stroke="none"/>')
    # pulse line
    g.append(f'<polyline points="176,178 186,178 191,170 197,186 203,174 209,178 224,178" stroke="{TEAL}" stroke-width="2.4"/>')
    return "".join(g)

def c_clinical():
    # bedside vitals monitor on stand + heart + waveform
    g=[]
    g.append(f'<rect x="146" y="84" width="108" height="76" rx="8" fill="{GREYF}"/>')
    g.append(f'<polyline points="156,128 168,128 174,112 182,142 189,122 196,128 214,128" stroke="{TEAL}" stroke-width="2.6"/>')
    g.append(f'<path d="M 232 104 c -5,-6 -14,-2 -14,5 c 0,7 14,14 14,14 c 0,0 14,-7 14,-14 c 0,-7 -9,-11 -14,-5 z" fill="{CORAL}" stroke="none"/>')
    g.append(f'<line x1="200" y1="160" x2="200" y2="184"/>')
    g.append(f'<line x1="182" y1="186" x2="218" y2="186"/>')
    # second small device
    g.append(f'<rect x="262" y="120" width="34" height="56" rx="8" fill="#ffffff"/>')
    g.append(f'<line x1="270" y1="134" x2="288" y2="134" stroke="{HAIR}"/>')
    g.append(f'<line x1="270" y1="146" x2="284" y2="146" stroke="{HAIR}"/>')
    return "".join(g)

def c_wireless():
    # access point + radiating wifi arcs + small node grid
    g=[]
    cx,cy=180,170
    g.append(f'<rect x="{cx-18}" y="{cy-8}" width="36" height="20" rx="5" fill="{TEAL}" stroke="none"/>')
    g.append(f'<circle cx="{cx}" cy="{cy+2}" r="3" fill="#ffffff" stroke="none"/>')
    for r,c in [(26,TEALL),(44,PERI),(62,HAIR)]:
        g.append(f'<path d="M {cx-r} {cy-6} A {r} {r} 0 0 1 {cx+r} {cy-6}" stroke="{c}" stroke-width="2.6"/>')
    # node grid right
    for i in range(3):
        for j in range(3):
            g.append(f'<circle cx="{262+j*20}" cy="{96+i*20}" r="3.4" fill="{HAIR}" stroke="none"/>')
    g.append(f'<circle cx="282" cy="116" r="3.4" fill="{TEAL}" stroke="none"/>')
    return "".join(g)

def c_property():
    # house/building + map pin + listing card
    g=[]
    g.append(f'<path d="M 150 150 l 34 -28 l 34 28" />')
    g.append(f'<rect x="158" y="150" width="52" height="44" rx="3" fill="{GREYF}"/>')
    g.append(f'<rect x="172" y="164" width="14" height="14" rx="2" fill="#ffffff"/>')
    g.append(f'<rect x="192" y="164" width="10" height="30" rx="2" fill="#ffffff"/>')
    # map pin
    g.append(f'<path d="M 250 120 c -11,0 -20,9 -20,20 c 0,15 20,30 20,30 c 0,0 20,-15 20,-30 c 0,-11 -9,-20 -20,-20 z" fill="{TEAL}" stroke="none"/>')
    g.append(f'<circle cx="250" cy="140" r="7" fill="#ffffff" stroke="none"/>')
    # listing line card
    g.append(f'<rect x="230" y="178" width="64" height="20" rx="5" fill="{GREYF}"/>')
    g.append(f'<line x1="240" y1="188" x2="284" y2="188" stroke="{HAIR}"/>')
    return "".join(g)

def c_bi_platform():
    # browser dashboard window: bars + line + donut
    g=[]
    g.append(f'<rect x="128" y="86" width="144" height="104" rx="10" fill="{GREYF}"/>')
    g.append(f'<line x1="128" y1="104" x2="272" y2="104" stroke="{HAIR}"/>')
    for i,c in enumerate([CORAL,AMBER,MINT]):
        g.append(f'<circle cx="{140+i*10}" cy="95" r="3" fill="{c}" stroke="none"/>')
    # bars
    bx,by=144,170
    for i,h in enumerate([20,34,26,42]):
        g.append(f'<rect x="{bx+i*16}" y="{by-h}" width="9" height="{h}" rx="2" fill="{TEAL}" stroke="none" opacity="{0.55+i*0.12:.2f}"/>')
    # line
    g.append(f'<polyline points="218,168 230,150 242,158 256,134" stroke="{CORAL}" stroke-width="2.4"/>')
    # donut
    g.append(f'<circle cx="240" cy="120" r="14" fill="none" stroke="{HAIR}" stroke-width="6"/>')
    g.append(f'<path d="M 240 106 A 14 14 0 0 1 252 128" fill="none" stroke="{TEAL}" stroke-width="6"/>')
    return "".join(g)

def c_classic():
    # presentation screen on stand + chart slide
    g=[]
    g.append(f'<rect x="138" y="80" width="124" height="86" rx="8" fill="{GREYF}"/>')
    g.append(f'<polyline points="150,150 168,132 182,140 200,116 218,126 236,104" stroke="{TEAL}" stroke-width="2.6"/>')
    g.append(f'<circle cx="236" cy="104" r="3.2" fill="{TEAL}" stroke="none"/>')
    g.append(f'<line x1="150" y1="156" x2="250" y2="156" stroke="{HAIR}"/>')
    # stand
    g.append(f'<line x1="200" y1="166" x2="200" y2="188"/>')
    g.append(f'<line x1="176" y1="190" x2="224" y2="190"/>')
    return "".join(g)

def c_messenger():
    # big chat bubble + small reply + motion arcs
    g=[]
    g.append(f'<path d="M 150 96 h 86 a 12 12 0 0 1 12 12 v 40 a 12 12 0 0 1 -12 12 h -52 l -20 18 v -18 h -14 a 12 12 0 0 1 -12 -12 v -40 a 12 12 0 0 1 12 -12 z" fill="{GREYF}"/>')
    g.append(f'<line x1="160" y1="116" x2="226" y2="116" stroke="{HAIR}"/>')
    g.append(f'<line x1="160" y1="130" x2="210" y2="130" stroke="{HAIR}"/>')
    # small reply bubble teal
    g.append(f'<path d="M 230 150 h 36 a 10 10 0 0 1 10 10 v 18 a 10 10 0 0 1 -10 10 h -10 l -14 12 v -12 h -2 a 10 10 0 0 1 -10 -10 v -18 a 10 10 0 0 1 10 -10 z" fill="{TEAL}" stroke="none"/>')
    g.append(f'<circle cx="244" cy="169" r="2.4" fill="#fff" stroke="none"/><circle cx="252" cy="169" r="2.4" fill="#fff" stroke="none"/><circle cx="260" cy="169" r="2.4" fill="#fff" stroke="none"/>')
    return "".join(g)

def c_onboarding():
    # phone with illustration circle + swipe dots + arrow
    g=[]
    g.append(f'<rect x="166" y="74" width="68" height="124" rx="14" fill="{GREYF}"/>')
    g.append(f'<circle cx="200" cy="118" r="22" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')
    g.append(f'<path d="M 192 118 l 6 6 l 12 -14" stroke="{TEAL}" stroke-width="2.6"/>')
    g.append(f'<rect x="182" y="150" width="36" height="5" rx="2.5" fill="{HAIR}" stroke="none"/>')
    g.append(f'<rect x="182" y="160" width="26" height="5" rx="2.5" fill="{HAIR}" stroke="none"/>')
    # dots
    g.append(f'<rect x="186" y="180" width="14" height="5" rx="2.5" fill="{TEAL}" stroke="none"/>')
    g.append(f'<circle cx="208" cy="182.5" r="2.5" fill="{HAIR}" stroke="none"/><circle cx="216" cy="182.5" r="2.5" fill="{HAIR}" stroke="none"/>')
    return "".join(g)

def c_headphone():
    # headphones on a rounded teal tile (nod to original)
    g=[]
    g.append(f'<rect x="138" y="74" width="124" height="152" rx="22" fill="{GREYF}" stroke="none"/>')
    cx=200
    g.append(f'<path d="M 162 158 v -16 a 38 38 0 0 1 76 0 v 16" stroke="{TEAL}" stroke-width="3"/>')
    g.append(f'<rect x="154" y="156" width="20" height="34" rx="8" fill="{TEAL}" stroke="none"/>')
    g.append(f'<rect x="226" y="156" width="20" height="34" rx="8" fill="{TEAL}" stroke="none"/>')
    return "".join(g)

THUMBS = {
    "design-program":      c_design_program,
    "design-system":       c_design_system,
    "supply-chain":        c_supply_chain,
    "oil-gas":             c_oil_gas,
    "mobile-health":       c_mobile_health,
    "clinical":            c_clinical,
    "wireless":            c_wireless,
    "property":            c_property,
    "bi-platform":         c_bi_platform,
    "classic":             c_classic,
    "messenger":           c_messenger,
    "onboarding":          c_onboarding,
    "headphone":           c_headphone,
}

for i, (name, fn) in enumerate(THUMBS.items()):
    svg = doc(fn(), i)
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name + ".svg")
print("DONE ->", OUT)
