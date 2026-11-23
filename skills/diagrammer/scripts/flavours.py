"""Find the style rules ("flavours") that apply to a diagram type.

A flavour is a plain text file with the user's own wishes for how diagrams look. There are two
kinds, `general.txt` for every diagram and `<spec name>.txt` for one type (for example
`flowchart.txt` or `plantuml_er.txt`). Each kind is looked up in three places, most specific
first, and the first file found wins:

1. project: `.diagrammer/flavours/` in the current working directory
2. user:    `~/.claude/diagrammer/flavours/` (or DIAGRAMMER_USER_FLAVOURS)
3. skill:   `flavours/` inside the skill, shipped with it

So a project can give the same diagram type other colours than the user's default.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Tuple

SKILL_FLAVOURS = Path(__file__).resolve().parent.parent / "flavours"
PROJECT_SUBDIR = Path(".diagrammer") / "flavours"
GENERAL = "general"


def flavour_dirs(cwd: Optional[Path] = None) -> List[Tuple[str, Path]]:
    """Return the (scope, directory) pairs to search, most specific first."""
    user = os.environ.get("DIAGRAMMER_USER_FLAVOURS") or str(Path.home() / ".claude" / "diagrammer" / "flavours")
    return [
        ("project", (cwd or Path.cwd()) / PROJECT_SUBDIR),
        ("user", Path(user).expanduser()),
        ("skill", SKILL_FLAVOURS),
    ]


def find_flavours(spec_name: str, cwd: Optional[Path] = None) -> List[Tuple[str, Path]]:
    """Return the flavour files for a spec, general first, as (scope, path) pairs.

    spec_name is the spec file name with or without `.md` (e.g. `stateDiagram`). An empty
    file counts as present, so a project can switch off a user or skill flavour with it.
    """
    name = Path(spec_name).stem
    found: List[Tuple[str, Path]] = []
    for kind in (GENERAL, name):
        for scope, directory in flavour_dirs(cwd):
            candidate = directory / f"{kind}.txt"
            if candidate.is_file():
                found.append((scope, candidate))
                break
    return found
