# Diagrammer-Skills

Ein Skill für [Claude Code](https://claude.com/claude-code), der aus einem Text, einer Datei
oder dem aktuellen Projekt ein Diagramm zeichnet. Du nennst den Diagrammtyp, Claude schreibt
das Diagramm in Mermaid oder PlantUML, prüft es mit dem echten Renderer und legt die
Quelldatei samt SVG und PNG ab.

```text
/diagrammer er-diagramm
/diagrammer er plantuml docs/datenmodell.md
/diagrammer sequenz Login-Ablauf zwischen Browser, API und Datenbank
```

Der Skill rät den Typ nicht. Fehlt er oder ist er mehrdeutig, fragt der Skill nach und zeigt
die verfügbaren Typen.

## Aufruf

```text
/diagrammer <typ> [mermaid|plantuml] [quelle oder anweisung]
```

- **Typ:** ein Stichwort aus der Liste unten, deutsch oder englisch (`er`, `sequenz`,
  `zustand`, `flowchart`, `class`, …).
- **Engine:** Standard ist Mermaid. Mit dem Zusatz `plantuml` entsteht die PlantUML-Variante;
  die gibt es für ER-Diagramm, Klassendiagramm und Mindmap.
- **Quelle:** ein Dateipfad, ein Text oder eine Anweisung. Ohne Angabe nimmt der Skill das,
  worüber gerade gesprochen wird, oder das aktuelle Projekt.

Das Ergebnis liegt in `diagrams/` im aktuellen Ordner, zum Beispiel `bibliothek_er.puml`,
`bibliothek_er.svg` und `bibliothek_er.png`.

## Diagrammtypen

| Engine | Typen |
| --- | --- |
| Mermaid | ER-Diagramm, Klassendiagramm, Mindmap, Sequenzdiagramm, Flowchart, Zustandsdiagramm, Gantt, Timeline, Architektur, C4, Block, GitGraph, Kanban, User Journey, Requirement, Pie, XY-Chart, Quadrant, Radar, Sankey, Treemap, Packet, ZenUML |
| PlantUML | ER-Diagramm (eigene Schreibweise auf Basis des Klassendiagramms, ohne Datentypen), Klassendiagramm, Mindmap |

Die Stichwörter zu jedem Typ stehen in [SKILL.md](skills/diagrammer/SKILL.md).

## Voraussetzungen

| Für | Wird gebraucht | Installation |
| --- | --- | --- |
| Mermaid | Node.js und die Mermaid-CLI `mmdc` | `npm install -g @mermaid-js/mermaid-cli` |
| PlantUML | PlantUML und Graphviz | macOS: `brew install plantuml graphviz` |

PlantUML wird nur für die drei PlantUML-Varianten gebraucht. Statt der Installation genügt
auch eine PlantUML-jar von <https://plantuml.com/download> zusammen mit Java: Lege sie in
`skills/diagrammer/vendor/` oder setze die Umgebungsvariable `PLANTUML_JAR` auf ihren Pfad.

Was auf deinem Rechner vorhanden ist und was fehlt, zeigt:

```bash
python3 skills/diagrammer/scripts/render.py --check
```

Getestet unter macOS mit Mermaid-CLI 11.12 und PlantUML 1.2025.10.

## Installation

### Über den Marketplace (empfohlen)

Gib in Claude Code diese beiden Befehle ein:

```text
/plugin marketplace add hgrabows/diagrammer-skills
/plugin install diagrammer@diagrammer-skills
```

Der erste macht dieses Repository als Marketplace bekannt, der zweite installiert den Skill
daraus. Der Befehl heißt dann `/diagrammer:diagrammer`, zum Beispiel
`/diagrammer:diagrammer er-diagramm`.

### Alternative: klonen und verlinken

Der Befehl heißt dann kurz `/diagrammer` und steht in jedem Projekt zur Verfügung:

```bash
git clone https://github.com/hgrabows/diagrammer-skills.git
```

```bash
mkdir -p ~/.claude/skills && ln -s "$PWD/diagrammer-skills/skills/diagrammer" ~/.claude/skills/diagrammer
```

Soll der Skill nur in einem bestimmten Projekt gelten, verlinke ihn stattdessen in dessen
Ordner `.claude/skills/`. Aktualisiert wird mit `git pull`.

## Anpassen

- **Stilvorgaben:** Textdateien in [skills/diagrammer/flavours/](skills/diagrammer/flavours/).
  `general.txt` gilt für alle Diagramme, `<name der spezifikation>.txt` für einen Typ, zum
  Beispiel `stateDiagram.txt` oder `plantuml_class.txt`.
- **Syntax:** je eine Spezifikation pro Typ in
  [skills/diagrammer/specs/](skills/diagrammer/specs/). Pro Aufruf liest der Skill genau
  eine davon.
- **PNG-Auflösung:** Standard sind 600 dpi, bei großen Diagrammen weniger, damit die längste
  Kante höchstens 8192 Pixel hat. Ändern lässt sich das über `MMDC_PNG_DPI`,
  `PLANTUML_PNG_DPI` und `DIAGRAMMER_MAX_PNG_SIDE`.

## Entwicklung

```bash
uvx pytest -q tests
```

Tests, die Mermaid oder PlantUML brauchen, werden übersprungen, wenn das Werkzeug fehlt.

Aufbau des Repositorys:

```text
skills/diagrammer/
  SKILL.md      Anleitung, die Claude beim Aufruf liest
  specs/        Syntax-Spezifikationen je Diagrammtyp
  flavours/     Stilvorgaben
  scripts/      render.py prüft und rendert eine Diagrammdatei
  vendor/       Platz für eine PlantUML-jar (nicht mitversioniert)
tests/          Tests für die Skripte
```

## Lizenz

MIT-Lizenz mit „Commons Clause“: Nutzen, Ändern und Weitergeben sind erlaubt, das Verkaufen
der Software oder eines Dienstes, dessen Wert im Wesentlichen auf ihr beruht, nicht. Der
volle Text steht in [LICENSE](LICENSE). Mermaid und PlantUML werden nicht mitgeliefert und
stehen unter ihren eigenen Lizenzen.
