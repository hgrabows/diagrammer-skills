#!/usr/bin/env python3
"""
Mermaid diagram validator utilities.

validate_mermaid_file(file_path, verbose=False) -> (ok: bool, message: str)
- Renders via Mermaid CLI (mmdc). mmdc parses and renders in a real browser, so a syntax
  error makes it exit non-zero with the parser message (line number included).
- Supports .mmd files or Markdown files containing ```mermaid fenced blocks.
- Needs Mermaid CLI 12 or newer: the PNG resolution is set with its `--size` option.

Differs from the project's original validator: the separate Node pre-parse step is gone.
Without a browser DOM it rejected valid diagrams of several types (state, mindmap, C4,
gitGraph, kanban, quadrant, sankey, xychart) with "DOMPurify.sanitize is not a function".
"""

from __future__ import annotations

import math
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from svg_size import SvgSize, max_png_side, read_svg_size


def _extract_mermaid_code(content: str) -> Optional[str]:
    """Extract Mermaid code from a fenced block in Markdown.

    Matches the first ```mermaid ... ``` block and returns its inner content.
    Returns None if no such block is found.
    """
    pattern = r"```mermaid\s*\n(.*?)```"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


DEFAULT_SCREEN_DPI = 96.0
DEFAULT_PNG_DPI = 600
STACK_FRAME_PATTERN = re.compile(r"^\s*at\s|\((?:/|file://|https?://)[^)]*:\d+:\d+\)\s*$")
ERROR_SVG_MARKER = 'aria-roledescription="error"'


def _resolve_target_png_dpi() -> int:
    """Return the desired PNG DPI (defaults to 600, overridable via MMDC_PNG_DPI)."""
    env_value = os.environ.get("MMDC_PNG_DPI")
    if not env_value:
        return DEFAULT_PNG_DPI
    try:
        dpi_value = int(env_value)
        return dpi_value if dpi_value > 0 else DEFAULT_PNG_DPI
    except ValueError:
        return DEFAULT_PNG_DPI


def _build_png_size_args(target_dpi: int, svg_size: SvgSize) -> List[str]:
    """Build the CLI args that set the PNG resolution (needs Mermaid CLI 12 or newer).

    `--size` gives the PNG's longest side in pixels. It is the diagram's size at the target
    DPI, capped so that a large diagram gets a lower resolution instead of a huge image.
    Without a known SVG size the whole-number `--scale` factor is the fallback.
    """
    if not svg_size:
        return ["--scale", str(max(int(target_dpi / DEFAULT_SCREEN_DPI), 1))]
    wanted = math.ceil(max(svg_size) * target_dpi / DEFAULT_SCREEN_DPI)
    return ["--size", str(max(1, min(wanted, max_png_side())))]


def _run_mmdc(
    mmdc_cmd: str,
    input_path: str,
    output_path: str,
    *,
    extra_args: Optional[List[str]] = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke Mermaid CLI with standard flags and optional extras."""
    cmd = [
        mmdc_cmd,
        "-i",
        input_path,
        "-o",
        output_path,
        "-b",
        "transparent",
    ]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _clean_mmdc_error(text: str) -> str:
    """Keep the parser message of an mmdc failure and drop the JavaScript stack trace."""
    kept: List[str] = []
    for line in (text or "").splitlines():
        if STACK_FRAME_PATTERN.search(line):
            break
        kept.append(line.rstrip())
    return "\n".join(kept).strip()


def _is_error_svg(svg_path: Path) -> bool:
    """Return True when Mermaid drew its "syntax error" placeholder instead of the diagram."""
    try:
        return ERROR_SVG_MARKER in svg_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def validate_mermaid_file(file_path: str, verbose: bool = False) -> Tuple[bool, str]:
    """Validate a Mermaid file by rendering SVG+PNG via Mermaid CLI.

    - file_path: path to a .mmd file or a Markdown file containing a mermaid block.
    - verbose: currently unused; reserved for future logging verbosity.

    Returns (ok, message). On failure the message is the parser/render error.
    The SVG and a high-DPI PNG are written next to the source using the same basename.
    """
    p = Path(file_path)
    if not p.exists():
        return False, f"File not found: {p}"

    svg_output = p.with_suffix(".svg")
    png_output = p.with_suffix(".png")

    try:
        content = p.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read file: {e}"

    code = _extract_mermaid_code(content)
    mmdc = os.environ.get("MMDC_CMD", "mmdc")

    tmp_path: Optional[str] = None
    try:
        if code is not None:
            with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False, encoding="utf-8") as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            input_target = tmp_path
        else:
            input_target = str(p)

        # Remove stale artifacts so a failed run can never be mistaken for a fresh render.
        for stale in (svg_output, png_output):
            if stale.exists():
                stale.unlink()

        svg_result = _run_mmdc(mmdc, input_target, str(svg_output))
        if svg_result.returncode != 0 or not svg_output.exists():
            message = _clean_mmdc_error(svg_result.stderr) or _clean_mmdc_error(svg_result.stdout)
            return False, message or "mmdc failed to render SVG output."
        if _is_error_svg(svg_output):
            svg_output.unlink()
            return False, "Mermaid reported a syntax error in the diagram text."

        svg_size = read_svg_size(svg_output)
        png_args = _build_png_size_args(_resolve_target_png_dpi(), svg_size)
        png_result = _run_mmdc(mmdc, input_target, str(png_output), extra_args=png_args)
        if png_result.returncode != 0 or not png_output.exists():
            message = _clean_mmdc_error(png_result.stderr) or _clean_mmdc_error(png_result.stdout)
            svg_output.unlink(missing_ok=True)
            png_output.unlink(missing_ok=True)
            return False, message or "mmdc failed to render PNG output."

        return True, ""
    except FileNotFoundError:
        return False, "mmdc command not found. Install Mermaid CLI: npm install -g @mermaid-js/mermaid-cli"
    except Exception as e:
        return False, f"Error validating diagram: {e}"
    finally:
        if tmp_path:
            try:
                os.remove(tmp_path)
            except Exception:
                pass


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Validate Mermaid diagram files and render SVG/PNG outputs")
    parser.add_argument("files", nargs="+", help="Mermaid files to validate (.mmd or .md)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    total_ok = 0
    for f in args.files:
        ok, msg = validate_mermaid_file(f, verbose=args.verbose)
        print(f"{f}: {'OK' if ok else 'FAIL'}")
        if msg:
            print(msg)
        total_ok += int(ok)

    sys.exit(0 if total_ok == len(args.files) else 1)
