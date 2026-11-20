# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Interactive diagram explorers for the Sphinx pages, built with diagram_kit.

An explorer is an SVG diagram: selecting a part lights what it needs and what
uses it, and a card under it explains the part. Pages embed one through
fragment(). write_static_assets() writes the CSS and the script that every
page loads (docs/sphinx/conf.py lists them).
"""

import html
import json
import re
from pathlib import Path

from . import diagram_kit as dk
from ._shared import mermaid_init, write_text_lf

_SCOPE = ".kx"
_TONES = ("blue", "violet", "green", "orange", "red", "cyan", "yellow")

# GitHub hides HTML comments and conf.py's source-read hook swaps the two
# blocks, so GitHub shows the Mermaid fallback and Sphinx shows the explorer.
GITHUB_ONLY = ("<!-- github-only -->", "<!-- /github-only -->")
SPHINX_ONLY = ("<!-- sphinx-only", "-->")

# family: (strong fill, pale fill, border, text), from the diagrams skill palette
_MERMAID_COLORS = {
    "blue": ("#a5d8ff", "#e7f5ff", "#1971c2", "#1864ab"),
    "violet": ("#d0bfff", "#f3f0ff", "#7048e8", "#5f3dc4"),
    "green": ("#b2f2bb", "#ebfbee", "#2f9e44", "#2b8a3e"),
    "orange": ("#ffd8a8", "#fff4e6", "#e8590c", "#d9480f"),
    "red": ("#ffc9c9", "#fff5f5", "#e03131", "#c92a2a"),
    "cyan": ("#99e9f2", "#e3fafc", "#1098ad", "#0b7285"),
    "yellow": ("#ffec99", "#fff9db", "#f08c00", "#a35a00"),
    "neutral": ("#f8f9fa", "#f8f9fa", "#495057", "#212529"),
}


def _scoped(css: str) -> str:
    """Prefixes every rule outside :root and @keyframes, so the kit cannot restyle the Sphinx theme."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    out = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", css):
        selector, body = match.group(1).strip(), match.group(2)
        if selector.startswith("@keyframes") or ":root" in selector:
            out.append(f"{selector} {{{body}}}")
        elif selector.startswith("@media"):
            out.append(f"{selector} {{{_scoped(body)}}}")
        else:
            prefixed = ", ".join(
                f"{_SCOPE} {part.strip()}" for part in selector.split(",")
            )
            out.append(f"{prefixed} {{{body}}}")
    return "\n".join(out)


def explorer_css() -> str:
    """The theme tokens, the explorer components and the diagram CSS scoped to .kx, and the Mermaid colors."""
    theme = dk.THEME_CSS
    tokens = re.sub(
        r"/\*.*?\*/", "", theme[: theme.index("* { box-sizing")], flags=re.DOTALL
    )
    components = theme[theme.index("/* chips") : theme.index("/* tile board")]
    badges = theme[theme.index(".badge {") : theme.index(".examples {")]
    headings = (
        "h3 { font-size: 1.1rem; margin: 0; } p { margin: 0; } "
        "h4 { margin: 0 0 6px; font: 600 0.72rem/1.3 var(--body); text-transform: uppercase; "
        "letter-spacing: 0.08em; color: var(--muted); }"
    )
    return "\n".join(
        [
            "/* AUTO-GENERATED from scripts/generation/diagram_assets/ by explorer_docs.py. */",
            tokens.strip(),
            _scoped(components + badges + dk.DIAGRAM_CSS + headings),
            f"{_SCOPE} {{ display: grid; gap: 14px; margin: 1.5rem 0; color: var(--fg); }}",
            f"{_SCOPE} .diagram svg {{ min-width: 720px; }}",
            f"{_SCOPE} {{ --tone: var(--fg); --tone-bg: var(--fg); --tone-fg: var(--bg); }}",
            *(
                f'{_SCOPE} [data-tone="{fam}"], {_SCOPE}[data-tone="{fam}"] {{ --tone: var(--{fam}-border); '
                f"--tone-bg: var(--{fam}-strong); --tone-fg: var(--{fam}-text); }}"
                for fam in _TONES
            ),
            f"{_SCOPE} .chip .dot {{ background: var(--tone); }}",
            f"{_SCOPE} .chip:hover:not(:disabled) {{ border-color: var(--tone); }}",
            f'{_SCOPE} .chip[aria-pressed="true"] {{ background: var(--tone-bg); color: var(--tone-fg); border-color: var(--tone); }}',
            f"{_SCOPE}.seq-steps {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0.5rem 0 1.5rem; }}",
            f"{_SCOPE} .seq-nav {{ border-color: var(--tone); }}",
            f"{_SCOPE} .seq-nav:last-child:not(:disabled) {{ background: var(--tone-bg); color: var(--tone-fg); }}",
            f"{_SCOPE} .seq-group {{ display: flex; flex-wrap: wrap; gap: 8px; }}",
            f"{_SCOPE} .seq-group + .seq-group {{ padding-left: 12px; border-left: 1px solid var(--line-strong); }}",
            f"{_SCOPE} .chip:disabled {{ opacity: 0.4; cursor: default; }}",
            (
                f"{_SCOPE} .seq-status {{ flex-basis: 100%; font: 0.85rem/1.4 var(--mono); color: var(--muted); "
                f"border-left: 3px solid var(--tone); padding-left: 8px; }}"
            ),
            (dk.ASSETS / "mermaid.css").read_text(encoding="utf-8").strip(),
            "",
        ]
    )


def write_static_assets(static_dir: Path) -> None:
    static_dir.mkdir(parents=True, exist_ok=True)
    write_text_lf(static_dir / "explorer.css", explorer_css())
    write_text_lf(static_dir / "explorer.js", dk.EXPLORER_JS)
    write_text_lf(
        static_dir / "sequence-steps.js",
        (dk.ASSETS / "sequence-steps.js").read_text(encoding="utf-8"),
    )


def _mermaid_text(raw: str) -> str:
    return html.unescape(raw).replace('"', "#quot;")


def mermaid_fallback(markup: str) -> list[str]:
    """The explorer as a static Mermaid flowchart, for GitHub, which strips inline SVG and scripts.

    A call and its answer become one arrow in the call's direction, labeled
    "request / answer".
    """
    nodes = re.findall(
        r'<g class="node fam-(\w+) (\w+)[^"]*" data-id="([^"]+)"[^>]*>(.*?)</g>', markup
    )
    edges: dict[tuple[str, str], tuple[str, str]] = {}
    for kind, links, body in re.findall(
        r'<g class="edge (\w+)" data-seg="[^"]*" data-links="([^"]*)">(.*?)</g>', markup
    ):
        label = " ".join(re.findall(r'class="elabel"[^>]*>(.*?)</text>', body))
        for link in links.split(","):
            source, target = link.split(">")
            edges[(source, target)] = (kind, label)
    arrows = []
    for (source, target), (kind, label) in edges.items():
        answer = edges.get((target, source))
        if kind != "call" and answer and answer[0] == "call":
            continue
        if kind == "call" and answer:
            label = " / ".join(text for text in (label, answer[1]) if text)
        arrow = f' -->|"{_mermaid_text(label)}"| ' if label else " --> "
        arrows.append(f"  {source}{arrow}{target}")
    lines = ["```mermaid", mermaid_init().replace('"elk"', '"dagre"'), "flowchart TD"]
    used = set()
    for fam, kind, nid, body in nodes:
        texts = [
            _mermaid_text(t) for t in re.findall(r"<text [^>]*>(.*?)</text>", body)
        ]
        cls = f"{fam}{'Src' if kind == 'src' else ''}"
        used.add((cls, fam, kind))
        lines.append(f'  {nid}("{"<br/>".join(texts)}"):::{cls}')
    lines += arrows
    for cls, fam, kind in sorted(used):
        strong, pale, border, text = _MERMAID_COLORS[fam]
        fill = strong if kind == "src" else pale
        lines.append(
            f"  classDef {cls} fill:{fill},stroke:{border},color:{text},stroke-width:2px,rx:10px"
        )
    lines += [
        "  linkStyle default stroke-width:2px,stroke-linecap:round,stroke-linejoin:round",
        "```",
    ]
    return lines


def fragment(
    markup: str,
    data: dict,
    caption: str,
    *,
    access: str | None = None,
    legend: tuple[str, str] | None = None,
) -> list[str]:
    """A Mermaid fallback for GitHub, then a MyST raw-HTML block with the path chips,
    the diagram, the legend and the card, hidden from GitHub in an HTML comment.

    legend renames the bold-line and moving-line entries, for a diagram whose
    arrows mean something other than data flow. Raises ValueError when
    dk.check() finds a mismatch or a geometry fault, so a broken diagram fails
    generation instead of shipping.
    """
    svg_id = re.match(r'<svg id="([^"]+)"', markup)
    if svg_id is None:
        raise ValueError("an explorer needs the markup that diagram_kit.svg() returns")
    sid = svg_id.group(1)
    if problems := dk.check(markup, {sid: data}):
        raise ValueError(f"{sid}: " + "; ".join(problems))
    blob = json.dumps({sid: data}, ensure_ascii=False).replace("</", "<\\/")
    key = dk.legend(access)
    if legend:
        key = key.replace("what the selected part needs", dk.esc(legend[0])).replace(
            "where its data goes", dk.esc(legend[1])
        )
    if SPHINX_ONLY[1] in markup + blob + key + caption:
        raise ValueError(f"{sid}: the explorer cannot sit in an HTML comment")
    return [
        GITHUB_ONLY[0],
        "",
        *mermaid_fallback(markup),
        "",
        GITHUB_ONLY[1],
        "<!-- markdownlint-disable MD013 -->",
        SPHINX_ONLY[0],
        "```{raw} html",
        '<div class="kx">',
        f'<div class="chips" role="group" aria-label="Show one path" data-paths-for="{sid}"></div>',
        "<figure>",
        f'<div class="diagram explorer">{markup}</div>',
        f"<figcaption>{dk.esc(caption)}</figcaption>",
        "</figure>",
        key,
        f'<div class="detail" data-detail-for="{sid}" aria-live="polite"></div>',
        f'<script type="application/json" id="diagram-data">{blob}</script>',
        "</div>",
        "```",
        SPHINX_ONLY[1],
        "<!-- markdownlint-enable MD013 -->",
    ]
