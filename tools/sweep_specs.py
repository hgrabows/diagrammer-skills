#!/usr/bin/env python3
"""Render every fenced example of the skill's spec files and report the ones that fail.

Usage:
    python3 tools/sweep_specs.py <work-dir> [name-filter ...]

Each ```mermaid / ```plantuml block of specs/**/*.md is written to <work-dir>/<spec>/NN.mmd
(or .puml) and rendered with the skill's own validators. Run it after updating Mermaid or
PlantUML, or after editing a spec. Exit code 1 means at least one example failed.
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "diagrammer"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SKILL / "scripts"))

from render import render_file  # noqa: E402

FENCE = re.compile(r"```(mermaid|plantuml)[^\n]*\n(.*?)```", re.DOTALL | re.IGNORECASE)
SUFFIX = {"mermaid": ".mmd", "plantuml": ".puml"}


def collect(work: Path, filters: list[str]) -> list[tuple[str, int, Path]]:
    """Write all examples to files and return (spec name, block number, file)."""
    jobs: list[tuple[str, int, Path]] = []
    for spec in sorted((SKILL / "specs").glob("*/*.md")):
        if filters and not any(f.lower() in spec.stem.lower() for f in filters):
            continue
        for number, match in enumerate(FENCE.finditer(spec.read_text(encoding="utf-8")), start=1):
            target = work / spec.stem / f"{number:02d}{SUFFIX[match.group(1).lower()]}"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(match.group(2), encoding="utf-8")
            jobs.append((spec.stem, number, target))
    return jobs


def main(argv: list[str]) -> int:
    """Command-line entry point."""
    if not argv:
        print(__doc__)
        return 2
    work = Path(argv[0]).resolve()
    jobs = collect(work, argv[1:])
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: render_file(job[2]), jobs))

    failures = 0
    per_spec: dict[str, list[int]] = {}
    for (name, number, path), (ok, _engine, message) in zip(jobs, results):
        counts = per_spec.setdefault(name, [0, 0])
        counts[0] += 1
        counts[1] += int(ok)
        if not ok:
            failures += 1
            first_lines = " | ".join(message.strip().splitlines()[:3])
            print(f"FAIL {name} #{number} ({path}): {first_lines[:300]}")
    for name, (total, good) in per_spec.items():
        print(f"{'ok  ' if total == good else 'FAIL'} {name:28s} {good}/{total}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
