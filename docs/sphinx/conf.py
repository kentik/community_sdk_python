# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
import logging
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.abspath("../../src"))

project = "Kentik API - Python SDK"
copyright = "2026, Kentik"
author = "Alex DeAraujo"


source_suffix = [".rst", ".md"]

root_doc = "index"

# "**/README.md" does not match a README at the source root, so list it too.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md", "**/README.md"]

# Deliberately empty. Broken links surface as myst.xref_missing and orphaned
# pages as toc.not_included, so suppressing either would let `-W` pass on the
# exact defects it exists to catch. Link to files outside this tree by GitHub
# URL instead.
suppress_warnings: list[str] = []

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic",  # Formats Pydantic v2 models beautifully
    "sphinxcontrib.mermaid",  # Renders Mermaid diagrams (replaces PlantUML)
]

myst_enable_extensions = [
    "alert",
    "colon_fence",
]

myst_fence_as_directive = ["mermaid"]
# Pinned: participant types and the neo look need 12, and the step script reads its SVG classes.
mermaid_version = "12.3.0"

html_theme = "sphinx_book_theme"

# The generator writes these from scripts/generation/diagram_assets/. The script
# only acts on pages that hold an interactive diagram.
html_static_path = ["_static"]
html_css_files = ["explorer.css"]
html_js_files = [
    ("explorer.js", {"defer": "defer"}),
    ("sequence-steps.js", {"defer": "defer"}),
]

# Skip copying every source page into build/html/_sources/. Those copies are
# byte-identical to docs/sphinx/**, and this repo already tracks the
# rendered HTML in git, so the copies were pure duplication.
html_copy_source = False
html_show_sourcelink = False

# The theme's "download source" button links to _sources/ regardless of
# html_show_sourcelink, so it needs its own opt-out too.
html_theme_options = {
    "use_download_button": False,
}

autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_config_summary = False


class SuppressDocutilsFilter(logging.Filter):
    """Filter out pedantic docstring formatting warnings from generated code."""

    def filter(self, record):
        msg = record.getMessage()
        return not (
            "Block quote ends without a blank line" in msg
            or "unexpected unindent" in msg
        )


_RST_INLINE_MARKUP = re.compile(r"([\\*`|_])")
# The generator writes each explorer twice: a Mermaid fallback that GitHub shows,
# and the explorer inside an HTML comment that GitHub hides. Sphinx gets the explorer.
_GITHUB_ONLY = re.compile(r"<!-- github-only -->.*?<!-- /github-only -->\n?", re.DOTALL)
_SPHINX_ONLY = re.compile(r"<!-- sphinx-only\n(.*?)\n-->", re.DOTALL)


def _swap_github_blocks(app, docname, source):
    source[0] = _SPHINX_ONLY.sub(r"\1", _GITHUB_ONLY.sub("", source[0]))


def setup(app):
    """Sphinx hook to inject our custom logger filter."""
    from sphinx.util.logging import getLogger
    from sphinxcontrib.autodoc_pydantic.directives.autodocumenters import (
        PydanticFieldDocumenter,
    )

    class SchemaTextFieldDocumenter(PydanticFieldDocumenter):
        def _get_field_description(self) -> str:
            text = super()._get_field_description() or ""
            # Indented schema prose (an example payload) would parse as an RST definition list.
            # prepare_docstring() dedents every line after the first, so "::" goes on line two.
            if any(line[:1].isspace() for line in text.splitlines()):
                return "\n::\n\n" + textwrap.indent(text, "   ")
            # Field descriptions are schema prose: `c_` or `*.` is not RST markup.
            return _RST_INLINE_MARKUP.sub(r"\\\1", text)

    app.add_autodocumenter(SchemaTextFieldDocumenter, override=True)
    app.connect("source-read", _swap_github_blocks)
    logger = getLogger("sphinx")
    logger.logger.addFilter(SuppressDocutilsFilter())
