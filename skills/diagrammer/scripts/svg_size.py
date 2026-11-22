#!/usr/bin/env python3
"""Keep rendered PNGs complete and within a sane pixel size.

Both renderers derive the PNG from the SVG's size. At 600 dpi a mid-sized diagram exceeds
what they handle: PlantUML silently crops at its size limit (4096 px by default) and
Chromium cannot screenshot beyond its texture limit. The DPI is therefore lowered just
enough that the longest side stays within the limit; small diagrams keep the full target DPI.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple

SCREEN_DPI = 96.0
DEFAULT_MAX_PNG_SIDE_PX = 8192
VIEWBOX_PATTERN = re.compile(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"')

SvgSize = Optional[Tuple[float, float]]


def max_png_side() -> int:
    """Return the longest allowed PNG side in pixels (override: DIAGRAMMER_MAX_PNG_SIDE)."""
    raw = os.environ.get("DIAGRAMMER_MAX_PNG_SIDE", "")
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_MAX_PNG_SIDE_PX
    return value if value > 0 else DEFAULT_MAX_PNG_SIDE_PX


def read_svg_size(svg_path: Path) -> SvgSize:
    """Return (width, height) in CSS pixels from the SVG's viewBox, or None if unreadable."""
    try:
        with svg_path.open("r", encoding="utf-8", errors="ignore") as handle:
            head = handle.read(4096)
    except OSError:
        return None
    match = VIEWBOX_PATTERN.search(head)
    if not match:
        return None
    width, height = float(match.group(1)), float(match.group(2))
    if width <= 0 or height <= 0:
        return None
    return width, height


def capped_dpi(target_dpi: int, svg_size: SvgSize) -> int:
    """Return target_dpi, lowered if needed so the PNG's longest side fits the limit."""
    if not svg_size:
        return target_dpi
    fitting_dpi = int(SCREEN_DPI * max_png_side() / max(svg_size))
    return max(int(SCREEN_DPI), min(target_dpi, fitting_dpi))


def png_side_limit(dpi: int, svg_size: SvgSize) -> int:
    """Return the pixel limit to hand to a renderer so it never crops the PNG."""
    limit = max_png_side()
    if svg_size:
        limit = max(limit, int(max(svg_size) * dpi / SCREEN_DPI) + 64)
    return limit
