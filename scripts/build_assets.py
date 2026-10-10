"""Builds the static design SVGs of the profile README.

Run:  python scripts/build_assets.py
Data-driven cards (metrics, stats, languages) live in github_stats.py.
"""
import textwrap

from svgkit import (BG, BLUE, DIM, GREEN, GREEN_SOFT, LILAC, LINE, LINE_SOFT, MONO, MUTED, PANEL, SAND, TERRA,
                    TERRA_DEEP, TEXT, github_mark, icon, svg, t, text_width, write)

AREA_COLOR = {"pensiones": TERRA, "ambiente": GREEN, "datos": BLUE, "ia": LILAC, "producto": SAND}
TECH_COLOR = {
    "Python": GREEN, "TypeScript": BLUE, "JavaScript": SAND, "HTML": TERRA, "CSS": LILAC, "React": "#5FB3D9",
    "FastAPI": "#2FA39A", "Streamlit": "#E2545B", "Dash": BLUE, "pandas": LILAC, "Excel": GREEN_SOFT,
    "Next.js": TEXT, "Electron": "#6FA5B8", "Node.js": GREEN, "SQLite": "#7BA7D9", "PostgreSQL": "#6F93C9",
    "PDF": TERRA, "IPC DANE": SAND, "Tkinter": TERRA, "Monte Carlo": SAND,
}


def bg(w, h, rx=20):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{BG}" stroke="{LINE}"/>'


def tech_row(x, y, items, size=13.5, gap=22):
    out = []
    for name in items:
        c = TECH_COLOR.get(name, MUTED)
        out.append(f'<circle cx="{x + 5:.1f}" cy="{y - 4.5:.1f}" r="5" fill="{c}"/>')
        out.append(f'<text x="{x + 16:.1f}" y="{y}" class="sans" font-size="{size}" fill="{MUTED}">{t(name)}</text>')
        x += 16 + text_width(name, size) + gap
    return "".join(out)


def pill(x, y, label, color, anchor_end=False, size=11.5):
    w = text_width(label, size, mono=True) + 22
    if anchor_end:
        x -= w
    return (f'<rect x="{x:.1f}" y="{y - 15}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity=".1" '
            f'stroke="{color}" stroke-opacity=".55"/>'
            f'<text x="{x + w / 2:.1f}" y="{y}" text-anchor="middle" class="mono" font-size="{size}" fill="{color}" '
            f'letter-spacing=".4">{t(label)}</text>')


def lines(x, y, text, width, size, color, lh, cls="sans", extra=""):
    out = []
    for i, line in enumerate(textwrap.wrap(text, width)):
        out.append(f'<text x="{x}" y="{y + i * lh}" class="{cls}" font-size="{size}" fill="{color}"{extra}>{t(line)}</text>')
    return "".join(out)


# --------------------------------------------------------------------------- hero
def mountains(back, back_lit, mid, mid_lit, front, snow):
    return f"""
<path d="M0 230L44 186L84 206L128 132L158 152L200 82L232 122L262 108L300 160L342 142L400 190V380H0Z" fill="{back}"/>
<path d="M200 82L232 122L262 108L300 160L258 186L222 146Z" fill="{back_lit}"/>
<path d="M128 132L158 152L140 178L132 156Z" fill="{back_lit}"/>
<path d="M200 82L180 114L192 109L199 122L208 106L220 116Z" fill="{snow}"/>
<path d="M128 132L114 152L122 149L129 158L136 148L144 147Z" fill="{snow}" opacity=".85"/>
<path d="M262 108L252 122L262 119L270 126L276 118Z" fill="{snow}" opacity=".7"/>
<path d="M0 282L56 232L92 256L140 204L180 240L226 216L276 266L316 246L360 282L400 258V380H0Z" fill="{mid}"/>
<path d="M140 204L180 240L156 262L150 232ZM226 216L276 266L250 276L238 242Z" fill="{mid_lit}"/>
<path d="M140 204L130 220L138 218L143 226L150 214ZM226 216L218 228L226 226L232 233Z" fill="{snow}" opacity=".55"/>
<path d="M0 326L64 296L118 320L180 284L244 324L296 306L350 334L400 318V380H0Z" fill="{front}"/>"""


def hero():
    W, H = 1200, 560
    css = f"""
.w1,.w2,.w3{{opacity:0}}
.cyc{{animation:cyc 12s infinite both}}
@keyframes cyc{{0%{{opacity:0;transform:translateY(8px)}}3%,22%{{opacity:1;transform:translateY(0)}}25%,100%{{opacity:0;transform:translateY(-6px)}}}}
.blink{{animation:blink 1.05s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.hl{{animation:hl 7.5s infinite both}}
@keyframes hl{{0%,16%{{fill:{TERRA}}}22%,100%{{fill:{MUTED}}}}}
.tw{{animation:tw 3.6s ease-in-out infinite both}}
@keyframes tw{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
"""
    reduced = ".cyc,.blink,.hl,.tw{animation:none!important}"

    # top bar
    right = "DESARROLLO · DATOS · IA · PENSIONES · AMBIENTE"
    rw = len(right) * (12 * 0.6 + 2.2)
    body = [bg(W, H, 22),
            f'<radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
            f'gradientTransform="translate(300 280) scale(520 360)"><stop stop-color="{TERRA}" stop-opacity=".09"/>'
            f'<stop offset="1" stop-color="{TERRA}" stop-opacity="0"/></radialGradient>',
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="url(#glow)"/>',
            f'<g class="fade"><rect x="64" y="44" width="9" height="9" fill="{GREEN}"/><rect x="77" y="44" width="9" height="9" fill="{BLUE}"/>'
            f'<rect x="90" y="44" width="9" height="9" fill="{TERRA}"/>'
            f'<text x="112" y="53" class="mono" font-size="13" letter-spacing="3" fill="{TEXT}">JAVIER VALENCIA</text>'
            f'<circle cx="{1136 - rw - 12:.0f}" cy="48.5" r="4.5" fill="{TERRA}" class="tw"/>'
            f'<text x="1136" y="53" text-anchor="end" class="mono" font-size="12" letter-spacing="2.2" fill="{MUTED}">{t(right)}</text></g>',
            f'<path d="M64 84H1136" stroke="{LINE}"/>',
            f'<path d="M64 84H152" stroke="{TERRA}" stroke-width="3" class="draw" style="--len:88;stroke-dasharray:88"/>',
            f'<path d="M162 84H180" stroke="{DIM}" stroke-width="3"/>']

    # headline
    body.append(f"""
<linearGradient id="shine" x1="150" y1="0" x2="520" y2="0" gradientUnits="userSpaceOnUse">
  <stop stop-color="{TERRA}"/><stop offset=".5" stop-color="#F3A57E"/><stop offset="1" stop-color="{TERRA}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-560 0;-560 0;620 0" keyTimes="0;.55;1" dur="6s" repeatCount="indefinite"/>
</linearGradient>
<g class="up" style="animation-delay:.05s"><text x="64" y="146" class="mono" font-size="13" letter-spacing="2.5" fill="{TERRA}">PRODUCT BUILDER · COLOMBIA</text></g>
<g class="up" style="animation-delay:.15s"><text x="62" y="228" class="sans" font-size="72" font-weight="700" letter-spacing="-1.6" fill="{TEXT}">Soluciones reales</text></g>
<g class="up" style="animation-delay:.3s"><text x="62" y="308" class="sans" font-size="72" font-weight="700" letter-spacing="-1.6" fill="{TEXT}">con <tspan fill="url(#shine)">tecnología</tspan><tspan fill="{TERRA}">.</tspan></text></g>""")

    para = ("Combino mi experiencia en pensiones, gestión ambiental y análisis de datos con el desarrollo "
            "de software e inteligencia artificial para crear herramientas que simplifican procesos y "
            "generan valor en el mundo real.")
    body.append(f'<g class="up" style="animation-delay:.45s">{lines(64, 362, para, 56, 19, MUTED, 29)}</g>')

    # cycling focus line
    prefix = "› soluciones para "
    px = 64 + text_width(prefix, 15, mono=True)
    words = [("pensiones y seguridad social", TERRA), ("gestión ambiental", GREEN_SOFT),
             ("análisis de datos", "#7FA3F5"), ("automatización con IA", TEXT)]
    cyc = [f'<g class="up" style="animation-delay:.6s"><rect x="56" y="470" width="610" height="34" rx="8" fill="{PANEL}" stroke="{LINE_SOFT}"/>'
           f'<text x="68" y="492" class="mono" font-size="15" fill="{DIM}">{t(prefix)}</text>']
    for i, (word, color) in enumerate(words):
        cx = px + 4 + text_width(word, 15, mono=True) + 4
        cyc.append(f'<g class="cyc w{i}" style="animation-delay:{i * 3}s"><text x="{px + 4:.0f}" y="492" class="mono" font-size="15" '
                   f'fill="{color}">{t(word)}</text><rect x="{cx:.0f}" y="479" width="8" height="17" fill="{color}" class="blink"/></g>')
    cyc.append("</g>")
    body.append("".join(cyc))

    # artwork: duotone mountains + colour squares
    ax, ay, aw, ah = 736, 112, 400, 380
    squares = [(256, 176, BLUE, 0), (240, 192, GREEN, .6), (256, 192, TEXT, 1.4), (224, 208, BLUE, 2.1),
               (240, 208, TERRA, .9), (256, 208, GREEN_SOFT, 1.8), (208, 224, TEXT, 2.6), (240, 224, BLUE, .3),
               (360, 196, TEXT, 1.1), (376, 212, BLUE, 2.4), (344, 212, GREEN_SOFT, .4)]
    sq = "".join(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{c}" class="tw" style="animation-delay:{d}s"/>'
                 for x, y, c, d in squares)
    labels = ["IDEAS", "DATOS", "HERRAMIENTAS", "PERSONAS", "IMPACTO"]
    lab = "".join(f'<text x="282" y="{34 + i * 18}" class="mono hl" font-size="11" letter-spacing="2" fill="{MUTED}" '
                  f'style="animation-delay:{i * 1.5 - 7.5}s">{x}</text>' for i, x in enumerate(labels))
    body.append(f"""
<defs>
  <clipPath id="art"><rect width="{aw}" height="{ah}" rx="6"/></clipPath>
  <clipPath id="panel"><rect x="272" y="176" width="128" height="204"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#151C26"/><stop offset="1" stop-color="#2C3746"/></linearGradient>
  <linearGradient id="mist" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{TEXT}" stop-opacity="0"/><stop offset=".5" stop-color="{TEXT}" stop-opacity=".07"/><stop offset="1" stop-color="{TEXT}" stop-opacity="0"/></linearGradient>
  <pattern id="dots" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".75" fill="#000" fill-opacity=".3"/></pattern>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>
<g transform="translate({ax} {ay})"><g class="fade" style="animation-delay:.2s"><g clip-path="url(#art)">
  <rect width="{aw}" height="{ah}" fill="url(#sky)"/>
  <circle cx="74" cy="84" r="22" fill="{TERRA}" fill-opacity=".85"/>
  {mountains("#3C4858", "#4E5B6C", "#2A3441", "#364252", "#161B22", "#E9E3D8")}
  <rect y="230" width="{aw}" height="80" fill="url(#mist)"/>
  <g clip-path="url(#panel)"><rect x="272" y="176" width="128" height="204" fill="{TERRA}"/>
  {mountains("#C25B35", "#CF6B44", "#A84B2B", "#B65633", "#7E3519", "#F6C7A6")}</g>
  <rect width="{aw}" height="{ah}" fill="url(#dots)"/>
  <rect width="{aw}" height="{ah}" filter="url(#grain)" opacity=".13"/>
  {sq}
  {lab}
</g><rect x=".5" y=".5" width="{aw - 1}" height="{ah - 1}" rx="6" stroke="{LINE}"/></g></g>
<text x="{ax}" y="524" class="mono" font-size="11" letter-spacing="2.5" fill="{DIM}">TECNOLOGÍA PARA PROBLEMAS REALES</text>
<path d="M1124 519H1136M1130 513V525" stroke="{MUTED}" stroke-width="1.4"/>""")
    write("hero.svg", svg(W, H, "\n".join(body), "Javier Valencia — Soluciones reales con tecnología",
                          "Portada editorial: titular animado, áreas de trabajo y una ilustración de montañas en duotono terracota con cuadros de color.",
                          css, reduced))


# --------------------------------------------------------------------------- buttons
def button(name, label, kind, glyph, w=264, h=56):
    primary = kind == "primary"
    fill, stroke, fg = (TERRA, TERRA, "#FFF7EF") if primary else (PANEL, "#3A404A", TEXT)
    tw = text_width(label, 17, bold=True)
    gx = (w - (20 + 12 + tw)) / 2
    g = github_mark(gx, h / 2 - 10, 20, fg) if glyph == "github" else icon(glyph, gx, h / 2 - 10, 20, fg, 1.8)
    css = """.sh{animation:sh 6s ease-in-out infinite}@keyframes sh{0%,70%{transform:translateX(-120px)}100%{transform:translateX(320px)}}"""
    shine = (f'<clipPath id="c"><rect width="{w}" height="{h}" rx="10"/></clipPath><g clip-path="url(#c)">'
             f'<rect class="sh" x="0" y="-10" width="40" height="{h + 20}" fill="#fff" fill-opacity=".14" transform="skewX(-20)"/></g>') if primary else ""
    body = (f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{shine}'
            f'{g}<text x="{gx + 32:.1f}" y="{h / 2 + 6}" class="sans" font-size="17" font-weight="600" fill="{fg}">{t(label)}</text>')
    write(f"btn-{name}.svg", svg(w, h, body, label, css=css, reduced=".sh{animation:none!important;display:none}"))


# --------------------------------------------------------------------------- focus areas
def focus():
    W, H = 1200, 290
    cards = [
        ("users", TERRA, "Pensiones", "Asesoría, análisis normativo y herramientas para una mejor toma de decisiones.", "COLPENSIONES · RAIS · CETIL"),
        ("leaf", GREEN, "Ambiente", "Gestión ambiental, análisis de información y soluciones digitales para el territorio.", "TERRITORIO · CONSULTORÍA"),
        ("chart", BLUE, "Datos", "Análisis, visualización y automatización de procesos con Python y herramientas modernas.", "PYTHON · PANDAS · DASH"),
        ("sparkles", LILAC, "Inteligencia Artificial", "Exploración y desarrollo de soluciones con IA para problemas concretos.", "LLM · AGENTES · PROMPTS"),
    ]
    body = [bg(W, H)]
    cw, gap, x0, y0, ch = 282, 12, 24, 24, 242
    for i, (ic, color, title, desc, tags) in enumerate(cards):
        x = x0 + i * (cw + gap)
        body.append(f'<g class="up" style="animation-delay:{.1 + i * .12:.2f}s"><g transform="translate({x} {y0})">'
                    f'<rect x=".5" y=".5" width="{cw - 1}" height="{ch - 1}" rx="14" fill="{PANEL}" stroke="{LINE_SOFT}"/>'
                    f'<path d="M24 .5H72" stroke="{color}" stroke-width="3"/>'
                    f'{icon(ic, 24, 26, 30, color)}'
                    f'<text x="24" y="98" class="sans" font-size="21" font-weight="700" fill="{TEXT}">{t(title)}</text>'
                    f'{lines(24, 128, desc, 31, 15, MUTED, 22)}'
                    f'<text x="24" y="220" class="mono" font-size="10.5" letter-spacing="1.4" fill="{DIM}">{t(tags)}</text>'
                    f'{icon("arrow", cw - 42, 206, 18, color, 2)}</g></g>')
    write("focus.svg", svg(W, H, "".join(body), "Áreas de trabajo: Pensiones, Ambiente, Datos e Inteligencia Artificial"))


# --------------------------------------------------------------------------- section header
def section(name, index, title, meta):
    W, H = 1200, 92
    body = (f'{bg(W, H, 16)}'
            f'<g class="up"><text x="40" y="38" class="mono" font-size="12" letter-spacing="2.5" fill="{TERRA}">{t(index)}</text>'
            f'<text x="40" y="70" class="sans" font-size="28" font-weight="700" letter-spacing="-.4" fill="{TEXT}">{t(title)}</text></g>'
            f'<text x="1160" y="70" text-anchor="end" class="mono fade" font-size="12" letter-spacing="1.6" fill="{MUTED}" style="animation-delay:.3s">{t(meta)}</text>'
            )
    write(f"section-{name}.svg", svg(W, H, body, title))


# --------------------------------------------------------------------------- featured project
def featured():
    W, H = 1200, 340
    name = "AppIndemnizaciones"
    nw = text_width(name, 30, bold=True)
    desc = ("Aplicación administrativa para apoyar la liquidación de la Indemnización Sustitutiva de Vejez: "
            "histórico IPC, extracción de certificados CETIL, normalización anual y cálculos trazables con exportación a Excel.")
    chips = ["IPC histórico", "Certificados CETIL", "Revisión manual", "Exportación Excel"]
    cx, chip_svg = 40, []
    for c in chips:
        w = text_width(c, 13) + 26
        chip_svg.append(f'<rect x="{cx:.0f}" y="238" width="{w:.0f}" height="28" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
                        f'<text x="{cx + 13:.0f}" y="257" class="sans" font-size="13" fill="{TEXT}">{t(c)}</text>')
        cx += w + 8

    # stylised product screenshot
    ux, uy, uw, uh = 640, 30, 520, 280
    nav = "".join(f'<rect x="16" y="{62 + i * 24}" width="{[70, 58, 76, 52, 64][i]}" height="7" rx="3.5" fill="{TEXT if i == 0 else DIM}" fill-opacity="{1 if i == 0 else .5}"/>'
                  for i in range(5))
    fields = ""
    for i, (lab, val) in enumerate([("Fecha de nacimiento", "1958-04-12"), ("Semanas cotizadas", "842,57"),
                                    ("Salario base (IBL)", "$ 2.184.300"), ("Año de liquidación", "2026")]):
        fx, fy = 132 + (i % 2) * 184, 74 + (i // 2) * 52
        fields += (f'<text x="{fx}" y="{fy}" class="sans" font-size="9.5" fill="{DIM}">{t(lab)}</text>'
                   f'<rect x="{fx}" y="{fy + 6}" width="172" height="26" rx="5" fill="#0C0F13" stroke="{LINE}"/>'
                   f'<text x="{fx + 10}" y="{fy + 23}" class="mono" font-size="11" fill="{TEXT}">{t(val)}</text>')
    chart = (f'<rect x="132" y="186" width="356" height="70" rx="6" fill="#0C0F13" stroke="{LINE}"/>'
             f'<text x="144" y="202" class="sans" font-size="9.5" fill="{DIM}">IPC acumulado</text>'
             f'<path d="M144 246L184 240L224 236L264 229L304 222L344 212L384 205L424 194L476 184V250H144Z" fill="{BLUE}" fill-opacity=".14"/>'
             f'<path d="M144 246L184 240L224 236L264 229L304 222L344 212L384 205L424 194L476 184" stroke="{TERRA}" stroke-width="2" '
             f'class="draw" style="--len:360;stroke-dasharray:360;animation-delay:.6s"/>')
    ui = (f'<g class="up" style="animation-delay:.25s"><g transform="translate({ux} {uy})">'
          f'<rect x=".5" y=".5" width="{uw - 1}" height="{uh - 1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
          f'<path d="M1 34H{uw - 1}" stroke="{LINE}"/>'
          f'<circle cx="18" cy="17" r="4.5" fill="{TERRA}"/><circle cx="32" cy="17" r="4.5" fill="{SAND}"/><circle cx="46" cy="17" r="4.5" fill="{GREEN}"/>'
          f'<rect x="170" y="10" width="180" height="14" rx="7" fill="#0C0F13"/><text x="260" y="21" text-anchor="middle" class="mono" font-size="9" fill="{DIM}">localhost:8050</text>'
          f'<path d="M116 35V{uh - 1}" stroke="{LINE}"/>{nav}'
          f'<text x="132" y="56" class="sans" font-size="13" font-weight="700" fill="{TEXT}">Calcula la indemnización sustitutiva</text>'
          f'{fields}{chart}'
          f'<rect x="{uw - 116}" y="44" width="100" height="22" rx="6" fill="{BLUE_BTN}"/><text x="{uw - 66}" y="59" text-anchor="middle" class="sans" font-size="10.5" font-weight="600" fill="#fff">Calcular</text>'
          f'</g></g>')
    body = (f'{bg(W, H)}<g class="up">{icon("book", 40, 38, 30, TERRA)}'
            f'<text x="84" y="64" class="sans" font-size="30" font-weight="700" letter-spacing="-.4" fill="{TEXT}">{name}</text>'
            f'{pill(84 + nw + 16, 58, "Público", GREEN_SOFT)}'
            f'<text x="40" y="104" class="mono" font-size="11.5" letter-spacing="2" fill="{TERRA}">PROYECTO DESTACADO · PENSIONES</text>'
            f'{lines(40, 138, desc, 66, 16.5, MUTED, 25)}{"".join(chip_svg)}'
            f'{tech_row(40, 308, ["Python", "Dash", "pandas", "PDF", "Excel"])}</g>{ui}')
    write("project-featured.svg", svg(W, H, body, "AppIndemnizaciones — proyecto destacado",
                                      "Tarjeta del proyecto AppIndemnizaciones con una vista ilustrada de la aplicación."))


BLUE_BTN = "#2F62D9"


# --------------------------------------------------------------------------- project cards
PROJECTS = [
    ("cetilia", "CETILIA", False, "pensiones", "PENSIONES · ARQUITECTURA",
     "Evaluación trazable de historias laborales y decisiones pensionales con dominio puro y pruebas por módulo.",
     ["Python", "FastAPI", "React"]),
    ("apppensional", "AppPensional", False, "pensiones", "PENSIONES · ESTUDIOS",
     "Extrae historias laborales, analiza semanas cotizadas, estima IBL y mesada y genera informes en Excel.",
     ["Python", "Streamlit", "Excel"]),
    ("historias360", "AppHistorias360", False, "pensiones", "PENSIONES · AUDITORÍA",
     "Auditoría de PDFs de historia laboral de Colpensiones, Porvenir y Protección en un solo producto web.",
     ["Python", "TypeScript", "PDF"]),
    ("appafp", "AppAFP", False, "pensiones", "PENSIONES · FONDOS PRIVADOS",
     "Analiza semanas en fondos privados, detecta inconsistencias y estima favorabilidad RAIS vs RPM.",
     ["JavaScript", "Python", "SQLite"]),
    ("deflacion", "Deflactor Pensional", False, "datos", "DATOS · IPC",
     "Lleva valores monetarios entre fechas con el IPC del DANE. Determinístico, trazable y 100 % local.",
     ["Python", "IPC DANE"]),
    ("mundial", "WC26 Intelligence", False, "datos", "DATOS · MODELOS PREDICTIVOS",
     "Seguimiento y predicción del Mundial 2026 con Elo, Poisson y simulaciones Monte Carlo.",
     ["TypeScript", "FastAPI", "PostgreSQL"]),
    ("pdflow", "PDFlow", False, "producto", "ESCRITORIO · DOCUMENTOS",
     "Suite de herramientas PDF portables para Windows: sin instalación, sin red y sin perder calidad.",
     ["TypeScript", "React"]),
    ("extracta", "EXTRACTA", False, "producto", "ESCRITORIO · LECTURA",
     "Lector editorial multiformato (EPUB, MOBI, PDF) para Windows. Sin conexión y con privacidad total.",
     ["Electron", "JavaScript"]),
    ("aidev", "AI Dev Console", False, "ia", "IA · HERRAMIENTAS DE DESARROLLO",
     "Panel local y cifrado para gobernar asistentes de código: modelos, credenciales y lanzadores.",
     ["Node.js", "JavaScript"]),
]


def card(slug, name, public, area, kicker, desc, tech):
    W, H = 400, 226
    color = AREA_COLOR[area]
    status = pill(W - 22, 44, "Público" if public else "Privado", GREEN_SOFT if public else TERRA, anchor_end=True, size=11)
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{LINE}"/>'
            f'<path d="M24 .5H88" stroke="{color}" stroke-width="3"/>'
            f'<g class="up">{icon("book" if public else "lock", 24, 27, 22, color, 1.8)}'
            f'<text x="56" y="45" class="sans" font-size="20" font-weight="700" letter-spacing="-.2" fill="{TEXT}">{t(name)}</text>'
            f'{status}'
            f'<text x="24" y="80" class="mono" font-size="10.5" letter-spacing="1.6" fill="{DIM}">{t(kicker)}</text>'
            f'{lines(24, 110, desc, 44, 15, MUTED, 22)}'
            f'<path d="M24 172.5H{W - 24}" stroke="{LINE_SOFT}"/>'
            f'{tech_row(24, 203, tech, 13, 18)}</g>')
    write(f"card-{slug}.svg", svg(W, H, body, f"{name} — {desc}"))


# --------------------------------------------------------------------------- contact
def contact():
    W, H = 1200, 270
    text = ("Si te interesa colaborar en proyectos, tienes una idea o simplemente quieres conversar sobre "
            "tecnología, pensiones, medio ambiente o IA, estaré encantado de hablar contigo.")
    quote = "“La tecnología tiene más sentido cuando resuelve problemas reales de personas reales.”"
    sq = "".join(f'<rect x="{1112 + (i % 3) * 14}" y="{30 + (i // 3) * 14}" width="10" height="10" fill="{c}" class="tw" style="animation-delay:{i * .5}s"/>'
                 for i, c in enumerate([GREEN, BLUE, TERRA, BLUE, TERRA, GREEN]))
    body = (f'{bg(W, H)}'
            f'<g class="up"><text x="56" y="62" class="mono" font-size="12" letter-spacing="2.5" fill="{TERRA}">04 — CONTACTO</text>'
            f'<text x="56" y="108" class="sans" font-size="38" font-weight="700" letter-spacing="-.8" fill="{TEXT}">Conectemos</text>'
            f'{lines(56, 150, text, 62, 18, MUTED, 28)}</g>'
            f'<path d="M760 64V210" stroke="{TERRA}" stroke-width="2.5" class="draw" style="--len:146;stroke-dasharray:146;animation-delay:.3s"/>'
            f'<g class="up" style="animation-delay:.4s">{lines(792, 98, quote, 34, 22, TEXT, 34, extra=" font-style=\"italic\"")}'
            f'<text x="792" y="206" class="mono" font-size="11.5" letter-spacing="2.5" fill="{DIM}">— JAVIER VALENCIA</text></g>{sq}')
    css = ".tw{animation:tw 3.6s ease-in-out infinite both}@keyframes tw{0%,100%{opacity:1}50%{opacity:.3}}"
    write("contact.svg", svg(W, H, body, "Conectemos", css=css, reduced=".tw{animation:none!important}"))


if __name__ == "__main__":
    hero()
    button("proyectos", "Ver mis proyectos", "primary", "github")
    button("contacto", "Contáctame", "secondary", "mail")
    button("web", "javiervalencia.pro", "primary", "globe")
    button("pensiotech", "PensioTech", "secondary", "rocket")
    button("github", "@Javiervalenciam", "secondary", "github")
    focus()
    section("proyectos", "01 — PORTAFOLIO", "Proyectos destacados", "10 DE 30 REPOSITORIOS")
    section("catalogo", "02 — CATÁLOGO", "Todos los repositorios", "10 PÚBLICOS · 20 PRIVADOS")
    featured()
    for p in PROJECTS:
        card(*p)
    contact()
