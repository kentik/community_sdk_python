"""Build the consolidated upstream findings report and its HTML companions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, cast

REPORTS = Path(__file__).resolve().parents[1]
PROJECT_ROOT = REPORTS.parent
SKILL_ROOTS = (
    Path.home() / ".copilot/skills",
    Path.home() / ".claude/skills",
    Path.home() / "projects/claude-setup/plugins/core/skills",
)
SUPPORT_REPORTS = (
    "upstream-kptr-missing-http-annotations",
    "upstream-ratelimit-scope-undocumented",
    "upstream-service-visibility-exposure",
    "v5-feature-parity-audit",
)
ROOT_REPORTS = {
    ".gitignore",
    "kentik-api-team-findings.md",
    "kentik-api-team-findings.html",
}


def load_kit(relative_path: str) -> ModuleType:
    """Loads a page-theme module from an installed skills directory.

    Args:
        relative_path: Module path under the page-theme skill directory.

    Returns:
        The loaded module.

    Raises:
        FileNotFoundError: If no supported skills directory contains the module.
        ImportError: If Python cannot load the module.
    """
    path = next(
        (
            root / "page-theme" / "assets" / relative_path
            for root in SKILL_ROOTS
            if (root / "page-theme" / "assets" / relative_path).is_file()
        ),
        None,
    )
    if path is None:
        raise FileNotFoundError(
            f"{relative_path} was not found under a page-theme skills directory"
        )
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_lf(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def build_body() -> str:
    return """
<div class="wrap">
  <header class="masthead">
    <div class="eyebrow">Kentik API · Upstream review · 2026-11-19</div>
    <h1>Upstream issues with the <span>SDK</span></h1>
    <p class="lede">A reviewed register of upstream API and schema problems
    that affect the Kentik Community Python SDK. Confirmed failures, open
    questions, stale claims, and SDK workarounds are marked separately.</p>
    <div class="meta">
      <span>Review <b>2026-11-19</b></span>
      <span>Schema pin <b>9f58fdd</b></span>
      <span>Latest read-only E2E <b>2026-11-19</b></span>
    </div>
    <div class="figures" aria-label="Review figures">
      <div><strong>16</strong><span>upstream items reviewed</span></div>
      <div><strong>92</strong><span>read-only E2E tests passed</span></div>
      <div><strong>17</strong><span>expected E2E xfails</span></div>
      <div><strong>3</strong><span>schema services with no REST paths</span></div>
      <div><strong>13</strong><span>private or protected REST operations</span></div>
    </div>
  </header>

  <nav class="toc" aria-label="Sections">
    <ul>
      <li><a href="#snapshot">Latest checks</a></li>
      <li><a href="#groups">Issue groups</a></li>
      <li><a href="#scope">Scope and evidence</a></li>
      <li><a href="#full-report">Full report</a></li>
    </ul>
  </nav>

  <section id="snapshot">
    <div class="intro">
      <h2>Latest checks</h2>
      <p>The E2E run found no unexpected failures. Its expected xfails still
      identify API behavior that needs an upstream answer or fix.</p>
    </div>
    <div class="tablebox">
      <table>
        <thead>
          <tr><th>Suite result</th><th>Count</th><th>Meaning</th></tr>
        </thead>
        <tbody>
          <tr><td>Passed</td><td class="num">92</td><td>Read-only calls matched the SDK contract.</td></tr>
          <tr><td>Expected failures</td><td class="num">17</td><td>Known upstream responses, including 500, 501, and the V5 chart timeout.</td></tr>
          <tr><td>Skipped</td><td class="num">145</td><td>Mutating operations are excluded from the read-only run.</td></tr>
          <tr><td>Deselected</td><td class="num">277</td><td>Tests outside the selected REST E2E suite.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="notes">
      <div><b>SDK workarounds</b>Two confirmed issues have shared-runtime or
      generated-request workarounds. The server-side defects remain open.</div>
      <div><b>Schema exposure</b>Public RPCs lack HTTP bindings, while
      `PRIVATE` and `PROTECTED` operations appear in published OpenAPI.</div>
      <div><b>Evidence limits</b>No live probes ran during this review. Mutating
      canaries need an approved disposable resource and cleanup.</div>
    </div>
  </section>

  <section id="groups">
    <div class="intro">
      <h2>Issue groups</h2>
      <p>The full report records evidence date, SDK impact, and the next
      upstream action for each item.</p>
    </div>
    <div class="cards">
      <details class="card" open>
        <summary><span class="name">Runtime behavior</span>
          <span class="tags"><span class="tag red">500 / 501</span>
          <span class="tag orange">deadline</span></span>
        </summary>
        <div class="body">
          <p>Body parsing, FlowTag creation, AutoAck, gRPC deadlines, missing
          resources, malformed IDs, and unimplemented methods.</p>
          <a href="#md-up-01-rest-update-body-keys-conflict-with-the-published-contract">Open findings UP-01 to UP-10</a>
        </div>
      </details>
      <details class="card" open>
        <summary><span class="name">Schema publication</span>
          <span class="tags"><span class="tag blue">13 missing paths</span>
          <span class="tag red">visibility conflict</span></span>
        </summary>
        <div class="body">
          <p>REST bindings are absent for public RPCs, while private or protected
          paths are present in public OpenAPI.</p>
          <a href="#md-up-11-public-kptr-and-deviceconf-rpcs-have-no-http-bindings">Open schema findings UP-11 and UP-12</a>
        </div>
      </details>
      <details class="card" open>
        <summary><span class="name">Contracts and tooling</span>
          <span class="tags"><span class="tag yellow">needs answers</span>
          <span class="tag neutral">dependency request</span></span>
        </summary>
        <div class="body">
          <p>Rate-limit scope, the V5 batch response contract, and unused
          generator dependencies need clarification.</p>
          <a href="#md-up-13-rate-limit-documentation-conflicts-with-observed-headers">Open findings UP-13 to UP-16</a>
        </div>
      </details>
    </div>
  </section>

  <section id="scope">
    <div class="intro">
      <h2>Scope and evidence</h2>
      <p>“Open” means an upstream behavior or contract remains unresolved.
      It does not mean every item is a confirmed defect.</p>
    </div>
    <div class="stops">
      <p>The schema audit used local HEAD `dbe7ce6`. A file-level comparison
      found no changes to the affected services from the SDK pin `9f58fdd`.
      It did not test server authorization.</p>
    </div>
    <p><a href="#full-report">Read all 16 findings, stale claims, and next actions.</a></p>
    <p><a href="upstream/README.md">Browse supporting reports and evidence.</a></p>
  </section>

  <footer>
    <p>Evidence is dated per finding. This report does not include credentials
    or live account captures.</p>
  </footer>
</div>
"""


def main() -> None:
    """Build the tracker HTML and refresh supporting report tabs."""
    page_kit = cast(Any, load_kit("page_kit.py"))
    report_tabs = cast(Any, load_kit("report_tabs.py"))
    markdown = REPORTS / "kentik-api-team-findings.md"
    output = REPORTS / "kentik-api-team-findings.html"
    unexpected = [
        path.name
        for path in REPORTS.iterdir()
        if path.is_file() and path.name not in ROOT_REPORTS
    ]
    if unexpected:
        raise SystemExit(
            "Unexpected files in reports root: " + ", ".join(sorted(unexpected))
        )

    twins = {
        REPORTS / f"upstream/{name}.md": REPORTS / f"upstream/{name}.html"
        for name in SUPPORT_REPORTS
    }
    twins[markdown] = output
    page = page_kit.page(
        "Upstream Issues Affecting Kentik SDK",
        build_body(),
        standalone=True,
    )
    page = report_tabs.wrap(
        page,
        md_path=markdown,
        page_path=output,
        css_href="assets/report-tabs.css",
        js_href="assets/report-tabs.js",
        twins=twins,
    )
    if problems := report_tabs.check(page, output):
        raise SystemExit("\n".join(problems))
    write_lf(output, page)

    for name in SUPPORT_REPORTS:
        page_path = REPORTS / f"upstream/{name}.html"
        md_path = REPORTS / f"upstream/{name}.md"
        source = page_path.read_text(encoding="utf-8")
        for old, new in (
            ('href="report-theme.css"', 'href="../assets/report-theme.css"'),
            ('href="assets/report-tabs.css"', 'href="../assets/report-tabs.css"'),
            ('src="assets/', 'src="../assets/'),
            ('srcset="assets/', 'srcset="../assets/'),
            ('href="../docs/', 'href="../../docs/'),
            ('href="scripts/', 'href="../scripts/'),
            (
                'href="kentik-api-team-findings.md"',
                'href="../kentik-api-team-findings.md"',
            ),
        ):
            source = source.replace(old, new)
        source = report_tabs.wrap(
            source,
            md_path=md_path,
            page_path=page_path,
            css_href="../assets/report-tabs.css",
            js_href="../assets/report-tabs.js",
            twins=twins,
        )
        if problems := report_tabs.check(source, page_path):
            raise SystemExit(f"{page_path}:\n" + "\n".join(problems))
        write_lf(page_path, source)

    print(f"wrote {output}")
    for name in SUPPORT_REPORTS:
        print(f"refreshed {REPORTS / f'upstream/{name}.html'}")


if __name__ == "__main__":
    main()
