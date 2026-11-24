# Diagrammer Skills

A skill for [Claude Code](https://claude.com/claude-code) and
[Codex](https://developers.openai.com/codex) that draws a diagram from a text, a file or the
current project. You name the diagram type, the agent writes the diagram in Mermaid or
PlantUML, validates it with the real renderer and saves the source file together with an
SVG and a PNG.

```text
/diagrammer:diagrammer er
/diagrammer:diagrammer er plantuml docs/data-model.md
/diagrammer:diagrammer sequence login flow between browser, API and database
```

The skill does not guess the type. If it is missing or ambiguous, the skill asks and shows
the available types.

## Installation

### Claude Code: via the marketplace (recommended)

Enter these two commands in Claude Code:

```text
/plugin marketplace add hgrabows/diagrammer-skills
/plugin install diagrammer@diagrammer-skills
```

The first registers this repository as a marketplace, the second installs the skill from it.
The command is then `/diagrammer:diagrammer`.

### Claude Code: clone and link

The command is then the short `/diagrammer`, available in every project:

```bash
git clone https://github.com/hgrabows/diagrammer-skills.git
```

```bash
mkdir -p ~/.claude/skills && ln -s "$PWD/diagrammer-skills/skills/diagrammer" ~/.claude/skills/diagrammer
```

To use the skill in one project only, link it into that project's `.claude/skills/` folder
instead. Update with `git pull`.

### Codex: clone and link

```bash
git clone https://github.com/hgrabows/diagrammer-skills.git
```

```bash
mkdir -p ~/.codex/skills && ln -s "$PWD/diagrammer-skills/skills/diagrammer" ~/.codex/skills/diagrammer
```

Start Codex anew afterwards. Call the skill with `$diagrammer` followed by the same
arguments, for example `$diagrammer er plantuml docs/data-model.md`, or just ask for a
diagram of a named type. Update with `git pull`.

Mermaid renders through a headless browser, which the Codex sandbox does not let start. When
Codex asks whether it may run `render.py` outside the sandbox, allow it; without that it
writes the `.mmd` file but no SVG or PNG. PlantUML diagrams render inside the sandbox.

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
| Mermaid | ER diagram, class diagram, mindmap, sequence diagram, flowchart, state diagram, Gantt, timeline, architecture, C4, block, GitGraph, Kanban, user journey, requirement, pie, XY chart, quadrant, radar, Sankey, treemap, packet, ZenUML, use case, swimlane, Venn, Ishikawa (fishbone), TreeView, Wardley map, Cynefin, Event Modeling, railroad (syntax) diagram, Agent Flow |
| PlantUML | ER diagram (a custom notation based on the class diagram, without data types), class diagram, mindmap |

The keywords for each type are listed in [SKILL.md](skills/diagrammer/SKILL.md).

## Examples

One example per diagram type, taken from the specs the skill reads. Click a picture for its
source; the SVG and the PNG are next to it in [examples/](examples/). The pictures show the
default look of Mermaid 12.

<!-- gallery:start -->
<table>
<tr><td align="center" width="33%"><a href="examples/flowchart.mmd"><img src="examples/flowchart.png" alt="Flowchart" height="180"></a><br><sub>Flowchart</sub></td><td align="center" width="33%"><a href="examples/sequenceDiagram.mmd"><img src="examples/sequenceDiagram.png" alt="Sequence diagram" height="180"></a><br><sub>Sequence diagram</sub></td><td align="center" width="33%"><a href="examples/classDiagram.mmd"><img src="examples/classDiagram.png" alt="Class diagram" height="180"></a><br><sub>Class diagram</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/stateDiagram.mmd"><img src="examples/stateDiagram.png" alt="State diagram" height="180"></a><br><sub>State diagram</sub></td><td align="center" width="33%"><a href="examples/entityRelationshipDiagram.mmd"><img src="examples/entityRelationshipDiagram.png" alt="ER diagram" height="180"></a><br><sub>ER diagram</sub></td><td align="center" width="33%"><a href="examples/userJourney.mmd"><img src="examples/userJourney.png" alt="User journey" height="180"></a><br><sub>User journey</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/gantt.mmd"><img src="examples/gantt.png" alt="Gantt" height="180"></a><br><sub>Gantt</sub></td><td align="center" width="33%"><a href="examples/pieChart.mmd"><img src="examples/pieChart.png" alt="Pie chart" height="180"></a><br><sub>Pie chart</sub></td><td align="center" width="33%"><a href="examples/quadrantChart.mmd"><img src="examples/quadrantChart.png" alt="Quadrant chart" height="180"></a><br><sub>Quadrant chart</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/requirementDiagram.mmd"><img src="examples/requirementDiagram.png" alt="Requirement diagram" height="180"></a><br><sub>Requirement diagram</sub></td><td align="center" width="33%"><a href="examples/gitGraph.mmd"><img src="examples/gitGraph.png" alt="GitGraph" height="180"></a><br><sub>GitGraph</sub></td><td align="center" width="33%"><a href="examples/c4Diagram.mmd"><img src="examples/c4Diagram.png" alt="C4" height="180"></a><br><sub>C4</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/mindmap.mmd"><img src="examples/mindmap.png" alt="Mindmap" height="180"></a><br><sub>Mindmap</sub></td><td align="center" width="33%"><a href="examples/timeline.mmd"><img src="examples/timeline.png" alt="Timeline" height="180"></a><br><sub>Timeline</sub></td><td align="center" width="33%"><a href="examples/zenuml.mmd"><img src="examples/zenuml.png" alt="ZenUML" height="180"></a><br><sub>ZenUML</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/sankeyDiagram.mmd"><img src="examples/sankeyDiagram.png" alt="Sankey" height="180"></a><br><sub>Sankey</sub></td><td align="center" width="33%"><a href="examples/xyChart.mmd"><img src="examples/xyChart.png" alt="XY chart" height="180"></a><br><sub>XY chart</sub></td><td align="center" width="33%"><a href="examples/blockDiagram.mmd"><img src="examples/blockDiagram.png" alt="Block diagram" height="180"></a><br><sub>Block diagram</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/packet.mmd"><img src="examples/packet.png" alt="Packet" height="180"></a><br><sub>Packet</sub></td><td align="center" width="33%"><a href="examples/kanban.mmd"><img src="examples/kanban.png" alt="Kanban" height="180"></a><br><sub>Kanban</sub></td><td align="center" width="33%"><a href="examples/architectureDiagram.mmd"><img src="examples/architectureDiagram.png" alt="Architecture" height="180"></a><br><sub>Architecture</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/radar.mmd"><img src="examples/radar.png" alt="Radar" height="180"></a><br><sub>Radar</sub></td><td align="center" width="33%"><a href="examples/treemap.mmd"><img src="examples/treemap.png" alt="Treemap" height="180"></a><br><sub>Treemap</sub></td><td align="center" width="33%"><a href="examples/useCase.mmd"><img src="examples/useCase.png" alt="Use case" height="180"></a><br><sub>Use case</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/swimlane.mmd"><img src="examples/swimlane.png" alt="Swimlane" height="180"></a><br><sub>Swimlane</sub></td><td align="center" width="33%"><a href="examples/venn.mmd"><img src="examples/venn.png" alt="Venn" height="180"></a><br><sub>Venn</sub></td><td align="center" width="33%"><a href="examples/ishikawa.mmd"><img src="examples/ishikawa.png" alt="Ishikawa" height="180"></a><br><sub>Ishikawa</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/treeView.mmd"><img src="examples/treeView.png" alt="TreeView" height="180"></a><br><sub>TreeView</sub></td><td align="center" width="33%"><a href="examples/wardley.mmd"><img src="examples/wardley.png" alt="Wardley map" height="180"></a><br><sub>Wardley map</sub></td><td align="center" width="33%"><a href="examples/cynefin.mmd"><img src="examples/cynefin.png" alt="Cynefin" height="180"></a><br><sub>Cynefin</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/eventModeling.mmd"><img src="examples/eventModeling.png" alt="Event Modeling" height="180"></a><br><sub>Event Modeling</sub></td><td align="center" width="33%"><a href="examples/railroad.mmd"><img src="examples/railroad.png" alt="Railroad" height="180"></a><br><sub>Railroad</sub></td><td align="center" width="33%"><a href="examples/agentFlow.mmd"><img src="examples/agentFlow.png" alt="Agent Flow" height="180"></a><br><sub>Agent Flow</sub></td></tr>
<tr><td align="center" width="33%"><a href="examples/plantuml_er.puml"><img src="examples/plantuml_er.png" alt="ER diagram (PlantUML)" height="180"></a><br><sub>ER diagram (PlantUML)</sub></td><td align="center" width="33%"><a href="examples/plantuml_class.puml"><img src="examples/plantuml_class.png" alt="Class diagram (PlantUML)" height="180"></a><br><sub>Class diagram (PlantUML)</sub></td><td align="center" width="33%"><a href="examples/plantuml_mindmap.puml"><img src="examples/plantuml_mindmap.png" alt="Mindmap (PlantUML)" height="180"></a><br><sub>Mindmap (PlantUML)</sub></td></tr>
</table>
<!-- gallery:end -->

## Requirements

| For | Needed | Installation |
| --- | --- | --- |
| Mermaid | Node.js 22.12+ and the Mermaid CLI `mmdc`, version 12 or newer | `npm install -g @mermaid-js/mermaid-cli` |
| PlantUML | PlantUML and Graphviz | macOS: `brew install plantuml graphviz` |

PlantUML is only needed for the three PlantUML variants. Instead of installing it, a PlantUML
jar from <https://plantuml.com/download> together with Java is enough: set the environment
variable `PLANTUML_JAR` to its path (for Claude Code, for example under `env` in
`~/.claude/settings.json`), or, in a cloned copy, put it into `skills/diagrammer/vendor/`.

To see what is present on your machine and what is missing, run this in a cloned copy:

```bash
python3 skills/diagrammer/scripts/render.py --check
```

Tested on macOS with Mermaid CLI 12.2 (Mermaid 12.3) and PlantUML 1.2025.10.

## Customising

### Style rules ("flavours")

A flavour is a plain text file with your own wishes for how diagrams look, for example
colours, direction or label length. The agent reads it in addition to the spec, which always
wins on syntax. `general.txt` applies to every diagram, `<spec name>.txt` to one type, for
example `flowchart.txt`, `stateDiagram.txt` or `plantuml_er.txt` (the spec names are in
[skills/diagrammer/specs/](skills/diagrammer/specs/)).

Flavours can live in three places:

| Place | Folder | Use it for |
| --- | --- | --- |
| Project | `.diagrammer/flavours/` in the project | the look of one project, e.g. company colours |
| User | `~/.diagrammer/flavours/` or `~/.claude/diagrammer/flavours/` | your personal defaults in every project |
| Skill | `skills/diagrammer/flavours/` | the defaults shipped with the skill |

Both user folders work with either agent; if both hold a file of the same name, the one in
`~/.diagrammer/flavours/` is taken.

How the agent picks them for a diagram:

1. It looks for `general.txt` in the project, then in the user folders, then in the skill, and
   takes the **first one it finds**. The others are ignored, not added.
2. It does the same for the type's file, for example `flowchart.txt`.
3. It reads those two files (at most two). Where they disagree, the type's file wins.

So a project file **replaces** the user's or the skill's file of the same name; it does not
extend it. If a project's `flowchart.txt` should keep a rule from your user `flowchart.txt`,
copy that rule into it. An empty file switches a rule off for that project. The user and
project folders survive plugin updates; the skill folder does not.

Example: you keep `general.txt` ("transparent background") and `flowchart.txt` ("blue
nodes") in your user folder, and one project has its own `flowchart.txt` ("green nodes").

| Diagram | In that project | In any other project |
| --- | --- | --- |
| Flowchart | transparent background, **green** nodes | transparent background, blue nodes |
| Sequence diagram | transparent background | transparent background |

To see which files apply in the current folder, run this in a cloned copy (the agent
runs it for you on every call):

```bash
python3 skills/diagrammer/scripts/render.py --flavours flowchart
```

Example `.diagrammer/flavours/flowchart.txt` in a project:

```text
Use left-to-right direction.
Fill decision nodes with #FFE4B5, all other nodes with #E0F0FF.
Keep node labels under four words.
```

### Other settings

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

After updating Mermaid or PlantUML, or after editing a spec, render every example of all
specs and list the ones that fail:

```bash
python3 tools/sweep_specs.py /tmp/diagrammer-sweep
```

Repository layout:

```text
skills/diagrammer/
  SKILL.md      instructions the agent reads when the skill is invoked
  specs/        syntax specs per diagram type
  flavours/     style rules
  scripts/      render.py validates and renders a diagram file
  vendor/       place for a PlantUML jar (not version-controlled)
tests/          tests for the scripts
tools/          sweep_specs.py renders every example in the specs
```

## License

MIT License with the "Commons Clause": you may use, modify and share the software, but not
sell it or a service whose value derives substantially from it. The full text is in
[LICENSE](LICENSE). Mermaid and PlantUML are not included and come under their own licenses.
