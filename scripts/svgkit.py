"""Shared palette, typography, icons and helpers for the profile SVGs."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Palette ------------------------------------------------------------------
BG = "#0F1216"        # ink background
PANEL = "#14181D"     # card surface
LINE = "#262B33"      # borders / rules
LINE_SOFT = "#1D2229"
TEXT = "#F2EDE4"      # warm paper white
MUTED = "#ABA49A"
DIM = "#6F6A63"
TERRA = "#D2693F"     # terracota
TERRA_DEEP = "#B4532E"
BLUE = "#4C7DF0"
BLUE_DEEP = "#2148B8"
GREEN = "#34B27F"
GREEN_SOFT = "#46D7A1"
SAND = "#E8B84A"
LILAC = "#8A6FD1"

SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, Menlo, monospace"

BASE_CSS = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.up{{animation:up .9s cubic-bezier(.2,.7,.2,1) both}}
.fade{{animation:fade 1.2s ease both}}
.draw{{animation:draw 1.6s cubic-bezier(.6,0,.2,1) both}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes draw{{from{{stroke-dashoffset:var(--len,400)}}to{{stroke-dashoffset:0}}}}
"""

REDUCED = "@media (prefers-reduced-motion:reduce){.up,.fade,.draw{animation:none!important}%s}"

# Lucide-style 24x24 stroke icons ------------------------------------------
ICONS = {
    "users": ['<circle cx="9" cy="7" r="4"/>', '<path d="M2 21v-2a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v2"/>',
              '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>', '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'],
    "leaf": ['<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>',
             '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>'],
    "chart": ['<path d="M3 3v18h18"/>', '<path d="M8 17v-5"/>', '<path d="M13 17V8"/>', '<path d="M18 17v-9"/>'],
    "sparkles": ['<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9Z"/>',
                 '<path d="M5 3v4"/>', '<path d="M3 5h4"/>', '<path d="M19 17v4"/>', '<path d="M17 19h4"/>'],
    "book": ['<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>',
             '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'],
    "lock": ['<rect x="3" y="11" width="18" height="11" rx="2"/>', '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'],
    "mail": ['<rect x="2" y="4" width="20" height="16" rx="2"/>', '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'],
    "globe": ['<circle cx="12" cy="12" r="10"/>', '<path d="M2 12h20"/>',
              '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'],
    "arrow": ['<path d="M5 12h14"/>', '<path d="m12 5 7 7-7 7"/>'],
    "activity": ['<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'],
    "rocket": ['<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>',
               '<path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>',
               '<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>', '<path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>'],
    "layers": ['<path d="m12 2 10 5-10 5L2 7z"/>', '<path d="m2 17 10 5 10-5"/>', '<path d="m2 12 10 5 10-5"/>'],
    "star": ['<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>'],
    "calendar": ['<rect x="3" y="4" width="18" height="18" rx="2"/>', '<path d="M16 2v4"/>', '<path d="M8 2v4"/>', '<path d="M3 10h18"/>'],
    "code": ['<path d="m16 18 6-6-6-6"/>', '<path d="m8 6-6 6 6 6"/>'],
}

GITHUB_MARK = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94"
               "-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07"
               "-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27"
               ".68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95"
               ".29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z")


def icon(name, x, y, size=28, color=TERRA, width=1.7):
    s = size / 24
    body = "".join(ICONS[name])
    return (f'<g transform="translate({x} {y}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{width / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{body}</g>')


def github_mark(x, y, size=20, color=TEXT):
    return f'<path transform="translate({x} {y}) scale({size / 16:.4f})" fill="{color}" d="{GITHUB_MARK}"/>'


def t(text):
    return escape(text, quote=True)


_NARROW = set("iljtfr.,:;'!|() ")
_WIDE = set("mwMW@%")


def text_width(text, size, bold=False, mono=False):
    """Rough advance-width estimate; good enough to place pills and cursors."""
    if mono:
        return len(text) * size * 0.6
    w = 0.0
    for ch in text:
        if ch in _NARROW:
            w += 0.30
        elif ch in _WIDE:
            w += 0.86
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        else:
            w += 0.53
    return w * size * (1.06 if bold else 1.0)


def svg(width, height, body, title, desc="", css="", reduced=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-labelledby="t d" fill="none">\n'
            f'<title id="t">{t(title)}</title><desc id="d">{t(desc or title)}</desc>\n'
            f'<style>{BASE_CSS}{css}{REDUCED % reduced}</style>\n{body}\n</svg>\n')


def write(name, content):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8")
    print("wrote", name)
