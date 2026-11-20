# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""House-style diagram kit: SVG parts on a fixed grid, the explorer page, and
static SVG files for Markdown on GitHub. Standard library only.

A copy of the diagrams skill's kit, with the page-theme tokens beside it in
diagram_assets/, so the generator and CI build explorers without the skills.
"""

import html
import json
import re
from itertools import pairwise
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "diagram_assets"
THEME_CSS = (ASSETS / "theme.css").read_text(encoding="utf-8")
DIAGRAM_CSS = (ASSETS / "diagram.css").read_text(encoding="utf-8")
EXPLORER_JS = (ASSETS / "explorer.js").read_text(encoding="utf-8")

FAMILIES = ("blue", "violet", "green", "orange", "red", "cyan", "yellow", "neutral")
KINDS = ("src", "proc", "hub")
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,500..800'
    '&family=JetBrains+Mono:wght@400;600;700&family=Public+Sans:wght@400;500;600&display=swap">\n'
)

type Box = tuple[float, float, float, float]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def markers(prefix: str) -> str:
    out = [
        f'<marker id="{prefix}-{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" class="{name}"/></marker>'
        for name in ("ah", "ah-hi")
    ]
    return "<defs>" + "".join(out) + "</defs>"


def node(
    nid: str,
    box: Box,
    fam: str,
    kind: str,
    lines: list[str],
    *,
    label: str | None = None,
    extra: str = "",
    interactive: bool = True,
) -> str:
    """One rounded box. The first line is the name, the others are facts.
    An empty string in lines leaves a blank line, to group facts."""
    if fam not in FAMILIES or kind not in KINDS:
        raise ValueError(
            f"{nid}: family {fam!r} or kind {kind!r} is not in the house style"
        )
    if kind == "hub" and fam != "neutral":
        raise ValueError(f"{nid}: a hub is neutral; a colored box is src or proc")
    x, y, w, h = box
    step = 17
    top = y + h / 2 - (len(lines) - 1) * step / 2 + 5
    texts = "".join(
        f'<text x="{x + w / 2}" y="{top + i * step:.1f}" class="{"nm" if i == 0 else "ft"}">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )
    name = esc(label or ", ".join(line for line in lines if line))
    attrs = (
        f' tabindex="0" role="button" aria-label="Select {name}"' if interactive else ""
    )
    return (
        f'<g class="node fam-{fam} {kind} {extra}" data-id="{nid}"{attrs}>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>{texts}</g>'
    )


def seg(
    sid: str,
    d: str,
    links: list[str],
    prefix: str,
    label: str | None = None,
    at: tuple[float, float] = (0, 0),
    *,
    anchor: str = "middle",
    arrow: bool = True,
    kind: str = "data",
    label2: tuple[str, float, float] | None = None,
) -> str:
    """One wire. links names every "from>to" pair that the wire carries, so a
    merged trunk lists each source that joins it. kind="access" draws a dotted
    request path that a person opens. kind="call" draws the solid request
    half of a two-way exchange. The explorer keeps both out of the closure."""
    marker = f' marker-end="url(#{prefix}-ah)"' if arrow else ""
    out = [f'<g class="edge {kind}" data-seg="{sid}" data-links="{",".join(links)}">']
    out.append(
        f'<path d="{_rounded(d)}" data-route="{d}" class="wire{" arrow" if arrow else ""}"{marker}/>'
    )
    for text, x, y in [(label, *at)] + ([label2] if label2 else []):
        if text:
            out.append(
                f'<text x="{x}" y="{y}" class="elabel" text-anchor="{anchor}">{esc(text)}</text>'
            )
    out.append("</g>")
    return "".join(out)


def note(
    x: float, y: float, text: str, fam: str = "neutral", *, anchor: str = "start"
) -> str:
    """A short note beside a box, in the color of that box. fam="warn" marks
    a warning instead."""
    cls = "warn" if fam == "warn" else f"fam-{fam}"
    return f'<text x="{x}" y="{y}" class="note {cls}" text-anchor="{anchor}">{esc(text)}</text>'


def container(box: Box, label: str) -> str:
    x, y, w, h = box
    return (
        f'<g class="container"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/>'
        f'<text x="{x + 14}" y="{y + 20}" class="clabel">{esc(label)}</text></g>'
    )


def svg(sid: str, size: tuple[int, int], aria: str, body: str, prefix: str) -> str:
    """Draw the wires before the nodes in body, so the boxes paint on top."""
    w, h = size
    return (
        f'<svg id="{sid}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}" '
        f'xmlns="http://www.w3.org/2000/svg">{markers(prefix)}{body}</svg>'
    )


def legend(access: str | None = None) -> str:
    """The three line styles of an explorer. access names the dotted path."""

    def line(stroke: str, extra: str) -> str:
        return (
            '<svg viewBox="0 0 34 10"><line x1="2" y1="5" x2="32" y2="5" '
            f'stroke="var({stroke})" stroke-linecap="round" {extra}/></svg>'
        )

    items = [
        line("--wire-hi", 'stroke-width="3"') + "what the selected part needs",
        line("--wire-hi", 'stroke-width="3" stroke-dasharray="9 7"')
        + "where its data goes",
    ]
    if access:
        items.append(
            line("--wire", 'stroke-width="2.5" stroke-dasharray="1 7"') + esc(access)
        )
    return (
        '<div class="legend" aria-hidden="true">'
        + "".join(f"<span>{i}</span>" for i in items)
        + "</div>"
    )


def page(
    title: str, body: str, data: dict | None = None, *, standalone: bool = False
) -> str:
    """A single-file page with the theme, the diagram CSS and the explorer
    inlined. An artifact gets standalone=False, because the artifact service
    adds the document skeleton. A file for a browser or GitHub Pages gets
    standalone=True, or it renders in quirks mode."""
    blob = json.dumps(data or {}, ensure_ascii=False).replace("</", "<\\/")
    head = f"<title>{esc(title)}</title>\n{FONTS}<style>\n{THEME_CSS}\n{DIAGRAM_CSS}</style>\n"
    tail = f'<script type="application/json" id="diagram-data">{blob}</script>\n<script>\n{EXPLORER_JS}</script>\n'
    if not standalone:
        return (
            head
            + '<meta name="claude:viewport-fit-sides" content="cover">\n'
            + body
            + tail
        )
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"{head}</head>\n<body>\n{body}\n{tail}</body>\n</html>\n"
    )


def tokens(theme: str = "light") -> dict[str, str]:
    """The color tokens of theme.css, resolved for one theme."""

    def block(selector: str) -> dict[str, str]:
        start = THEME_CSS.index(selector) + len(selector)
        return dict(
            re.findall(
                r"--([\w-]+):\s*([^;]+);",
                THEME_CSS[start : THEME_CSS.index("}", start)],
            )
        )

    light = block(":root {")
    if theme == "light":
        return light
    if theme == "dark":
        return light | block(':root[data-theme="dark"] {')
    raise ValueError(f"theme must be light or dark, not {theme!r}")


def static_svg(markup: str, theme: str = "light") -> str:
    """A standalone SVG file for an <img> or <picture> in Markdown. GitHub
    strips inline SVG and scripts, but it shows an SVG file with its own
    <style>. Web fonts do not load there, so the monospace fallback draws."""
    t = tokens(theme)
    css = re.sub(r"var\(--([\w-]+)\)", lambda m: t[m.group(1)], DIAGRAM_CSS)
    markup = re.sub(
        r' tabindex="0" role="button" aria-label="Select [^"]*"', "", markup
    )
    opening = re.match(r'<svg [^>]*viewBox="0 0 (\S+) (\S+)"[^>]*>', markup)
    if opening is None:
        raise ValueError("static_svg needs the markup that svg() returns")
    w, h = opening.groups()
    # Without a size, an <img> of an SVG shows at the 300 px default width.
    head = opening.group(0).replace("<svg ", f'<svg width="{w}" height="{h}" ', 1)
    background = f'<rect width="100%" height="100%" fill="{t["surface"]}"/>'
    return f"{head}<style>{css}</style>{background}{markup[opening.end() :]}"


type Point = tuple[float, float]

LABEL_CHAR_WIDTH = 7.2
MIN_LAST_LEG = 20
MIN_JOG = 40
CORNER_INSET = 14
_LEAVING = {"right": (1, 0), "left": (-1, 0), "bottom": (0, 1), "top": (0, -1)}


def _points(d: str) -> list[Point] | None:
    """The corners of an absolute M/H/V/L path, or None for anything else."""
    if re.fullmatch(r"\s*M[\d.,\s]+(?:[HVL][\d.,\s]+)*", d) is None:
        return None
    points: list[Point] = []
    for cmd, a, b in re.findall(r"([MHVL])\s*([\d.]+)(?:[,\s]\s*([\d.]+))?", d):
        if cmd in "ML":
            points.append((float(a), float(b)))
        elif cmd == "H":
            points.append((float(a), points[-1][1]))
        else:
            points.append((points[-1][0], float(a)))
    return points


def _sign(v: float) -> int:
    return (v > 0) - (v < 0)


BEND_RADIUS = 10


def _rounded(d: str) -> str:
    """The route d with each right-angle bend drawn as a short curve."""
    pts = _points(d)
    if pts is None or len(pts) < 3:
        return d
    out = [f"M{pts[0][0]:g},{pts[0][1]:g}"]
    for prev, (cx, cy), nxt in zip(pts, pts[1:], pts[2:]):
        r = min(
            BEND_RADIUS,
            (abs(cx - prev[0]) + abs(cy - prev[1])) / 2,
            (abs(nxt[0] - cx) + abs(nxt[1] - cy)) / 2,
        )
        ax, ay = cx - _sign(cx - prev[0]) * r, cy - _sign(cy - prev[1]) * r
        bx, by = cx + _sign(nxt[0] - cx) * r, cy + _sign(nxt[1] - cy) * r
        out.append(f"L{ax:g},{ay:g} Q{cx:g},{cy:g} {bx:g},{by:g}")
    out.append(f"L{pts[-1][0]:g},{pts[-1][1]:g}")
    return " ".join(out)


def _side(box: Box, p: Point) -> str | None:
    """The edge of box that p sits on, clear of the rounded corners."""
    x, y, w, h = box
    if p[0] in (x, x + w) and y + CORNER_INSET <= p[1] <= y + h - CORNER_INSET:
        return "left" if p[0] == x else "right"
    if p[1] in (y, y + h) and x + CORNER_INSET <= p[0] <= x + w - CORNER_INSET:
        return "top" if p[1] == y else "bottom"
    return None


def _crosses(box: Box, a: Point, b: Point) -> bool:
    """Whether segment a-b enters the open interior of box (Liang-Barsky)."""
    x, y, w, h = box
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in (
        (-dx, a[0] - x),
        (dx, x + w - a[0]),
        (-dy, a[1] - y),
        (dy, y + h - a[1]),
    ):
        if p == 0:
            if q <= 0:
                return False
        elif p < 0:
            t0 = max(t0, q / p)
        else:
            t1 = min(t1, q / p)
    return t1 - t0 > 1e-9


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    inside = min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[
        1
    ] <= max(a[1], b[1])
    return abs(cross) < 1e-6 and inside


def check_routes(markup: str) -> list[str]:
    """Geometry faults that the eye catches at once: a wire that starts or
    ends in empty space, an arrow that turns at the box it enters, a short
    jog that aligned boxes would remove, and a wire or label over a box."""
    boxes: dict[str, Box] = {
        nid: (float(x), float(y), float(w), float(h))
        for nid, x, y, w, h in re.findall(
            r'<g class="node [^"]*" data-id="([^"]+)"[^>]*><rect x="([\d.]+)" y="([\d.]+)" '
            r'width="([\d.]+)" height="([\d.]+)"',
            markup,
        )
    }
    edges = re.findall(
        r'<g class="edge [^"]*" data-seg="([^"]+)" data-links="([^"]*)"><path d="[^"]+" data-route="([^"]+)" class="([^"]+)"[^>]*/>(.*?)</g>',
        markup,
    )
    problems: list[str] = []
    routes: dict[str, list[Point]] = {}
    for sid, _, d, _, _ in edges:
        if (pts := _points(d)) is None:
            problems.append(f"{sid}: use only absolute M, H, V and L in a wire path")
        else:
            routes[sid] = pts
    segments = [(sid, a, b) for sid, pts in routes.items() for a, b in pairwise(pts)]

    def joins(sid: str, p: Point) -> bool:
        return any(_on_segment(p, a, b) for other, a, b in segments if other != sid)

    labels: list[tuple[str, Box]] = []
    for sid, links, _, cls, rest in edges:
        if sid not in routes:
            continue
        pts = routes[sid]
        pairs = [k.split(">") for k in links.split(",") if ">" in k]
        start_box = next((n for n, b in boxes.items() if _side(b, pts[0])), None)
        if start_box:
            side = _side(boxes[start_box], pts[0])
            first = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
            if side and (_sign(first[0]), _sign(first[1])) != _LEAVING[side]:
                problems.append(
                    f"{sid} does not leave {start_box} straight out of its {side} edge"
                )
        elif not joins(sid, pts[0]):
            problems.append(
                f"{sid} starts in empty space, not on a box edge or another wire"
            )
        last = (pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
        if "arrow" in cls.split():
            targets = [boxes[t] for _, t in pairs if t in boxes]
            side = next((s for b in targets if (s := _side(b, pts[-1]))), None)
            if side is None:
                problems.append(
                    f"{sid}: the arrow does not end on an edge of its target box, clear of the corners"
                )
            elif (-_sign(last[0]), -_sign(last[1])) != _LEAVING[side]:
                problems.append(
                    f"{sid}: the arrow does not enter straight through the {side} edge"
                )
            if abs(last[0]) + abs(last[1]) < MIN_LAST_LEG:
                problems.append(
                    f"{sid}: the arrow turns {abs(last[0]) + abs(last[1]):.0f} px before the box"
                )
        elif not any(_side(b, pts[-1]) for b in boxes.values()) and not joins(
            sid, pts[-1]
        ):
            problems.append(
                f"{sid} ends in empty space, not on a box edge or another wire"
            )
        for a, b in pairwise(pts[1:-1]):
            if abs(b[0] - a[0]) + abs(b[1] - a[1]) < MIN_JOG:
                problems.append(
                    f"{sid} has a {abs(b[0] - a[0]) + abs(b[1] - a[1]):.0f} px jog; align the boxes"
                )
        for x, y, anchor, text in re.findall(
            r'<text x="([\d.]+)" y="([\d.]+)" class="elabel" text-anchor="(\w+)">([^<]*)</text>',
            rest,
        ):
            width = len(html.unescape(text)) * LABEL_CHAR_WIDTH
            left = float(x) - {"start": 0, "middle": width / 2, "end": width}[anchor]
            labels.append(
                (
                    f"{sid} label {html.unescape(text)!r}",
                    (left - 2, float(y) - 11, width + 4, 15),
                )
            )
    for sid, a, b in segments:
        problems += [
            f"{sid} runs through {nid}"
            for nid, box in boxes.items()
            if _crosses(box, a, b)
        ]
    for name, rect in labels:
        lx, ly, lw, lh = rect
        problems += [
            f"{name} overlaps {nid}"
            for nid, (bx, by, bw, bh) in boxes.items()
            if lx < bx + bw and bx < lx + lw and ly < by + bh and by < ly + lh
        ]
        problems += [
            f"{name} sits on wire {sid}"
            for sid, a, b in segments
            if _crosses(rect, a, b)
        ]
    return problems


def check(markup: str, data: dict) -> list[str]:
    """Mismatches between one explorer svg and its data, and the wire
    geometry faults of check_routes. Each one shows in a browser only as a
    dead chip, an empty card or a broken arrow, so a build script fails on
    them instead."""
    sid = re.match(r'<svg id="([^"]+)"', markup)
    if sid is None:
        return ["the markup does not start with an svg that has an id"]
    entry = data.get(sid.group(1), {})
    nodes = set(re.findall(r'<g class="node [^"]*" data-id="([^"]+)"', markup))
    wires = {
        k
        for group in re.findall(r'data-links="([^"]*)"', markup)
        for k in group.split(",")
    }
    parts = entry.get("parts", {})
    problems = [
        f"wire {k} names a part with no box"
        for k in sorted(wires)
        if not set(k.split(">")) <= nodes
    ]
    problems += [
        f"part {n} has no stops line"
        for n in sorted(nodes)
        if not parts.get(n, {}).get("stops")
    ]
    problems += [
        f"card text for {n}, which has no box" for n in sorted(set(parts) - nodes)
    ]
    if entry.get("select") and entry["select"] not in nodes:
        problems.append(f"select names {entry['select']}, which has no box")
    for key, path in entry.get("paths", {}).items():
        problems += [
            f"path {key} names {k}, which no wire carries"
            for k in path.get("links", [])
            if k not in wires
        ]
    problems += [
        f"links names {k}, which no wire carries"
        for k in entry.get("links", {})
        if k not in wires
    ]
    return problems + check_routes(markup)
