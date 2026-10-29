#!/usr/bin/env python3
"""
Render the tech-stack card (stack.svg) in the same terminal-window style as
stats.svg: grouped rows of monochrome icon chips that slide in one after another.
Icons are Simple Icons SVGs in assets/icons/ (single-color, so they take the theme).
Static content -- run by hand when the stack changes.

    python scripts/render_stack_svg.py [output.svg]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, "..", "assets", "icons")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "stack.svg")

BG, BG2, TILE, FRAME = "#0d1117", "#111722", "#161b22", "#30363d"
MUTED, INK, GREEN = "#7d8590", "#c9d1d9", "#39d353"

# (folder, [(label, icon file or None)])  -- None = text monogram
GROUPS = [
    ("languages", [("Python", "python"), ("TypeScript", "typescript"), ("Java", "openjdk"),
                   ("Swift", "swift")]),
    ("frontend", [("React", "react"), ("Tailwind CSS", "tailwindcss"), ("Vite", "vite")]),
    ("data", [("MLflow", "mlflow"), ("Streamlit", "streamlit"),
              ("MySQL", "mysql"), ("SQLite", "sqlite")]),
    ("backend", [("FastAPI", "fastapi"), ("Docker", "docker"), ("Azure", None),
                 ("Git", "git"), ("Linux", "linux")]),
    ("platform", [("Databricks", "databricks"), ("Prometheus", "prometheus"),
                  ("Grafana", "grafana"), ("GitHub Actions", "githubactions")]),
]

W, PAD, TITLEBAR_H = 860, 22, 30
LABEL_W = 150
ROW_H, CHIP_H, CHIP_GAP = 56, 38, 10
CHAR_W = 8.4
H = TITLEBAR_H + PAD + len(GROUPS) * ROW_H + PAD - 8
STAGGER = 0.07


def icon_path(name):
    svg = open(os.path.join(ICONS, name + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>.t{opacity:0;animation:in .45s ease-out both}'
    '@keyframes in{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:translateY(0)}}'
    '@media (prefers-reduced-motion: reduce){.t{opacity:1!important;transform:none!important;animation:none!important}}'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">alex@github: ~$ ls ~/stack</text>')

n = 0
for gi, (folder, items) in enumerate(GROUPS):
    cy = TITLEBAR_H + PAD + gi * ROW_H + CHIP_H / 2
    parts.append(f'<g class="t" style="animation-delay:{n*STAGGER:.2f}s">'
                 f'<text x="{PAD}" y="{cy + 5}" font-size="15" fill="{MUTED}">'
                 f'<tspan fill="{GREEN}">$</tspan> {folder}/</text></g>')
    x = PAD + LABEL_W
    for label, icon in items:
        n += 1
        w = 14 + 22 + 8 + len(label) * CHAR_W + 14
        y = cy - CHIP_H / 2
        if icon:
            glyph = (f'<g transform="translate({x + 14:.1f},{cy - 11:.1f}) scale({22/24:.4f})">'
                     f'<path d="{icon_path(icon)}" fill="{INK}"/></g>')
        else:
            glyph = (f'<text x="{x + 25:.1f}" y="{cy + 6}" font-size="17" font-weight="700" '
                     f'fill="{INK}" text-anchor="middle">A</text>')
        parts.append(
            f'<g class="t" style="animation-delay:{n*STAGGER:.2f}s">'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{CHIP_H}" rx="8" fill="{TILE}" stroke="{FRAME}"/>'
            f'{glyph}'
            f'<text x="{x + 44:.1f}" y="{cy + 5}" font-size="14" fill="{INK}">{label}</text></g>')
        x += w + CHIP_GAP

parts.append("</svg>")
svg = "".join(parts)
open(OUT, "w", encoding="utf-8").write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
