---
name: diagrammer
description: Erzeugt ein Mermaid- oder PlantUML-Diagramm eines ausdrücklich genannten Typs (ER-Diagramm, Sequenzdiagramm, Flowchart, Klassendiagramm, Zustandsdiagramm, Mindmap, Gantt, C4 und weitere) aus einem Text, einer Datei oder dem aktuellen Projekt, prüft es mit dem echten Renderer und legt die Quelldatei samt SVG und PNG ab. Verwenden, wenn der Nutzer /diagrammer aufruft oder eine gerenderte Diagrammdatei (Mermaid, PlantUML, SVG, PNG) haben möchte.
argument-hint: "<typ> [mermaid|plantuml] [quelle oder anweisung]"
---

# Diagrammer

Erzeuge genau ein Diagramm des genannten Typs, prüfe es mit dem echten Renderer und liefere
Quelldatei, SVG und PNG.

Argumente dieses Aufrufs: `$ARGUMENTS`

Beispiele:

- `/diagrammer er-diagramm` – ER-Diagramm aus dem, worüber gerade gesprochen wird
- `/diagrammer er plantuml docs/datenmodell.md` – PlantUML-Variante aus einer Datei
- `/diagrammer sequenz Login-Ablauf zwischen Browser, API und Datenbank`

Pfade in dieser Anleitung sind relativ zum Verzeichnis dieses Skills: `${CLAUDE_SKILL_DIR}`
(das „Base directory“, das beim Laden genannt wird).

## Ablauf

1. **Typ bestimmen.** Ordne das erste Argument sinngemäß einer Zeile der Tabelle unten zu
   (`ER-Diagramm`, `Zustandsdiagramm` und `sequence diagram` sind eindeutig, auch wenn sie
   nicht wörtlich dastehen). Der Nutzer wählt den Typ bewusst selbst, deshalb gibt es keine
   automatische Typwahl: Ist das erste Argument kein Typ (etwa nur ein Dateipfad), passt es
   zu keiner Zeile oder zu zwei Zeilen gleich gut, dann nenne die verfügbaren Typen kompakt
   (ein Stichwort pro Typ) und frage nach. Lies dafür nicht die Quelle, um selbst einen Typ
   vorzuschlagen. Steht `plantuml` oder `mermaid` dabei, gilt diese Engine; sonst Mermaid.

2. **Quelle bestimmen.** Der Rest der Argumente ist entweder ein Dateipfad (dann lesen), ein
   Text oder eine Anweisung. Ohne weitere Argumente ist die Quelle das, worum es im Gespräch
   gerade geht, oder das aktuelle Projekt (z. B. Tabellen für ein ER-Diagramm, Code für ein
   Sequenzdiagramm). Ist nicht erkennbar, was dargestellt werden soll, frage kurz nach.

3. **Spezifikation lesen.** Lies genau die eine Datei aus der Tabelle, also
   `specs/mermaid/<datei>` oder `specs/plantuml/<datei>`. Sie beschreibt die Syntax, die der
   installierte Renderer annimmt. Halte dich daran statt an die Erinnerung, denn gerade die
   neueren Mermaid-Typen ändern ihre Syntax zwischen Versionen.

4. **Stilvorgaben lesen, falls vorhanden.** `flavours/general.txt` gilt für alle Diagramme,
   `flavours/<name der spec ohne .md>.txt` für den jeweiligen Typ (Beispiel:
   `flavours/stateDiagram.txt`). Die typspezifische Vorgabe geht vor der allgemeinen; keine
   von beiden darf der Spezifikation widersprechen. Fehlt eine Datei, gibt es keine Vorgabe.

5. **Diagramm schreiben.** Formuliere zuerst für dich die Kernaussage der Quelle in ein bis
   zwei Sätzen und richte das Diagramm daran aus: lieber das Wesentliche klar als alles
   vollständig. Beschrifte in der Sprache der Quelle; ist die nicht eindeutig (etwa bei SQL
   oder Code), in der Sprache, in der der Nutzer schreibt. Namen aus der Quelle (Tabellen,
   Spalten, Klassen, Funktionen) bleiben unverändert.
   Speichere als `diagrams/<thema>_<typ>.mmd` (Mermaid) oder `.puml` (PlantUML) im aktuellen
   Arbeitsverzeichnis, außer der Nutzer nennt einen anderen Ort. `<thema>` ist ein kurzes
   Stichwort in Kleinbuchstaben, `<typ>` das erste Stichwort der Tabellenzeile, zum Beispiel
   `bibliothek_er.puml` oder `login_sequenz.mmd`. Die Datei enthält nur den Diagrammcode,
   ohne Markdown-Zäune. Überschreibe kein vorhandenes anderes Diagramm; wähle dann einen
   anderen Namen.

6. **Rendern und prüfen.**

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" <pfad zur diagrammdatei>
   ```

   `OK` bedeutet: Syntax gültig, SVG und PNG liegen neben der Quelldatei. `FAIL` liefert die
   Fehlermeldung des Renderers, meist mit Zeilennummer; SVG und PNG gibt es dann nicht.

7. **Bei `FAIL` korrigieren.** Ordne die Meldung der betroffenen Zeile zu, vergleiche mit der
   Spezifikation, ändere die Stelle und rendere erneut. Gib nicht dieselbe Fassung noch
   einmal ab. Schlägt auch die dritte Korrektur fehl, melde das offen mit der letzten
   Fehlermeldung. Ein Diagramm gilt erst als fertig, wenn `render.py` `OK` gemeldet hat.

8. **Bild ansehen.** `OK` heißt nur, dass die Syntax stimmt, nicht, dass das Bild das
   Gemeinte zeigt. Öffne das PNG und prüfe: Stimmen Elemente und Verbindungen mit der Quelle
   überein, gibt es verwaiste oder unbeabsichtigte Knoten, überlappen Beschriftungen, wird
   etwas von Linien verdeckt? Das PNG ist hochaufgelöst und wird beim Ansehen verkleinert;
   wirkt eine Stelle eng, kürze dort die Beschriftung oder entzerre das Layout. Bessere
   höchstens zweimal nach und rendere jeweils neu.

9. **Ergebnis melden.** Nenne die Pfade von Quelldatei, SVG und PNG und in einem Satz, was
   das Diagramm zeigt. Mehr braucht es nicht.

## Änderungen an einem vorhandenen Diagramm

Wünscht der Nutzer Änderungen („mach die Pfeile beschriftet“, „füge die Tabelle Rechnung
hinzu“), bearbeite die bestehende Quelldatei und wiederhole die Schritte 6 bis 9. Die
Spezifikation des Typs gilt weiter.

## Typen

Standard ist Mermaid. ER-Diagramm, Klassendiagramm und Mindmap gibt es zusätzlich als
PlantUML-Variante; sie wird nur mit dem Zusatz `plantuml` verwendet. Die Stichwörter sind
Erkennungshilfen, keine feste Schreibweise: Bindestriche, Groß- und Kleinschreibung und
Zusätze wie „-diagramm“ spielen keine Rolle.

| Der Nutzer sagt | Mermaid (`specs/mermaid/`) | PlantUML (`specs/plantuml/`) |
| --- | --- | --- |
| er, erd, entity-relationship, datenmodell | `entityRelationshipDiagram.md` | `plantuml_er.md` |
| klasse, klassen, class | `classDiagram.md` | `plantuml_class.md` |
| mindmap | `mindmap.md` | `plantuml_mindmap.md` |
| sequenz, sequence, interaktion, nachrichten | `sequenceDiagram.md` | – |
| flowchart, fluss, ablauf, prozess | `flowchart.md` | – |
| zustand, zustands, state, zustandsautomat | `stateDiagram.md` | – |
| gantt, zeitplan, projektplan | `gantt.md` | – |
| timeline, zeitstrahl, chronologie | `timeline.md` | – |
| architektur, architecture | `architectureDiagram.md` | – |
| c4 | `c4Diagram.md` | – |
| block | `blockDiagram.md` | – |
| git, gitgraph, branches | `gitGraph.md` | – |
| kanban | `kanban.md` | – |
| journey, user-journey, nutzerreise | `userJourney.md` | – |
| requirement, anforderung | `requirementDiagram.md` | – |
| pie, torte, kreis | `pieChart.md` | – |
| xy, xychart, linie, balken | `xyChart.md` | – |
| quadrant | `quadrantChart.md` | – |
| radar, netz, spinnennetz | `radar.md` | – |
| sankey, mengenfluss | `sankeyDiagram.md` | – |
| treemap, kacheldiagramm | `treemap.md` | – |
| packet, paket, protokollkopf | `packet.md` | – |
| zenuml | `zenuml.md` | – |

## Voraussetzungen

Mermaid braucht `node` und die Mermaid-CLI `mmdc`. PlantUML braucht das Kommando `plantuml`
oder eine PlantUML-jar mit `java` (Umgebungsvariable `PLANTUML_JAR` oder eine jar im Ordner
`vendor/`), für Klassen- und ER-Diagramme außerdem Graphviz (`dot`). Meldet `render.py`,
dass ein Werkzeug fehlt, zeigt

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --check
```

was fehlt und wie es installiert wird. Installiere nichts ungefragt: Nenne dem Nutzer das
fehlende Werkzeug samt Installationsbefehl, statt ein ungeprüftes Diagramm als fertig
auszugeben.
