# Diagrammer Skills

A skill for [Claude Code](https://claude.com/claude-code) that draws a diagram from a text, a
file or the current project. You name the diagram type, Claude writes the diagram in Mermaid
or PlantUML, validates it with the real renderer and saves the source file together with an
SVG and a PNG.

```text
/diagrammer:diagrammer er
/diagrammer:diagrammer er plantuml docs/data-model.md
/diagrammer:diagrammer sequence login flow between browser, API and database
```

The skill does not guess the type. If it is missing or ambiguous, the skill asks and shows
the available types.

## Installation

### Via the marketplace (recommended)

Enter these two commands in Claude Code:

```text
/plugin marketplace add hgrabows/diagrammer-skills
/plugin install diagrammer@diagrammer-skills
```

The first registers this repository as a marketplace, the second installs the skill from it.
The command is then `/diagrammer:diagrammer`.

### Alternative: clone and link

The command is then the short `/diagrammer`, available in every project:

```bash
git clone https://github.com/hgrabows/diagrammer-skills.git
```

```bash
mkdir -p ~/.claude/skills && ln -s "$PWD/diagrammer-skills/skills/diagrammer" ~/.claude/skills/diagrammer
```

To use the skill in one project only, link it into that project's `.claude/skills/` folder
instead. Update with `git pull`.

## Usage

```text
/diagrammer:diagrammer <type> [mermaid|plantuml] [source or instruction]
```

- **Type:** a keyword from the list below, in English or German (`er`, `sequence`, `state`,
  `flowchart`, `class`, …).
- **Engine:** Mermaid is the default. Adding `plantuml` produces the PlantUML variant, which
  exists for ER diagram, class diagram and mindmap.
- **Source:** a file path, a text or an instruction. Without one, the skill uses what the
  conversation is currently about, or the current project.

The result is written to `diagrams/` in the current folder, for example `library_er.puml`,
`library_er.svg` and `library_er.png`. Labels follow the language of the source.

## Diagram types

| Engine | Types |
| --- | --- |
| Mermaid | ER diagram, class diagram, mindmap, sequence diagram, flowchart, state diagram, Gantt, timeline, architecture, C4, block, GitGraph, Kanban, user journey, requirement, pie, XY chart, quadrant, radar, Sankey, treemap, packet, ZenUML |
| PlantUML | ER diagram (a custom notation based on the class diagram, without data types), class diagram, mindmap |

The keywords for each type are listed in [SKILL.md](skills/diagrammer/SKILL.md).

## Requirements

| For | Needed | Installation |
| --- | --- | --- |
| Mermaid | Node.js and the Mermaid CLI `mmdc` | `npm install -g @mermaid-js/mermaid-cli` |
| PlantUML | PlantUML and Graphviz | macOS: `brew install plantuml graphviz` |

PlantUML is only needed for the three PlantUML variants. Instead of installing it, a PlantUML
jar from <https://plantuml.com/download> together with Java is enough: set the environment
variable `PLANTUML_JAR` to its path (for Claude Code, for example under `env` in
`~/.claude/settings.json`), or, in a cloned copy, put it into `skills/diagrammer/vendor/`.

To see what is present on your machine and what is missing, run this in a cloned copy:

```bash
python3 skills/diagrammer/scripts/render.py --check
```

Tested on macOS with Mermaid CLI 11.12 and PlantUML 1.2025.10.

## Customising

- **Style rules:** text files in [skills/diagrammer/flavours/](skills/diagrammer/flavours/).
  `general.txt` applies to all diagrams, `<spec name>.txt` to one type, for example
  `stateDiagram.txt` or `plantuml_class.txt`.
- **Syntax:** one spec per type in [skills/diagrammer/specs/](skills/diagrammer/specs/). The
  skill reads exactly one of them per call.
- **PNG resolution:** 600 dpi by default, less for large diagrams so that the longest side
  stays within 8192 pixels. Change it with `MMDC_PNG_DPI`, `PLANTUML_PNG_DPI` and
  `DIAGRAMMER_MAX_PNG_SIDE`.

## Development

```bash
uvx pytest -q tests
```

Tests that need Mermaid or PlantUML are skipped when the tool is missing.

Repository layout:

```text
skills/diagrammer/
  SKILL.md      instructions Claude reads when the skill is invoked
  specs/        syntax specs per diagram type
  flavours/     style rules
  scripts/      render.py validates and renders a diagram file
  vendor/       place for a PlantUML jar (not version-controlled)
tests/          tests for the scripts
```

## License

MIT License with the "Commons Clause": you may use, modify and share the software, but not
sell it or a service whose value derives substantially from it. The full text is in
[LICENSE](LICENSE). Mermaid and PlantUML are not included and come under their own licenses.
