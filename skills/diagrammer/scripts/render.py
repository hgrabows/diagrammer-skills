#!/usr/bin/env python3
"""Validate and render diagram files for the diagrammer skill.

Usage:
    python3 render.py <file> [<file> ...]   # .mmd -> Mermaid, .puml -> PlantUML
    python3 render.py --check               # report which render tools are available

Each file is validated and rendered to an SVG and a PNG next to the source file.
Exit code 0 means every file rendered; 1 means at least one failed.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# Keep the skill folder clean: importing the sibling modules must not leave __pycache__ behind.
sys.dont_write_bytecode = True

from mermaid_validator import validate_mermaid_file
from validate_plantuml import _resolve_plantuml_jar, validate_plantuml_file

MERMAID_SUFFIXES = {".mmd", ".mermaid"}
PLANTUML_SUFFIXES = {".puml", ".plantuml", ".iuml"}


def detect_engine(path: Path) -> str:
    """Return "mermaid" or "plantuml" for a diagram file, based on its suffix."""
    suffix = path.suffix.lower()
    if suffix in MERMAID_SUFFIXES:
        return "mermaid"
    if suffix in PLANTUML_SUFFIXES:
        return "plantuml"
    raise ValueError(
        f"Unknown diagram suffix '{path.suffix}' for {path}. "
        "Use .mmd for Mermaid or .puml for PlantUML."
    )


def render_file(path: Path) -> tuple[bool, str, str]:
    """Validate and render one diagram; return (ok, engine, validator message)."""
    engine = detect_engine(path)
    if engine == "plantuml":
        ok, message = validate_plantuml_file(str(path))
    else:
        ok, message = validate_mermaid_file(str(path))
    return ok, engine, message


def check_tools() -> list[tuple[str, bool, str]]:
    """Return (tool, available, detail) for every external tool the renderers need.

    PlantUML runs either from a jar (PLANTUML_JAR or the skill's vendor/ folder, needs java)
    or through an installed `plantuml` command, which brings its own Java.
    """
    node = shutil.which("node")
    mmdc = shutil.which(os.environ.get("MMDC_CMD", "mmdc"))
    dot = shutil.which(os.environ.get("GRAPHVIZ_DOT", "dot"))
    tools = [
        ("node", bool(node), node or "needed for Mermaid: https://nodejs.org"),
        ("mmdc", bool(mmdc), mmdc or "needed for Mermaid: npm install -g @mermaid-js/mermaid-cli"),
    ]

    jar = _resolve_plantuml_jar()
    if jar is not None:
        java = shutil.which(os.environ.get("JAVA_CMD", "java"))
        tools.append(("plantuml", True, f"jar {jar}"))
        tools.append(("java", bool(java), java or "needed to run the PlantUML jar"))
    else:
        plantuml = shutil.which(os.environ.get("PLANTUML_CMD", "plantuml"))
        hint = "needed for PlantUML: install it (e.g. brew install plantuml) or set PLANTUML_JAR to a plantuml jar"
        tools.append(("plantuml", bool(plantuml), plantuml or hint))

    tools.append(("dot", bool(dot), dot or "Graphviz, needed for PlantUML class and ER diagrams"))
    return tools


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Validate and render Mermaid/PlantUML files to SVG + PNG.")
    parser.add_argument("files", nargs="*", help="Diagram files (.mmd or .puml)")
    parser.add_argument("--check", action="store_true", help="Only report which render tools are available")
    args = parser.parse_args(argv)

    if args.check:
        tools = check_tools()
        for name, available, detail in tools:
            print(f"{'ok     ' if available else 'MISSING'} {name}: {detail}")
        return 0 if all(available for _, available, _ in tools) else 1

    if not args.files:
        parser.error("no diagram file given")

    all_ok = True
    for raw in args.files:
        path = Path(raw).expanduser().resolve()
        try:
            ok, engine, message = render_file(path)
        except ValueError as exc:
            print(f"FAIL {path}\n{exc}")
            all_ok = False
            continue
        if ok:
            print(f"OK   {path} ({engine})")
            print(f"     SVG: {path.with_suffix('.svg')}")
            print(f"     PNG: {path.with_suffix('.png')}")
        else:
            print(f"FAIL {path} ({engine})")
            print(message or "Validator reported a failure without a message.")
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
