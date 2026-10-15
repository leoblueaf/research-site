#!/usr/bin/env python3
"""Generate the research-section figures as theme-aware inline SVG.

Colours come from CSS variables set by the page (--app = visible / teal,
--app2 = hidden / violet, --ink, --muted, --line, --paper), so every figure
follows light and dark mode automatically. Figures must be INLINED into the
page (not <img>) for the variables to apply. Run: python3 make_figures.py
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)


def svg(w, h, body, label):
    return (f'<svg class="rs-fig" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- 1. the filter (hero)
def fig_filter():
    m, t = 6, 2
    W, H = 520, 410
    row_h = 46
    base_y = 340
    cx = 250
    gap = 19
    parts = []
    # veil band between order t and t+1
    vy = base_y - (t + 0.5) * row_h
    parts.append('<defs><linearGradient id="rsVeil" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0" stop-color="var(--app2)" stop-opacity="0.03"/>'
                 '<stop offset="1" stop-color="var(--app2)" stop-opacity="0.15"/></linearGradient>'
                 '<radialGradient id="rsGlow" cx="0.5" cy="0.5" r="0.5">'
                 '<stop offset="0" stop-color="var(--app2)" stop-opacity="0.35"/>'
                 '<stop offset="1" stop-color="var(--app2)" stop-opacity="0"/></radialGradient></defs>')
    y_top = base_y - m * row_h - 24
    parts.append(f'<rect x="20" y="{y_top:.1f}" width="460" height="{vy - y_top:.1f}" rx="14" fill="url(#rsVeil)"/>')
    parts.append(f'<line x1="20" y1="{vy:.1f}" x2="480" y2="{vy:.1f}" class="rs-veil"/>')
    for k in range(m + 1):
        n = math.comb(m, k)
        y = base_y - k * row_h
        x0 = cx - (n - 1) * gap / 2
        hidden = k > t
        for i in range(n):
            x = x0 + i * gap
            if hidden:
                parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="11" fill="url(#rsGlow)"/>')
                parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="6" class="rs-hid"/>')
            else:
                parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="6.5" class="rs-vis"/>')
        parts.append(f'<text x="4" y="{y + 5}" class="rs-t rs-small">{k}</text>')
    parts.append(f'<text x="4" y="{base_y - m * row_h - 26}" class="rs-t rs-small rs-muted">size of pattern</text>')
    ly = base_y + 38
    parts.append(f'<circle cx="40" cy="{ly - 5}" r="6.5" class="rs-vis"/>')
    parts.append(f'<text x="54" y="{ly}" class="rs-t rs-small rs-vislab">visible to depth 2: 22</text>')
    parts.append(f'<circle cx="262" cy="{ly - 5}" r="6" class="rs-hid"/>')
    parts.append(f'<text x="276" y="{ly}" class="rs-t rs-small rs-hidlab">hidden kernel: 42</text>')
    return svg(W, H, "".join(parts),
               "The 64 patterns of six switches, arranged by size. A depth-two observer sees the 22 patterns "
               "of size zero, one and two. The 42 larger patterns above the line are hidden from it.")


# ---------------------------------------------------------------- 2. three coins
def fig_coins():
    W, H = 520, 330
    p = []
    # left: pairs
    p.append('<text x="20" y="28" class="rs-t rs-h">Any two coins</text>')
    p.append('<text x="20" y="50" class="rs-t rs-small rs-muted">all four outcomes, equally often</text>')
    combos = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for j, (a, b) in enumerate(combos):
        y = 92 + j * 52
        for i, v in enumerate((a, b)):
            x = 40 + i * 40
            cls = "rs-vis" if v else "rs-coin0"
            p.append(f'<circle cx="{x}" cy="{y}" r="14" class="{cls}"/>')
        p.append(f'<rect x="120" y="{y - 8}" width="70" height="16" rx="8" class="rs-bar0"/>')
        p.append(f'<rect x="120" y="{y - 8}" width="35" height="16" rx="8" class="rs-bar"/>')
        p.append(f'<text x="200" y="{y + 5}" class="rs-t rs-small">25%</text>')
    # right: all three
    p.append('<text x="270" y="28" class="rs-t rs-h">All three together</text>')
    p.append('<text x="270" y="50" class="rs-t rs-small rs-muted">only patterns with an even count</text>')
    pats = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    for j, pat in enumerate(pats):
        col, row = j // 4, j % 4
        x0 = 290 + col * 120
        y = 92 + row * 52
        allowed = sum(pat) % 2 == 0
        g = [] if allowed else ['<g opacity="0.4">']
        for i, v in enumerate(pat):
            cls = ("rs-vis" if allowed else "rs-hidfill") if v else "rs-coin0"
            g.append(f'<circle cx="{x0 + i * 30}" cy="{y}" r="11" class="{cls}"/>')
        if not allowed:
            g.append(f'<line x1="{x0 - 16}" y1="{y + 16}" x2="{x0 + 76}" y2="{y - 16}" class="rs-strike"/></g>')
        p += g
    p.append('<text x="270" y="318" class="rs-t rs-small rs-muted">filled = heads, open = tails</text>')
    return svg(W, H, "".join(p),
               "Three coins. Any two of them look completely random: each of the four outcomes happens a quarter "
               "of the time. But all three together only ever show an even number of heads, so half of the "
               "possible patterns never occur.")


# ---------------------------------------------------------------- 3. the sharp edge
def fig_threshold():
    W, H = 520, 330
    L, R, T, B = 56, 500, 24, 270
    p = []

    def X(u):
        return L + u * (R - L)

    def Y(v):
        return B - v * (B - T)

    # grid
    for v in (0, 0.5, 1):
        p.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" class="rs-grid"/>')
        p.append(f'<text x="{L - 10}" y="{Y(v) + 5:.1f}" text-anchor="end" class="rs-t rs-small rs-muted">{int(v * 100)}%</text>')
    for u in (0, 0.25, 0.5, 0.75, 1):
        lab = {0: "0", 0.25: "¼", 0.5: "½", 0.75: "¾", 1: "1"}[u]
        p.append(f'<text x="{X(u):.1f}" y="{B + 22}" text-anchor="middle" class="rs-t rs-small rs-muted">{lab}</text>')
    p.append(f'<line x1="{X(0.5):.1f}" y1="{T - 6}" x2="{X(0.5):.1f}" y2="{B}" class="rs-half"/>')
    styles = {8: "rs-c1", 32: "rs-c2", 256: "rs-c3"}
    for m, cls in styles.items():
        tot = 2 ** m
        pts = []
        cum = 0  # number of patterns of size <= t
        for t in range(0, m + 1):
            cum += math.comb(m, t)
            hidden = (tot - cum) / tot
            pts.append((t / m, hidden))
        # start at (0, 1) for visual continuity: depth below 0 hides everything
        pts = [(0.0, 1.0)] + pts
        d = "M" + " L".join(f"{X(u):.1f},{Y(v):.1f}" for u, v in pts)
        p.append(f'<path d="{d}" class="rs-curve {cls}"/>')
    p.append(f'<text x="{X(0.18):.1f}" y="{Y(0.62):.1f}" class="rs-t rs-small rs-c1t">8 switches</text>')
    p.append(f'<text x="{X(0.555):.1f}" y="{Y(0.78):.1f}" class="rs-t rs-small rs-c3t">256 switches</text>')
    p.append(f'<text x="{X(0.60):.1f}" y="{Y(0.16):.1f}" class="rs-t rs-small rs-c2t">32</text>')
    p.append(f'<text x="{X(0.5) + 6:.1f}" y="{T + 8}" class="rs-t rs-small rs-muted">half</text>')
    p.append(f'<text x="{(L + R) / 2:.1f}" y="{H - 6}" text-anchor="middle" class="rs-t rs-small">observer depth, as a fraction of the system</text>')
    p.append(f'<text transform="translate(14 {(T + B) / 2:.0f}) rotate(-90)" text-anchor="middle" class="rs-t rs-small">share hidden</text>')
    return svg(W, H, "".join(p),
               "The share of structure hidden from an observer, plotted against its depth as a fraction of the "
               "system size, for systems of 8, 32 and 256 switches. The larger the system, the more sharply the "
               "hidden share drops from nearly all to nearly none at one half.")


# ---------------------------------------------------------------- 4. return to ground
def fig_ground():
    m = 4
    W, H = 560, 230
    p = []
    panel_w = 110
    for s, keep in enumerate((4, 3, 2, 1, 0)):
        ox = 14 + s * panel_w
        for k in range(m + 1):
            n = math.comb(m, k)
            y = 150 - k * 26
            x0 = ox + 48 - (n - 1) * 12 / 2
            for i in range(n):
                cls = "rs-vis" if k <= keep else "rs-gone"
                r = 4.6 if k <= keep else 3.6
                p.append(f'<circle cx="{x0 + i * 12:.1f}" cy="{y}" r="{r}" class="{cls}"/>')
        p.append(f'<text x="{ox + 48}" y="188" text-anchor="middle" class="rs-t rs-small">P<tspan baseline-shift="sub" font-size="75%">{keep}</tspan></text>')
        if s < 4:
            p.append(f'<path d="M{ox + 72} 183 l26 0 m-5 -5 l5 5 l-5 5" class="rs-arrow"/>')
    p.append(f'<text x="{14 + 4 * panel_w + 48}" y="216" text-anchor="middle" class="rs-t rs-small rs-muted">unity</text>')
    return svg(W, H, "".join(p),
               "Erasure in steps. Each step removes the largest remaining patterns, from all of them down to "
               "none, ending at the uniform state where nothing can be told apart.")


if __name__ == "__main__":
    save("filter", fig_filter())
    save("coins", fig_coins())
    save("threshold", fig_threshold())
    save("ground", fig_ground())
    print("wrote", sorted(os.listdir(OUT)))
