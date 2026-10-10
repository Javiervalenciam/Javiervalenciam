"""Builds the data-driven SVGs (metrics strip, GitHub stats, languages).

With GH_TOKEN set (a token with `repo` scope, so private repositories and
private contributions are counted) it refreshes data/github-stats.json from the
GitHub API; without it, it re-renders from that cached snapshot.

Run:  GH_TOKEN=... python scripts/github_stats.py
"""
import collections
import datetime as dt
import json
import os
import urllib.request

from svgkit import (BG, BLUE, DIM, GREEN, GREEN_SOFT, LILAC, LINE, LINE_SOFT, MUTED, PANEL, ROOT, SAND, TERRA, TEXT,
                    icon, svg, t, write)

USER = "Javiervalenciam"
CACHE = ROOT / "data" / "github-stats.json"
LANG_COLOR = {"Python": GREEN, "TypeScript": BLUE, "JavaScript": SAND, "HTML": TERRA, "CSS": LILAC}
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
HEAT = ["#1A1F27", "#1C3366", "#24499A", "#3567D6", "#86A8F7"]


def api(url, token, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch(token):
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner", token)
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    langs = collections.Counter()
    for r in repos:
        if not r["fork"]:
            langs.update(api(r["languages_url"], token))
    q = "{viewer{contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"
    cal = api("https://api.github.com/graphql", token, {"query": q})["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]
    days = [[d["date"], d["contributionCount"]] for w in cal["weeks"] for d in w["contributionDays"]]
    total = sum(langs.values()) or 1
    return {
        "updated": dt.date.today().isoformat(),
        "repos": len(repos),
        "public": sum(not r["private"] for r in repos),
        "private": sum(r["private"] for r in repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "deployed": sum(bool(r["homepage"]) and not r["fork"] for r in repos),
        "contributions": cal["totalContributions"],
        "languages": [[k, round(100 * v / total, 1)] for k, v in langs.most_common()],
        "days": days,
    }


def metrics(d):
    W, H = 1200, 132
    langs = sum(p >= 2 for _, p in d["languages"])
    items = [("layers", BLUE, d["repos"], "Repositorios", f"{d['public']} PÚBLICOS · {d['private']} PRIVADOS"),
             ("activity", TERRA, d["contributions"], "Contribuciones", "ÚLTIMOS 12 MESES"),
             ("rocket", GREEN, d["deployed"], "Apps desplegadas", "EN PRODUCCIÓN"),
             ("code", SAND, langs, "Lenguajes", "CON USO REAL")]
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{BG}" stroke="{LINE}"/>']
    cw = W / 4
    for i, (ic, color, num, label, sub) in enumerate(items):
        x = i * cw + 40
        if i:
            body.append(f'<path d="M{i * cw:.0f} 30V{H - 30}" stroke="{LINE}"/>')
        body.append(f'<g class="up" style="animation-delay:{i * .12:.2f}s">{icon(ic, x, 44, 34, color, 1.6)}'
                    f'<text x="{x + 54}" y="68" class="sans" font-size="36" font-weight="700" letter-spacing="-.5" fill="{TEXT}">{num}</text>'
                    f'<text x="{x + 54}" y="92" class="sans" font-size="15" fill="{MUTED}">{t(label)}</text>'
                    f'<text x="{x + 54}" y="111" class="mono" font-size="9.5" letter-spacing="1.2" fill="{DIM}">{t(sub)}</text></g>')
    write("metrics.svg", svg(W, H, "".join(body), f"{d['repos']} repositorios, {d['contributions']} contribuciones, "
                                                    f"{d['deployed']} apps desplegadas, {langs} lenguajes"))


def stats(d):
    W, H = 1200, 440
    days = d["days"]
    active = [c for _, c in days if c]
    qs = sorted(active)
    cuts = [qs[int(len(qs) * f)] for f in (.25, .5, .75)] if qs else [1, 2, 3]

    def level(c):
        if not c:
            return 0
        return 1 + sum(c > k for k in cuts)

    tiles = [("Contribuciones", d["contributions"], TERRA), ("Repositorios", d["repos"], BLUE),
             ("Estrellas", d["stars"], SAND), ("Días activos", len(active), GREEN_SOFT)]
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{BG}" stroke="{LINE}"/>',
            f'<g class="up"><text x="40" y="50" class="mono" font-size="12" letter-spacing="2.5" fill="{TERRA}">03 — ACTIVIDAD</text>'
            f'<text x="40" y="86" class="sans" font-size="26" font-weight="700" letter-spacing="-.4" fill="{TEXT}">Estadísticas de GitHub</text>'
            f'<text x="812" y="86" class="sans" font-size="26" font-weight="700" letter-spacing="-.4" fill="{TEXT}">Lenguajes más usados</text></g>',
            f'<path d="M784 40V{H - 70}" stroke="{LINE}"/>']
    for i, (label, num, color) in enumerate(tiles):
        x = 40 + i * 182
        body.append(f'<g class="up" style="animation-delay:{.1 + i * .08:.2f}s"><rect x="{x}" y="108" width="170" height="78" rx="12" fill="{PANEL}" stroke="{LINE_SOFT}"/>'
                    f'<text x="{x + 16}" y="134" class="sans" font-size="13" fill="{MUTED}">{t(label)}</text>'
                    f'<text x="{x + 16}" y="171" class="sans" font-size="30" font-weight="700" fill="{color}">{num}</text></g>')

    # contribution heatmap
    gx, gy, cell, step = 76, 236, 10, 13
    first = dt.date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    cols = collections.defaultdict(list)
    seen_month = set()
    for i, (date, count) in enumerate(days):
        idx = i + offset
        col, row = divmod(idx, 7)
        cols[col].append(f'<rect x="{gx + col * step}" y="{gy + row * step}" width="{cell}" height="{cell}" rx="2" fill="{HEAT[level(count)]}"/>')
        day = dt.date.fromisoformat(date)
        if day.day <= 7 and row == 0 and (day.year, day.month) not in seen_month and col < 52:
            seen_month.add((day.year, day.month))
            body.append(f'<text x="{gx + col * step}" y="{gy - 10}" class="sans" font-size="11" fill="{DIM}">{MONTHS[day.month - 1]}</text>')
    for col, rects in sorted(cols.items()):
        body.append(f'<g class="fade" style="animation-delay:{.2 + col * .018:.3f}s">{"".join(rects)}</g>')
    for row, name in ((1, "Lun"), (3, "Mié"), (5, "Vie")):
        body.append(f'<text x="40" y="{gy + row * step + 9}" class="sans" font-size="10.5" fill="{DIM}">{name}</text>')
    ly = gy + 7 * step + 22
    body.append(f'<text x="40" y="{ly + 9}" class="sans" font-size="11.5" fill="{MUTED}">{d["contributions"]} contribuciones en los últimos 12 meses · incluye repositorios privados</text>')
    lx = 690
    body.append(f'<text x="{lx - 8}" y="{ly + 9}" text-anchor="end" class="sans" font-size="11" fill="{DIM}">Menos</text>')
    for i, c in enumerate(HEAT):
        body.append(f'<rect x="{lx + i * 13}" y="{ly}" width="10" height="10" rx="2" fill="{c}"/>')
    body.append(f'<text x="{lx + 5 * 13 + 4}" y="{ly + 9}" class="sans" font-size="11" fill="{DIM}">Más</text>')

    # languages
    top = d["languages"][:5]
    rest = round(100 - sum(p for _, p in top), 1)
    rows = top + [["Otros", rest]]
    peak = max(p for _, p in rows)
    for i, (name, pct) in enumerate(rows):
        y = 132 + i * 36
        color = LANG_COLOR.get(name, DIM)
        w = 150 * pct / peak
        body.append(f'<g class="up" style="animation-delay:{.15 + i * .08:.2f}s"><circle cx="818" cy="{y - 5}" r="5.5" fill="{color}"/>'
                    f'<text x="834" y="{y}" class="sans" font-size="15" fill="{TEXT}">{t(name)}</text>'
                    f'<rect x="950" y="{y - 9}" width="150" height="8" rx="4" fill="{PANEL}"/>'
                    f'<rect x="950" y="{y - 9}" width="{w:.1f}" height="8" rx="4" fill="{color}" class="grow" style="animation-delay:{.4 + i * .1:.2f}s"/>'
                    f'<text x="1160" y="{y}" text-anchor="end" class="mono" font-size="12.5" fill="{MUTED}">{pct:.1f}%</text></g>')
    x, sy = 812.0, 356
    seg = []
    for name, pct in rows:
        w = 348 * pct / 100
        seg.append(f'<rect x="{x:.1f}" y="{sy}" width="{max(w - 2, 0):.1f}" height="10" fill="{LANG_COLOR.get(name, DIM)}"/>')
        x += w
    body.append(f'<clipPath id="bar"><rect x="812" y="{sy}" width="348" height="10" rx="5"/></clipPath>'
                f'<g clip-path="url(#bar)" class="fade" style="animation-delay:.9s">{"".join(seg)}</g>'
                f'<text x="812" y="{sy - 12}" class="sans" font-size="11.5" fill="{MUTED}">Distribución por bytes de código en {d["repos"]} repositorios</text>')
    body.append(f'<path d="M40 {H - 50}H1160" stroke="{LINE_SOFT}"/>'
                f'<text x="40" y="{H - 24}" class="mono" font-size="10.5" letter-spacing="1.6" fill="{DIM}">'
                f'ACTUALIZADO {d["updated"]} · DATOS DE LA API DE GITHUB · {d["public"]} PÚBLICOS + {d["private"]} PRIVADOS</text>'
                f'<g transform="translate(1110 {H - 34})"><rect width="10" height="10" fill="{GREEN}"/><rect x="14" width="10" height="10" fill="{BLUE}"/><rect x="28" width="10" height="10" fill="{TERRA}"/></g>')
    css = ".grow{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    langs_desc = ", ".join(f"{n} {p}%" for n, p in rows)
    write("github-stats.svg", svg(W, H, "\n".join(body), "Estadísticas de GitHub de Javier Valencia",
                                  f"{d['contributions']} contribuciones, {d['repos']} repositorios, {d['stars']} estrellas. Lenguajes: {langs_desc}.",
                                  css, ".grow{animation:none!important}"))


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN")
    if token:
        data = fetch(token)
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    else:
        data = json.loads(CACHE.read_text(encoding="utf-8"))
    metrics(data)
    stats(data)
