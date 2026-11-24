"""Tests for the render scripts bundled with the diagrammer skill."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "diagrammer" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import flavours  # noqa: E402
import mermaid_validator  # noqa: E402
import render  # noqa: E402
import svg_size  # noqa: E402
import validate_plantuml  # noqa: E402


def _plantuml_available() -> bool:
    """PlantUML runs from a jar (needs java) or from an installed `plantuml` command."""
    if validate_plantuml._resolve_plantuml_jar() is not None:
        return shutil.which("java") is not None
    return shutil.which("plantuml") is not None


needs_mmdc = pytest.mark.skipif(shutil.which("mmdc") is None, reason="Mermaid CLI (mmdc) not installed")
needs_plantuml = pytest.mark.skipif(not _plantuml_available(), reason="PlantUML (jar or command) not installed")
needs_local_jar = pytest.mark.skipif(
    validate_plantuml._resolve_plantuml_jar() is None or shutil.which("java") is None,
    reason="needs a local PlantUML jar and java to build a stand-in plantuml command",
)

STATE_DIAGRAM = "stateDiagram-v2\n    [*] --> Idle\n    Idle --> Running : start\n    Running --> [*]\n"
BROKEN_STATE_DIAGRAM = "stateDiagram-v2\n    [*] --> Idle\n    Idle --> --> Running : start\n"
ER_PLANTUML = "@startuml\nhide circle\nclass Kunde {\n  --\n  KUNDEN_NR (PK)\n}\n@enduml\n"


@pytest.mark.parametrize(
    ("name", "expected"),
    [("a.mmd", "mermaid"), ("a.MERMAID", "mermaid"), ("a.puml", "plantuml"), ("a.plantuml", "plantuml")],
)
def test_detect_engine_by_suffix(name: str, expected: str) -> None:
    assert render.detect_engine(Path(name)) == expected


def test_detect_engine_rejects_unknown_suffix() -> None:
    with pytest.raises(ValueError, match="Unknown diagram suffix"):
        render.detect_engine(Path("notes.md"))


def test_clean_mmdc_error_drops_stack_trace() -> None:
    raw = (
        "Error: Parse error on line 3:\n"
        "...Idle --> --> Running\n"
        "Expecting 'ID', got '-->'\n"
        "Parser.parseError (https://mermaid-cli-intercept.invalid/opt/mermaid/dist/state.mjs:205:21)\n"
        "Parser3.parseError (/opt/mermaid/dist/mermaid.js:129842:28)\n"
        "    at #evaluate (file:///opt/puppeteer/ExecutionContext.js:10:1)\n"
    )
    cleaned = mermaid_validator._clean_mmdc_error(raw)
    assert cleaned.endswith("Expecting 'ID', got '-->'")
    assert "mermaid.js" not in cleaned


def test_is_error_svg_detects_mermaid_error_placeholder(tmp_path: Path) -> None:
    error_svg = tmp_path / "error.svg"
    error_svg.write_text('<svg aria-roledescription="error"></svg>', encoding="utf-8")
    good_svg = tmp_path / "good.svg"
    good_svg.write_text('<svg aria-roledescription="stateDiagram"></svg>', encoding="utf-8")
    assert mermaid_validator._is_error_svg(error_svg)
    assert not mermaid_validator._is_error_svg(good_svg)
    assert not mermaid_validator._is_error_svg(tmp_path / "missing.svg")


def test_main_reports_unknown_suffix(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    unknown = tmp_path / "notes.txt"
    unknown.write_text("hello", encoding="utf-8")
    assert render.main([str(unknown)]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_main_check_lists_tools(capsys: pytest.CaptureFixture[str]) -> None:
    render.main(["--check"])
    output = capsys.readouterr().out
    for tool in ("node", "mmdc", "plantuml", "dot"):
        assert f" {tool}: " in output


def _without_plantuml_jar(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Put the validator in the state of a fresh clone: no jar in vendor/, none configured."""
    monkeypatch.setattr(validate_plantuml, "LOCAL_PLANTUML_DIR", tmp_path / "no-vendor")
    monkeypatch.delenv("PLANTUML_JAR", raising=False)


def test_check_reports_jar_and_java_when_a_jar_is_configured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    jar = tmp_path / "plantuml-test.jar"
    jar.write_bytes(b"")
    monkeypatch.setenv("PLANTUML_JAR", str(jar))
    tools = {name: (available, detail) for name, available, detail in render.check_tools()}
    assert tools["plantuml"] == (True, f"jar {jar.resolve()}")
    assert "java" in tools


def test_check_reports_missing_plantuml_with_install_hint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _without_plantuml_jar(monkeypatch, tmp_path)
    monkeypatch.setenv("PLANTUML_CMD", "plantuml-not-installed-anywhere")
    tools = {name: (available, detail) for name, available, detail in render.check_tools()}
    assert tools["plantuml"][0] is False
    assert "brew install plantuml" in tools["plantuml"][1]
    assert "java" not in tools, "java is only needed when a jar is used"
    assert render.main(["--check"]) == 1
    assert "MISSING plantuml" in capsys.readouterr().out


def test_missing_plantuml_fails_with_install_hint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _without_plantuml_jar(monkeypatch, tmp_path)
    monkeypatch.setenv("PLANTUML_CMD", "plantuml-not-installed-anywhere")
    diagram = tmp_path / "er.puml"
    diagram.write_text(ER_PLANTUML, encoding="utf-8")
    assert render.main([str(diagram)]) == 1
    output = capsys.readouterr().out
    assert "FAIL" in output
    assert "PLANTUML_JAR" in output and "--check" in output
    assert not diagram.with_suffix(".svg").exists()


@needs_local_jar
def test_plantuml_command_is_used_when_no_jar_is_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh clone ships no jar, so rendering must work through a `plantuml` command."""
    jar = validate_plantuml._resolve_plantuml_jar()
    command = tmp_path / "bin" / "plantuml"
    command.parent.mkdir()
    command.write_text(f'#!/bin/sh\nexec java -jar "{jar}" "$@"\n', encoding="utf-8")
    command.chmod(0o755)
    _without_plantuml_jar(monkeypatch, tmp_path)
    monkeypatch.setenv("PLANTUML_CMD", str(command))

    diagram = tmp_path / "er.puml"
    diagram.write_text(ER_PLANTUML, encoding="utf-8")
    assert render.main([str(diagram)]) == 0
    assert diagram.with_suffix(".svg").exists()
    # The DPI setting and the size limit must reach PlantUML through the command as well.
    assert _png_size(diagram.with_suffix(".png"))[0] > 400


@needs_mmdc
def test_state_diagram_renders(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """State diagrams were rejected by the old Node pre-parser; they must validate here."""
    diagram = tmp_path / "state.mmd"
    diagram.write_text(STATE_DIAGRAM, encoding="utf-8")
    assert render.main([str(diagram)]) == 0
    assert "OK" in capsys.readouterr().out
    assert diagram.with_suffix(".svg").exists()
    assert diagram.with_suffix(".png").exists()


@needs_mmdc
def test_broken_mermaid_fails_with_parser_message(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    diagram = tmp_path / "broken.mmd"
    diagram.write_text(BROKEN_STATE_DIAGRAM, encoding="utf-8")
    diagram.with_suffix(".svg").write_text("<svg>stale</svg>", encoding="utf-8")
    assert render.main([str(diagram)]) == 1
    output = capsys.readouterr().out
    assert "FAIL" in output
    assert "Parse error on line 3" in output
    assert not diagram.with_suffix(".svg").exists(), "a stale SVG must not survive a failed render"


@needs_plantuml
def test_plantuml_renders_png_at_high_resolution(tmp_path: Path) -> None:
    diagram = tmp_path / "er.puml"
    diagram.write_text(ER_PLANTUML, encoding="utf-8")
    assert render.main([str(diagram)]) == 0
    png = diagram.with_suffix(".png")
    assert diagram.with_suffix(".svg").exists()
    # PNG header: width is the big-endian integer at bytes 16..20. At 96 dpi this diagram is
    # about 130 px wide, so a clearly larger width proves the 600 dpi setting took effect.
    width = int.from_bytes(png.read_bytes()[16:20], "big")
    assert width > 400


@needs_plantuml
def test_broken_plantuml_fails_and_leaves_no_artifacts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    diagram = tmp_path / "broken.puml"
    diagram.write_text("@startuml\nclass {{{ broken\n@enduml\n", encoding="utf-8")
    assert render.main([str(diagram)]) == 1
    assert "FAIL" in capsys.readouterr().out
    assert not diagram.with_suffix(".svg").exists()
    assert not diagram.with_suffix(".png").exists()


def _png_size(png: Path) -> tuple[int, int]:
    header = png.read_bytes()[16:24]
    return int.from_bytes(header[:4], "big"), int.from_bytes(header[4:], "big")


@needs_plantuml
def test_large_plantuml_png_is_scaled_down_not_cropped(tmp_path: Path) -> None:
    """A diagram too large for 600 dpi must keep its full extent at a lower DPI."""
    classes = "\n".join(f"class Entity{i:02d} {{\n  --\n  ID_{i:02d} (PK)\n}}" for i in range(16))
    chain = "\n".join(f"Entity{i:02d} ||--o{{ Entity{i + 1:02d}" for i in range(15))
    diagram = tmp_path / "wide.puml"
    diagram.write_text(f"@startuml\nleft to right direction\n{classes}\n{chain}\n@enduml\n", encoding="utf-8")
    assert render.main([str(diagram)]) == 0

    svg_width, svg_height = svg_size.read_svg_size(diagram.with_suffix(".svg")) or (0.0, 0.0)
    png_width, png_height = _png_size(diagram.with_suffix(".png"))
    assert svg_width * 600 / 96 > svg_size.DEFAULT_MAX_PNG_SIDE_PX, "diagram is not large enough to test the cap"
    assert max(png_width, png_height) <= svg_size.DEFAULT_MAX_PNG_SIDE_PX
    # Cropping would change the aspect ratio; scaling keeps it.
    assert png_width / png_height == pytest.approx(svg_width / svg_height, rel=0.03)


@needs_mmdc
def test_wide_mermaid_png_is_capped_not_shrunk(tmp_path: Path) -> None:
    """A very wide diagram must fill the size limit instead of collapsing to the page width."""
    steps = "\n".join(f"    S{i}[Schritt {i}] --> S{i + 1}[Schritt {i + 1}]" for i in range(40))
    diagram = tmp_path / "wide.mmd"
    diagram.write_text(f"flowchart LR\n{steps}\n", encoding="utf-8")
    assert render.main([str(diagram)]) == 0

    svg_width, svg_height = svg_size.read_svg_size(diagram.with_suffix(".svg")) or (0.0, 0.0)
    png_width, png_height = _png_size(diagram.with_suffix(".png"))
    limit = svg_size.DEFAULT_MAX_PNG_SIDE_PX
    assert svg_width * 600 / 96 > limit, "diagram is not wide enough to test the cap"
    assert 0.97 * limit <= png_width <= limit
    assert png_width / png_height == pytest.approx(svg_width / svg_height, rel=0.1)


@needs_mmdc
def test_small_mermaid_png_is_rendered_at_target_dpi(tmp_path: Path) -> None:
    diagram = tmp_path / "state.mmd"
    diagram.write_text(STATE_DIAGRAM, encoding="utf-8")
    assert render.main([str(diagram)]) == 0
    svg_width, svg_height = svg_size.read_svg_size(diagram.with_suffix(".svg")) or (0.0, 0.0)
    png_width, png_height = _png_size(diagram.with_suffix(".png"))
    # Page-sized diagrams use the whole-number factor 6 (600 dpi would be 6.25).
    assert max(png_width, png_height) == pytest.approx(max(svg_width, svg_height) * 6, rel=0.03)


def test_png_size_args_scale_page_sized_and_size_wide_diagrams() -> None:
    assert mermaid_validator._build_png_size_args(600, (152.0, 299.0)) == ["--scale", "6"]
    assert mermaid_validator._build_png_size_args(600, (784.0, 196.0)) == ["--scale", "6"]
    # A tall diagram within the page width gets a smaller factor to respect the cap.
    assert mermaid_validator._build_png_size_args(600, (400.0, 3000.0)) == ["--scale", "2"]
    assert mermaid_validator._build_png_size_args(600, (1000.0, 300.0)) == ["--size", "6250"]
    assert mermaid_validator._build_png_size_args(600, (7848.0, 61.0)) == ["--size", "8192"]
    assert mermaid_validator._build_png_size_args(600, None) == ["--scale", "6"]


@needs_mmdc
def test_gantt_png_is_enlarged_not_relaid_out(tmp_path: Path) -> None:
    """Gantt charts fill the page width; the PNG must keep the SVG's aspect ratio."""
    diagram = tmp_path / "plan.mmd"
    diagram.write_text(
        "gantt\n    dateFormat YYYY-MM-DD\n    section A\n        Task :2024-01-01, 10d\n",
        encoding="utf-8",
    )
    assert render.main([str(diagram)]) == 0
    svg_width, svg_height = svg_size.read_svg_size(diagram.with_suffix(".svg")) or (0.0, 0.0)
    png_width, png_height = _png_size(diagram.with_suffix(".png"))
    assert png_width / png_height == pytest.approx(svg_width / svg_height, rel=0.05)
    assert png_width >= 5 * svg_width


def test_read_svg_size_from_viewbox(tmp_path: Path) -> None:
    svg = tmp_path / "a.svg"
    svg.write_text('<svg width="100%" viewBox="-8 -8 630.92 598"></svg>', encoding="utf-8")
    assert svg_size.read_svg_size(svg) == (630.92, 598.0)
    assert svg_size.read_svg_size(tmp_path / "missing.svg") is None
    svg.write_text("<svg></svg>", encoding="utf-8")
    assert svg_size.read_svg_size(svg) is None


def test_capped_dpi_keeps_target_for_small_and_lowers_for_large() -> None:
    assert svg_size.capped_dpi(600, (630.0, 598.0)) == 600
    assert svg_size.capped_dpi(600, None) == 600
    lowered = svg_size.capped_dpi(600, (4000.0, 1000.0))
    assert lowered == 196
    assert 4000 * lowered / 96 <= svg_size.DEFAULT_MAX_PNG_SIDE_PX
    # Never go below screen resolution, even for enormous diagrams ...
    assert svg_size.capped_dpi(600, (20000.0, 500.0)) == 96
    # ... and then the renderer's limit is raised so nothing is cropped.
    assert svg_size.png_side_limit(96, (20000.0, 500.0)) > 20000


def test_max_png_side_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DIAGRAMMER_MAX_PNG_SIDE", "4096")
    assert svg_size.max_png_side() == 4096
    monkeypatch.setenv("DIAGRAMMER_MAX_PNG_SIDE", "nonsense")
    assert svg_size.max_png_side() == svg_size.DEFAULT_MAX_PNG_SIDE_PX


def test_type_table_and_spec_files_match() -> None:
    """Every spec named in SKILL.md must exist, and every spec file must be reachable from it."""
    skill_dir = SCRIPTS_DIR.parent
    table = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    named = set(re.findall(r"`([A-Za-z0-9_]+\.md)`", table))
    existing = {path.name for path in (skill_dir / "specs").glob("*/*.md")}
    assert named - existing == set(), "SKILL.md names specs that do not exist"
    assert existing - named == set(), "spec files missing from the type table in SKILL.md"


@needs_plantuml
def test_plantuml_without_start_tag_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """PlantUML exits 0 for a fragment without @startuml but writes no image."""
    diagram = tmp_path / "fragment.puml"
    diagram.write_text("A ||--o{ B\n", encoding="utf-8")
    assert render.main([str(diagram)]) == 1
    assert "@startuml" in capsys.readouterr().out


@needs_plantuml
def test_plantuml_theme_does_not_lower_png_resolution(tmp_path: Path) -> None:
    """Themes such as spacelab set their own dpi; the PNG must still use the target DPI."""
    body = "class A\nclass B\nA --> B\n"
    plain = tmp_path / "plain.puml"
    plain.write_text(f"@startuml\n{body}@enduml\n", encoding="utf-8")
    themed = tmp_path / "themed.puml"
    themed.write_text(f"@startuml\n!theme spacelab\n{body}@enduml\n", encoding="utf-8")
    assert render.main([str(plain), str(themed)]) == 0
    assert _png_size(themed.with_suffix(".png"))[1] > 0.5 * _png_size(plain.with_suffix(".png"))[1]
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "plain.png", "plain.puml", "plain.svg", "themed.png", "themed.puml", "themed.svg",
    ]


def _flavour_setup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path, Path]:
    """Create empty project, user and skill flavour folders and point the lookup at them."""
    project = tmp_path / "project"
    user = tmp_path / "user"
    skill = tmp_path / "skill"
    for folder in (project / ".diagrammer" / "flavours", user, skill):
        folder.mkdir(parents=True)
    monkeypatch.setenv("DIAGRAMMER_USER_FLAVOURS", str(user))
    monkeypatch.setattr(flavours, "SKILL_FLAVOURS", skill)
    return project, user, skill


def test_flavours_most_specific_location_wins(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project, user, skill = _flavour_setup(tmp_path, monkeypatch)
    (skill / "general.txt").write_text("skill general", encoding="utf-8")
    (skill / "flowchart.txt").write_text("skill flowchart", encoding="utf-8")
    (user / "flowchart.txt").write_text("user flowchart", encoding="utf-8")
    (project / ".diagrammer" / "flavours" / "flowchart.txt").write_text("project", encoding="utf-8")

    found = flavours.find_flavours("flowchart.md", cwd=project)
    assert [(scope, path.read_text()) for scope, path in found] == [
        ("skill", "skill general"),
        ("project", "project"),
    ]
    # Another project without its own flavour falls back to the user's.
    other = tmp_path / "other"
    other.mkdir()
    assert [scope for scope, _ in flavours.find_flavours("flowchart", cwd=other)] == ["skill", "user"]
    assert flavours.find_flavours("gantt", cwd=other) == [("skill", skill / "general.txt")]


def test_user_flavours_are_found_in_the_neutral_and_the_claude_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    neutral = home / ".diagrammer" / "flavours"
    claude = home / ".claude" / "diagrammer" / "flavours"
    skill = tmp_path / "skill"
    for folder in (neutral, claude, skill):
        folder.mkdir(parents=True)
    monkeypatch.delenv("DIAGRAMMER_USER_FLAVOURS", raising=False)
    monkeypatch.setattr(Path, "home", lambda: home)
    monkeypatch.setattr(flavours, "SKILL_FLAVOURS", skill)
    (claude / "general.txt").write_text("claude", encoding="utf-8")
    (claude / "flowchart.txt").write_text("claude", encoding="utf-8")
    (neutral / "flowchart.txt").write_text("neutral", encoding="utf-8")

    found = flavours.find_flavours("flowchart", cwd=tmp_path)
    assert found == [("user", claude / "general.txt"), ("user", neutral / "flowchart.txt")]


def test_empty_project_flavour_switches_a_rule_off(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project, user, _skill = _flavour_setup(tmp_path, monkeypatch)
    (user / "general.txt").write_text("always dark", encoding="utf-8")
    (project / ".diagrammer" / "flavours" / "general.txt").write_text("", encoding="utf-8")
    found = flavours.find_flavours("flowchart", cwd=project)
    assert found == [("project", project / ".diagrammer" / "flavours" / "general.txt")]


def test_render_lists_flavours(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    project, _user, skill = _flavour_setup(tmp_path, monkeypatch)
    (skill / "flowchart.txt").write_text("x", encoding="utf-8")
    monkeypatch.chdir(project)
    assert render.main(["--flavours", "flowchart"]) == 0
    assert capsys.readouterr().out.split() == ["skill", str(skill / "flowchart.txt")]
    assert render.main(["--flavours", "gantt"]) == 0
    assert capsys.readouterr().out.strip() == "none"
