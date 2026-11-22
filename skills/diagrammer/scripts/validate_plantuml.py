#!/usr/bin/env python3
"""
PlantUML validation/render helper.

The validate_plantuml_file helper mirrors mermaid_validator.validate_mermaid_file:
- Accepts .puml/.plantuml/.iuml files or Markdown containing ```plantuml fences.
- Renders SVG + PNG next to the source and returns (ok: bool, message: str).

PlantUML is looked up in this order: the jar named by PLANTUML_JAR, a plantuml*.jar in the
skill's vendor/ folder (both run with java), then the `plantuml` command (or PLANTUML_CMD).
No jar is shipped with the skill.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from svg_size import capped_dpi, png_side_limit, read_svg_size


PLANTUML_FENCE_PATTERN = re.compile(r"```plantuml\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
PLANTUML_START_PATTERN = re.compile(r"@start", re.IGNORECASE)
APP_ROOT = Path(__file__).resolve().parent
LOCAL_PLANTUML_DIR = APP_ROOT.parent / "vendor"


def _extract_plantuml_block(content: str) -> Optional[str]:
    """Return the first ```plantuml ... ``` block body, if any."""
    match = PLANTUML_FENCE_PATTERN.search(content or "")
    if not match:
        return None
    return match.group(1).strip()


def _ensure_wrapped(code: str) -> str:
    """Ensure PlantUML code contains @start/@end markers."""
    stripped = (code or "").strip()
    if not stripped:
        return ""
    if PLANTUML_START_PATTERN.search(stripped):
        return stripped
    return "@startuml\n" + stripped + ("\n@enduml\n" if not stripped.endswith("\n@enduml") else "")


def _resolve_png_dpi() -> int:
    """Return desired PNG DPI; defaults to 600."""
    raw = os.environ.get("PLANTUML_PNG_DPI") or os.environ.get("PLANTUML_DPI")
    if not raw:
        return 600
    try:
        value = int(raw)
        return value if value > 0 else 600
    except ValueError:
        return 600


def _resolve_plantuml_jar() -> Optional[Path]:
    """Resolve a usable PlantUML jar, preferring explicit env overrides."""

    raw_env = (os.environ.get("PLANTUML_JAR") or "").strip()
    if raw_env:
        candidate = Path(raw_env).expanduser().resolve()
        if candidate.exists():
            return candidate

    local_candidates = sorted(LOCAL_PLANTUML_DIR.glob("plantuml*.jar"))
    for candidate in reversed(local_candidates):
        if candidate.is_file():
            return candidate.resolve()

    return None


def _build_base_command(fmt: str, dpi: Optional[int] = None) -> List[str]:
    """Construct the PlantUML invocation for a specific format (dpi applies to PNG only)."""
    fmt_flag = f"-t{fmt}"
    jar_path = _resolve_plantuml_jar()
    if jar_path is not None:
        java_cmd = os.environ.get("JAVA_CMD", "java")
        cmd = [java_cmd, "-jar", str(jar_path)]
    else:
        plantuml_cmd = os.environ.get("PLANTUML_CMD", "plantuml")
        if shutil.which(plantuml_cmd) is None:
            raise FileNotFoundError(f"no PlantUML jar found and the command '{plantuml_cmd}' is not installed.")
        cmd = [plantuml_cmd]

    graphviz_dot = os.environ.get("PLANTUML_DOT") or os.environ.get("GRAPHVIZ_DOT")
    if graphviz_dot:
        cmd.extend(["-graphvizdot", graphviz_dot])

    cmd.append(fmt_flag)

    if fmt.lower() == "png":
        # PlantUML 1.2025.x ignores "-dpi"; the skinparam form is the one that takes effect.
        cmd.append(f"-Sdpi={dpi or _resolve_png_dpi()}")

    output_dir = os.environ.get("PLANTUML_OUTPUT_DIR")
    if output_dir:
        cmd.extend(["-o", output_dir])

    return cmd


def _run_plantuml(
    input_path: str,
    fmt: str,
    *,
    dpi: Optional[int] = None,
    limit_px: Optional[int] = None,
) -> subprocess.CompletedProcess[str]:
    """Run PlantUML for the desired format and return the completed process.

    limit_px raises PlantUML's image size limit; without it PNGs are cropped at 4096 px.
    """
    cmd = _build_base_command(fmt, dpi) + [input_path]
    env: Optional[Dict[str, str]] = None
    if limit_px:
        env = dict(os.environ)
        env["PLANTUML_LIMIT_SIZE"] = str(limit_px)
    return subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)


def _collect_message(result: subprocess.CompletedProcess[str]) -> str:
    """Summarize stdout/stderr for logging."""
    pieces: list[str] = []
    if result.stdout:
        pieces.append(result.stdout.strip())
    if result.stderr:
        pieces.append(result.stderr.strip())
    return "\n".join(piece for piece in pieces if piece)


def _write_temp_puml(code: str, directory: Path) -> Path:
    """Persist extracted PlantUML code to a temporary .puml file inside directory."""
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".puml", delete=False, dir=str(directory), encoding="utf-8") as tmp:
        tmp.write(_ensure_wrapped(code) + "\n")
        return Path(tmp.name)


def _move_output(src: Path, dest: Path) -> None:
    """Move/rename a rendered artifact if it exists."""
    if src.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest.unlink()
        src.replace(dest)


def validate_plantuml_file(file_path: str, verbose: bool = False) -> Tuple[bool, str]:
    """
    Render PlantUML diagrams to SVG + PNG.

    Parameters
    ----------
    file_path:
        Path to a .puml/.plantuml/.iuml file or Markdown containing ```plantuml fences.
    verbose:
        Currently unused (kept for API parity).

    Returns
    -------
    Tuple[bool, str]
        ok flag plus CLI log/diagnostic output.
    """

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return False, f"File not found: {path}"

    svg_target = path.with_suffix(".svg")
    png_target = path.with_suffix(".png")

    input_path = path
    temp_input: Optional[Path] = None
    temp_svg: Optional[Path] = None
    temp_png: Optional[Path] = None

    try:
        code = None
        lower_suffix = path.suffix.lower()
        if lower_suffix in {".md", ".markdown"}:
            code = _extract_plantuml_block(path.read_text(encoding="utf-8"))
            if not code:
                return False, "No ```plantuml``` fenced block found in Markdown file."
            temp_input = _write_temp_puml(code, path.parent)
            input_path = temp_input
            temp_svg = temp_input.with_suffix(".svg")
            temp_png = temp_input.with_suffix(".png")
        elif lower_suffix not in {".puml", ".plantuml", ".iuml"}:
            # Treat unknown extensions as PlantUML code; enforce markers if missing.
            raw = path.read_text(encoding="utf-8")
            amended = _ensure_wrapped(raw)
            if amended != raw:
                temp_input = _write_temp_puml(amended, path.parent)
                input_path = temp_input
                temp_svg = temp_input.with_suffix(".svg")
                temp_png = temp_input.with_suffix(".png")

        svg_result = _run_plantuml(str(input_path), "svg")
        svg_ok = svg_result.returncode == 0

        # Size the PNG from the SVG: full target DPI when it fits, lower DPI instead of cropping.
        svg_size = read_svg_size(input_path.with_suffix(".svg")) if svg_ok else None
        png_dpi = capped_dpi(_resolve_png_dpi(), svg_size)
        png_result = _run_plantuml(
            str(input_path),
            "png",
            dpi=png_dpi,
            limit_px=png_side_limit(png_dpi, svg_size),
        )
        png_ok = png_result.returncode == 0

        if not svg_ok or not png_ok:
            combined = []
            if not svg_ok:
                combined.append(f"[svg] { _collect_message(svg_result) or 'PlantUML failed to render SVG.' }")
            if not png_ok:
                combined.append(f"[png] { _collect_message(png_result) or 'PlantUML failed to render PNG.' }")
            # PlantUML draws its error message into the output files; remove them so a failed
            # run can never be mistaken for a rendered diagram.
            for leftover in (svg_target, png_target):
                leftover.unlink(missing_ok=True)
            return False, "\n".join(combined).strip()

        # Relocate outputs when working from a temporary .puml file.
        actual_svg = temp_svg if temp_svg and temp_svg.exists() else svg_target
        actual_png = temp_png if temp_png and temp_png.exists() else png_target

        if temp_svg and temp_svg.exists():
            _move_output(temp_svg, svg_target)
        else:
            svg_target = actual_svg
        if temp_png and temp_png.exists():
            _move_output(temp_png, png_target)
        else:
            png_target = actual_png

        message_parts: list[str] = []
        svg_msg = _collect_message(svg_result)
        png_msg = _collect_message(png_result)
        if svg_msg:
            message_parts.append(f"[svg] {svg_msg}")
        if png_msg:
            message_parts.append(f"[png] {png_msg}")
        return True, "\n".join(message_parts).strip()
    except FileNotFoundError as exc:
        return (
            False,
            f"PlantUML could not be started: {exc}\n"
            "Install PlantUML (e.g. brew install plantuml) or set PLANTUML_JAR to a plantuml jar; "
            "a jar also needs java. Run render.py --check to see what is missing."
        )
    except Exception as exc:
        return False, f"PlantUML rendering failed: {exc}"
    finally:
        if temp_input and temp_input.exists():
            try:
                temp_input.unlink()
            except Exception:
                pass
        if temp_svg and temp_svg.exists():
            try:
                temp_svg.unlink()
            except Exception:
                pass
        if temp_png and temp_png.exists():
            try:
                temp_png.unlink()
            except Exception:
                pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate/render PlantUML diagrams to SVG/PNG.")
    parser.add_argument("files", nargs="+", help="PlantUML or Markdown files to render.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose CLI output.")
    args = parser.parse_args()

    total = 0
    for item in args.files:
        ok, msg = validate_plantuml_file(item, verbose=args.verbose)
        status = "OK" if ok else "FAIL"
        print(f"{item}: {status}")
        if msg:
            print(msg)
        total += int(ok)

    raise SystemExit(0 if total == len(args.files) else 1)
