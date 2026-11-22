#!/usr/bin/env python3
"""Rebuild the examples/ gallery: one example per diagram type, taken from the specs.

Usage:
    python3 tools/build_examples.py

Each entry of EXAMPLES names a spec and the number of its ```mermaid / ```plantuml block
(counted in file order). The block is written to examples/<spec>.mmd or .puml and rendered
to SVG and PNG at GALLERY_DPI, which keeps the PNGs small enough for the repository.
The README gallery is regenerated between its two marker comments.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "diagrammer"
EXAMPLES_DIR = REPO / "examples"
README = REPO / "README.md"
GALLERY_DPI = "192"
GALLERY_START = "<!-- gallery:start -->"
GALLERY_END = "<!-- gallery:end -->"
COLUMNS = 3

sys.dont_write_bytecode = True
os.environ.setdefault("MMDC_PNG_DPI", GALLERY_DPI)
os.environ.setdefault("PLANTUML_PNG_DPI", GALLERY_DPI)
sys.path.insert(0, str(SKILL / "scripts"))

from render import render_file  # noqa: E402

FENCE = re.compile(r"```(mermaid|plantuml)[^\n]*\n(.*?)```", re.DOTALL | re.IGNORECASE)
SUFFIX = {"mermaid": ".mmd", "plantuml": ".puml"}

# (spec file, block number, caption)
EXAMPLES: list[tuple[str, int, str]] = [
    ("mermaid/flowchart.md", 11, "Flowchart"),
    ("mermaid/sequenceDiagram.md", 5, "Sequence diagram"),
    ("mermaid/classDiagram.md", 8, "Class diagram"),
    ("mermaid/stateDiagram.md", 3, "State diagram"),
    ("mermaid/entityRelationshipDiagram.md", 14, "ER diagram"),
    ("mermaid/userJourney.md", 4, "User journey"),
    ("mermaid/gantt.md", 8, "Gantt"),
    ("mermaid/pieChart.md", 5, "Pie chart"),
    ("mermaid/quadrantChart.md", 4, "Quadrant chart"),
    ("mermaid/requirementDiagram.md", 8, "Requirement diagram"),
    ("mermaid/gitGraph.md", 5, "GitGraph"),
    ("mermaid/c4Diagram.md", 5, "C4"),
    ("mermaid/mindmap.md", 2, "Mindmap"),
    ("mermaid/timeline.md", 7, "Timeline"),
    ("mermaid/zenuml.md", 4, "ZenUML"),
    ("mermaid/sankeyDiagram.md", 4, "Sankey"),
    ("mermaid/xyChart.md", 5, "XY chart"),
    ("mermaid/blockDiagram.md", 9, "Block diagram"),
    ("mermaid/packet.md", 1, "Packet"),
    ("mermaid/kanban.md", 3, "Kanban"),
    ("mermaid/architectureDiagram.md", 1, "Architecture"),
    ("mermaid/radar.md", 4, "Radar"),
    ("mermaid/treemap.md", 3, "Treemap"),
    ("mermaid/useCase.md", 5, "Use case"),
    ("mermaid/swimlane.md", 5, "Swimlane"),
    ("mermaid/venn.md", 6, "Venn"),
    ("mermaid/ishikawa.md", 3, "Ishikawa"),
    ("mermaid/treeView.md", 5, "TreeView"),
    ("mermaid/wardley.md", 6, "Wardley map"),
    ("mermaid/cynefin.md", 3, "Cynefin"),
    ("mermaid/eventModeling.md", 7, "Event Modeling"),
    ("mermaid/railroad.md", 6, "Railroad"),
    ("mermaid/agentFlow.md", 7, "Agent Flow"),
    ("plantuml/plantuml_er.md", 2, "ER diagram (PlantUML)"),
    ("plantuml/plantuml_class.md", 10, "Class diagram (PlantUML)"),
    ("plantuml/plantuml_mindmap.md", 9, "Mindmap (PlantUML)"),
]


def extract(spec: str, number: int) -> tuple[str, str]:
    """Return (engine, code) of the numbered diagram block in a spec file."""
    blocks = list(FENCE.finditer((SKILL / "specs" / spec).read_text(encoding="utf-8")))
    if not 1 <= number <= len(blocks):
        raise SystemExit(f"{spec} has {len(blocks)} diagram blocks, not {number}")
    match = blocks[number - 1]
    return match.group(1).lower(), match.group(2)


def gallery_markdown(entries: list[tuple[str, str]]) -> str:
    """Build an HTML table of thumbnails; each links to the diagram's source file."""
    rows = []
    for start in range(0, len(entries), COLUMNS):
        cells = []
        for source, caption in entries[start : start + COLUMNS]:
            png = Path(source).with_suffix(".png").as_posix()
            cells.append(
                f'<td align="center" width="33%"><a href="{source}"><img src="{png}" alt="{caption}" '
                f'height="180"></a><br><sub>{caption}</sub></td>'
            )
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main() -> int:
    """Write, render and list all examples; return 1 if any of them fails."""
    EXAMPLES_DIR.mkdir(exist_ok=True)
    for old in EXAMPLES_DIR.iterdir():
        if old.suffix in {".mmd", ".puml", ".svg", ".png"}:
            old.unlink()

    entries: list[tuple[str, str]] = []
    failed = 0
    for spec, number, caption in EXAMPLES:
        engine, code = extract(spec, number)
        target = EXAMPLES_DIR / f"{Path(spec).stem}{SUFFIX[engine]}"
        target.write_text(code, encoding="utf-8")
        ok, _engine, message = render_file(target)
        print(f"{'ok  ' if ok else 'FAIL'} {target.relative_to(REPO)}")
        if not ok:
            failed += 1
            print(message)
        entries.append((target.relative_to(REPO).as_posix(), caption))

    readme = README.read_text(encoding="utf-8")
    if GALLERY_START in readme and GALLERY_END in readme:
        head, rest = readme.split(GALLERY_START, 1)
        _, tail = rest.split(GALLERY_END, 1)
        README.write_text(f"{head}{GALLERY_START}\n{gallery_markdown(entries)}\n{GALLERY_END}{tail}", encoding="utf-8")
    else:
        print(f"README has no {GALLERY_START} / {GALLERY_END} markers; gallery not updated")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
