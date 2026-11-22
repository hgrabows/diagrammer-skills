---
name: diagrammer
description: Creates a Mermaid or PlantUML diagram of an explicitly named type (ER diagram, sequence diagram, flowchart, class diagram, state diagram, mindmap, Gantt, C4, use case, swimlane, Venn, Ishikawa and more) from a text, a file or the current project, validates it with the real renderer and saves the source file together with an SVG and a PNG. Use when the user invokes /diagrammer or wants a rendered diagram file (Mermaid, PlantUML, SVG, PNG).
argument-hint: "<type> [mermaid|plantuml] [source or instruction]"
---

# Diagrammer

Create exactly one diagram of the named type, validate it with the real renderer and deliver
the source file, an SVG and a PNG.

Arguments of this call: `$ARGUMENTS`

Examples:

- `/diagrammer er` – ER diagram of whatever the conversation is currently about
- `/diagrammer er plantuml docs/data-model.md` – PlantUML variant from a file
- `/diagrammer sequence login flow between browser, API and database`

Paths in these instructions are relative to this skill's directory: `${CLAUDE_SKILL_DIR}`
(the "Base directory" named when the skill is loaded).

Talk to the user in the language they write in.

## Steps

1. **Determine the type.** Match the first argument by meaning to one row of the table below
   (`ER diagram`, `state machine` and `Sequenzdiagramm` are unambiguous even if they are not
   listed literally). The user picks the type deliberately, so there is no automatic type
   selection: if the first argument is not a type (for example only a file path), matches no
   row, or matches two rows equally well, list the available types compactly (one keyword
   per type) and ask. Do not read the source in order to suggest a type yourself. If
   `plantuml` or `mermaid` is given, use that engine; otherwise Mermaid.

2. **Determine the source.** The rest of the arguments is a file path (read it), a text or an
   instruction. Without further arguments the source is what the conversation is currently
   about, or the current project (for example tables for an ER diagram, code for a sequence
   diagram). If it is not clear what should be shown, ask briefly.

3. **Read the spec.** Read exactly the one file from the table, that is
   `specs/mermaid/<file>` or `specs/plantuml/<file>`. It describes the syntax the installed
   renderer accepts. Follow it rather than memory, because the newer Mermaid types in
   particular change their syntax between versions.

4. **Read style rules, if present.** `flavours/general.txt` applies to all diagrams,
   `flavours/<spec name without .md>.txt` to the respective type (example:
   `flavours/stateDiagram.txt`). The type-specific rule overrides the general one; neither
   may contradict the spec. A missing file means there is no rule.

5. **Write the diagram.** First state the core message of the source for yourself in one or
   two sentences and build the diagram around it: better the essentials clearly than
   everything completely. Label in the language of the source; if that is not clear (as with
   SQL or code), in the language the user writes in. Names from the source (tables, columns,
   classes, functions) stay unchanged.
   Save as `diagrams/<topic>_<type>.mmd` (Mermaid) or `.puml` (PlantUML) in the current
   working directory unless the user names another place. `<topic>` is a short lowercase
   keyword, `<type>` the first keyword of the table row, for example `library_er.puml` or
   `login_sequence.mmd`. The file contains only the diagram code, no Markdown fences. Do not
   overwrite an existing different diagram; choose another name instead.

6. **Render and validate.**

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" <path to the diagram file>
   ```

   `OK` means: syntax valid, SVG and PNG are next to the source file. `FAIL` gives the
   renderer's error message, usually with a line number; there is no SVG or PNG then.

7. **Fix on `FAIL`.** Map the message to the affected line, compare with the spec, change
   that place and render again. Do not submit the same version twice. If the third fix fails
   as well, report that openly with the last error message. A diagram only counts as done
   once `render.py` has reported `OK`.

8. **Look at the image.** `OK` only means the syntax is valid, not that the image shows what
   was meant. Open the PNG and check: do elements and connections match the source, are
   there orphaned or unintended nodes, do labels overlap, is anything hidden by lines? The
   PNG is high resolution and is scaled down when viewed; if a spot looks cramped, shorten
   the label there or loosen the layout. Improve at most twice and render again each time.

9. **Report the result.** Give the paths of source file, SVG and PNG and say in one sentence
   what the diagram shows. Nothing more is needed.

## Changing an existing diagram

If the user asks for changes ("label the arrows", "add the table Invoice"), edit the existing
source file and repeat steps 6 to 9. The spec of the type still applies.

## Types

Mermaid is the default. ER diagram, class diagram and mindmap also exist as a PlantUML
variant; it is used only with the addition `plantuml`. The keywords are recognition aids in
English and German, not a fixed spelling: hyphens, upper and lower case and additions such as
"diagram" or "-diagramm" do not matter.

| The user says | Mermaid (`specs/mermaid/`) | PlantUML (`specs/plantuml/`) |
| --- | --- | --- |
| er, erd, entity-relationship, data model, datenmodell | `entityRelationshipDiagram.md` | `plantuml_er.md` |
| class, classes, klasse, klassen | `classDiagram.md` | `plantuml_class.md` |
| mindmap | `mindmap.md` | `plantuml_mindmap.md` |
| sequence, interaction, messages, sequenz, nachrichten | `sequenceDiagram.md` | – |
| flowchart, flow, process, fluss, ablauf, prozess | `flowchart.md` | – |
| state, state machine, zustand, zustandsautomat | `stateDiagram.md` | – |
| gantt, schedule, project plan, zeitplan, projektplan | `gantt.md` | – |
| timeline, chronology, zeitstrahl, chronologie | `timeline.md` | – |
| architecture, architektur | `architectureDiagram.md` | – |
| c4 | `c4Diagram.md` | – |
| block | `blockDiagram.md` | – |
| git, gitgraph, branches | `gitGraph.md` | – |
| kanban | `kanban.md` | – |
| journey, user journey, nutzerreise | `userJourney.md` | – |
| requirement, anforderung | `requirementDiagram.md` | – |
| pie, torte, kreis | `pieChart.md` | – |
| xy, xychart, line, bar, linie, balken | `xyChart.md` | – |
| quadrant | `quadrantChart.md` | – |
| radar, spider, netz, spinnennetz | `radar.md` | – |
| sankey, mengenfluss | `sankeyDiagram.md` | – |
| treemap, kacheldiagramm | `treemap.md` | – |
| packet, protocol header, paket, protokollkopf | `packet.md` | – |
| zenuml | `zenuml.md` | – |
| usecase, use case, anwendungsfall | `useCase.md` | – |
| swimlane, swim lanes, lanes, schwimmbahn | `swimlane.md` | – |
| venn, mengen, mengendiagramm | `venn.md` | – |
| ishikawa, fishbone, cause and effect, fischgräte, ursache-wirkung | `ishikawa.md` | – |
| treeview, tree view, folder tree, file tree, ordnerbaum, verzeichnisbaum | `treeView.md` | – |
| wardley, wardley map | `wardley.md` | – |
| cynefin | `cynefin.md` | – |
| event modeling, eventmodeling, event model | `eventModeling.md` | – |
| railroad, syntax diagram, grammar, ebnf, syntaxdiagramm, grammatik | `railroad.md` | – |
| agentflow, agent flow, agent workflow | `agentFlow.md` | – |

## Requirements

Mermaid needs `node` and the Mermaid CLI `mmdc` in version 12 or newer. PlantUML needs the `plantuml` command or a
PlantUML jar with `java` (environment variable `PLANTUML_JAR` or a jar in the `vendor/`
folder), and for class and ER diagrams also Graphviz (`dot`). If `render.py` reports that a
tool is missing,

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --check
```

shows what is missing and how to install it. Do not install anything unasked: tell the user
the missing tool and its install command instead of presenting an unvalidated diagram as
done.
