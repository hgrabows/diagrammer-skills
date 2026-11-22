# Swimlane Diagram

## Summary

A **swimlane diagram** is a process flow divided into lanes. Each lane belongs to one actor, team, system or phase; the steps inside a lane are that owner's work, and every arrow that crosses a lane border is a handoff. In Mermaid it is its own diagram type that reuses the node and edge syntax of the flowchart.

> **Note:** Swimlane diagrams are a beta feature. The keyword is `swimlane-beta`; plain `swimlane` is not recognized.

**Use Cases:**
- Approval, ordering, onboarding and support processes that involve several departments
- Showing which system performs which step of an integration
- Making handoffs and waiting points between teams visible
- Incident or escalation procedures with clear responsibilities

**When to Use:**
- The question "who does this step?" matters as much as "what comes next?"
- Use a flowchart when ownership is irrelevant, a sequence diagram when the focus is on the messages between participants over time

---

## Syntax

### Declaration and direction

```text
swimlane-beta [direction]
```

| Direction | Flow | Lanes are drawn as |
| --- | --- | --- |
| `TB` / `TD` (default) | top to bottom | columns side by side, lane name in a header on top |
| `LR` | left to right | horizontal bands stacked from top to bottom, lane name rotated at the left edge |
| `BT` | bottom to top | columns |
| `RL` | right to left | horizontal bands |

`LR` gives the classic swimlane picture and suits long processes with few lanes. `TB` suits many lanes with few steps each.

### Lanes

A lane is a top-level `subgraph ... end` block. Lanes appear in the order they are written.

```text
subgraph Sales                     %% id and label are the same
subgraph fin [Finance team]        %% id fin, label "Finance team"
subgraph "Customer Care"           %% quoted label with spaces
```

### Nodes

Declare each node inside the lane that owns it, with flowchart shape syntax:

| Syntax | Shape | Typical use |
| --- | --- | --- |
| `id[Text]` | rectangle | task |
| `id(Text)` | rounded rectangle | step, event |
| `id([Text])` | stadium | start, end |
| `id{Text}` | diamond | decision |
| `id((Text))` | circle | connector |
| `id[(Text)]` | cylinder | data store |
| `id@{ shape: doc, label: "Text" }` | named shape | document and other flowchart shapes |

Quote a label that contains brackets or other special characters: `a["Check (manual)"]`. A line break is `<br/>`; a Markdown label is written as ``id["`**bold** text`"]``.

### Edges

Write the edges after the lanes. They may connect nodes in one lane or across lanes.

| Syntax | Meaning |
| --- | --- |
| `A --> B` | arrow |
| `A -->\|Label\| B` or `A -- Label --> B` | arrow with label |
| `A -.-> B` | dotted arrow |
| `A ==> B` | thick arrow |
| `A --- B` | line without arrowhead |
| `A <--> B` | arrow on both ends |
| `A --> B --> C` | chain |
| `A & B --> C` | several sources to one target |

### Styling and comments

`classDef name fill:#...,stroke:#...`, `class nodeId name`, `nodeId:::name`, `style id ...` (works for nodes and for lane ids) and `linkStyle 0 stroke:#...` behave as in a flowchart. `%%` starts a comment line. `accTitle:` and `accDescr:` are accepted.

The default look is colourful (each lane gets its own tint). The plain look is selected in the front matter:

```text
---
config:
  theme: default
  look: classic
---
```

---

## Examples

### Minimal: two lanes, one handoff

```mermaid
swimlane-beta LR
  subgraph Customer
    order[Place order]
  end
  subgraph Shop
    ship[Ship order]
  end
  order --> ship
```

### Handoffs with labels and a decision

```mermaid
swimlane-beta LR
  subgraph Customer
    request([Open request])
    receive([Receive answer])
  end
  subgraph Support
    triage{Known issue?}
    answer[Send answer]
  end
  subgraph Engineering
    investigate[Investigate]
    fix[Prepare fix]
  end

  request --> triage
  triage -->|Yes| answer
  triage -->|No| investigate
  investigate --> fix --> answer
  answer --> receive
```

### Columns (TB) with lane ids, shapes and a rework loop

```mermaid
swimlane-beta TB
  subgraph author [Author]
    draft([Write draft])
    submit[Submit text]
    revise[Revise text]
  end
  subgraph review [Review board]
    check{Ready to publish?}
  end
  subgraph pub [Publishing]
    layout[Create layout]
    done((Done))
  end

  draft --> submit --> check
  check -->|Yes| layout --> done
  check -.->|No| revise
  revise --> submit
```

### Highlighting steps with classes

```mermaid
swimlane-beta LR
  subgraph ops [Operations]
    intake[Receive request]
    plan[Plan work]
  end
  subgraph legal [Legal]
    contract["Review contract (manual)"]:::attention
  end
  subgraph archive [Archive]
    store[(Contract store)]
  end

  intake --> plan ==> contract --> store

  classDef attention fill:#fff2cc,stroke:#d6a500,color:#111
  style plan stroke:#c00,stroke-width:3px
```

### Realistic process: leave request

```mermaid
swimlane-beta LR
  subgraph emp [Employee]
    request([Request leave])
    informed([Get decision])
  end
  subgraph mgr [Manager]
    review{Approve?}
  end
  subgraph hr [HR system]
    balance[Check leave balance]
    record[(Record absence)]
    notify[Send notification]
  end

  request --> balance
  balance -->|Enough days| review
  review -->|Yes| record
  record --> notify
  review -->|No| notify
  notify --> informed
```

---

## Rules and Pitfalls

- **Keyword is `swimlane-beta`.** `swimlane` alone gives "No diagram type detected".
- **No title.** A `title ...` line is a parse error. A front matter `title:` is accepted but is drawn on top of the first node, so leave it out and put the title into the surrounding text.
- **Every node belongs in a lane.** A node that is only mentioned in an edge (or declared outside all `subgraph` blocks) is put into an extra, unlabelled lane in front of the others. Typos in node ids show up exactly like this.
- **A node is in one lane only.** If two lanes list the same id, the first lane keeps it.
- **Lanes are one level deep.** A `subgraph` inside a lane is drawn as a thin frame without its title. Do not nest; use separate lanes or a naming prefix.
- **Empty lanes disappear.** A `subgraph` without nodes is not drawn. Give a lane at least one node if it has to be visible.
- **One edge per direction between two nodes.** A second `A --> B` is routed around the outside of the lane frame and its label is cut off. Combine the labels into one edge. An edge back (`B --> A`) is fine.
- **`end` is reserved.** `end[End]` as a node id breaks the lane block; use `done`, `finish` or `endNode`.
- **Lane ids and node ids share one namespace.** A node with the id of a lane (lane `A`, node `A[...]`) renders without an error but garbled: lanes and nodes go missing. Use distinct ids, for example short lowercase lane ids (`fin`) and verb-like node ids (`invoice`).
- **Direction changes the lane orientation, not only the flow.** With `LR` the lane names are rotated and sit at the left; long lane names are easier to read with `TB`.
- **Keep it small and look at the PNG.** The edge routing gets unreliable as the diagram grows: in tests with four lanes and nine nodes, edges between neighbouring lanes took a detour around the whole diagram, and in one case the last lane was cut off at the image border. Three lanes and up to about eight nodes rendered cleanly. Split larger processes into several diagrams.
- **Declare the nodes of a lane in process order.** The order inside the `subgraph` influences the placement; a lane that lists a late step first produced crossing edges.
- Labels with parentheses, braces or quotes need double quotes: `step["Check (manual)"]`.

---

## References

- [Official Mermaid Swimlane Diagram Documentation](https://mermaid.js.org/syntax/swimlanes.html)
- [Mermaid Flowchart Syntax (node shapes and edges)](https://mermaid.js.org/syntax/flowchart.html)
