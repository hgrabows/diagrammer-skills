# Agent Flow Diagram

## Summary

An **agent flow diagram** (`agentflow-beta`) describes a system built from LLM agents: which agent does which task, which tools and documents it uses, where decisions are made and how work is handed from one agent to the next. It reads like a flowchart, but the node shapes and the three arrow types have fixed meanings. The diagram type is in beta.

**Use Cases:**
- Documenting a multi-agent pipeline (researcher, writer, reviewer)
- Showing which tools, APIs and reference documents an agent has
- Explaining success and failure paths of an agent loop
- Giving an overview of a large system with some agents collapsed

**When to Use:**
- When the diagram is about agents, tools and hand-offs.
- For ordinary process logic without agents a flowchart has more shapes and arrow types.

---

## Syntax Description

- First line: `agentflow-beta` followed by a direction: `TB` (same as `TD`), `BT`, `LR` or `RL`. Without a direction the diagram runs top to bottom.
- Comments start with `%%`. Indentation is free; indent the content of containers for readability.
- A title is set in the front matter (`title: ...`), see the last example.

**Nodes:**
```text
id["Label"]@{ shape: task }
```
- `id`: letters, digits, `_` and `-`. The label goes in square brackets, best in double quotes. `<br/>` breaks a line; long labels wrap by themselves.
- A node without `shape` is drawn like a task.

| `shape` | Meaning | Drawn as |
| --- | --- | --- |
| `task` | Work an agent performs | rounded rectangle |
| `tool` | Callable function or API | rectangle with double side bars |
| `input` | Data entering the flow | parallelogram |
| `decision` | Branch point | diamond |
| `refdoc` | Reference material | document with a wavy bottom edge |
| `action` | Step with a side effect (send, write, publish) | hexagon |

**Edges** (only these three operators exist):

| Operator | Meaning | Drawn as |
| --- | --- | --- |
| `A --> B` | Sequence: control or data moves on | solid line with arrowhead |
| `A -.- B` | Reference: A consults B | dotted line without arrowhead |
| `A --x B` | Failure path out of A | solid line ending in a cross |

- Labels: `A -- text --> B`, `A -- text --x B`, or with pipes `A -->|text| B`, `A -.-|text| B`.
- Chains (`a --> b --> c`) and groups (`a & b --> c`) work as in flowcharts.

**Containers** (agents, teams, stages):
```text
flow id["Title"]
  ...nodes, edges, nested flows...
end
```
- Containers nest to any depth. A node belongs to the container in which it is declared or mentioned.
- An edge may start or end at a container id (`researcher --> writer`).
- `global ... end` (no id, no title) declares nodes that stay outside all containers even though several containers refer to them.
- `id@{ view: "collapsed" }` on a separate line after the container shrinks it to a single box with three dots; edges to its inner nodes then end at that box.

**Connectors:** `connector id["Title"]` declares an external system. It is drawn as its own rounded box, not connected to anything unless you add an edge.

**Metadata:** any node, container or connector can carry more keys in `@{ ... }`, on the node itself or on a separate line (`id@{ key: "value" }`). Usual keys: `model`, `instruction`, `description`, `params`, `returns`, `value`, `example`, `connectorRef`, and for connectors `protocol`, `endpoint`. Only `shape`, `label` and `view` change the picture; everything else is kept in the source for readers and tools and is **not drawn**.

**Styling:** `classDef name fill:#fde,stroke:#933`, `class id name`, `id:::name` and `style id fill:#9f9` work as in flowcharts.

---

## Examples

### Minimal

```mermaid
agentflow-beta LR
  question["User question"]@{ shape: input }
  answer["Write answer"]@{ shape: task }
  question --> answer
```

### All Shapes

```mermaid
agentflow-beta LR
  brief["Brief"]@{ shape: input }
  draft["Draft copy"]@{ shape: task }
  spell["spell_check"]@{ shape: tool }
  guide["Style guide"]@{ shape: refdoc }
  ok["Good enough?"]@{ shape: decision }
  publish["Publish"]@{ shape: action }

  brief --> draft --> spell --> ok --> publish
  draft -.- guide
```

### Edge Types and Labels

```mermaid
agentflow-beta TB
  run["Run test suite"]@{ shape: tool }
  check["All green?"]@{ shape: decision }
  merge["Merge branch"]@{ shape: action }
  fix["Fix the code"]@{ shape: task }
  logs["Test logs"]@{ shape: refdoc }
  alert["Notify developer"]@{ shape: action }

  run --> check
  check -- yes --> merge
  check -- no --> fix
  fix -.-|reads| logs
  run -- timeout --x alert
```

### Nested Containers

```mermaid
agentflow-beta TB
  flow team["Content Team"]
    flow researcher["Researcher"]
      gather["Gather sources"]@{ shape: task }
      search["web_search"]@{ shape: tool }
      gather --> search
    end

    flow writer["Writer"]
      compose["Compose draft"]@{ shape: task }
    end

    researcher --> writer
  end
```

### Shared Nodes with `global`

```mermaid
agentflow-beta TB
  global
    corpus["Shared corpus"]@{ shape: refdoc }
  end

  flow summariser["Summariser"]
    summarise["Summarise"]@{ shape: task }
    summarise -.- corpus
  end

  flow indexer["Indexer"]
    index["Build index"]@{ shape: task }
    index -.- corpus
  end
```

### Collapsed Container

```mermaid
agentflow-beta LR
  flow intake["Intake"]
    receive["Receive request"]@{ shape: input }
  end

  flow processing["Processing"]
    validate["Validate"]@{ shape: task }
    enrich["Enrich"]@{ shape: task }
    validate --> enrich
  end
  processing@{ view: "collapsed" }

  flow output["Output"]
    publish["Publish"]@{ shape: action }
  end

  receive --> validate
  enrich --> publish
```

### Realistic: Support Ticket Pipeline

Front matter title, connector, metadata (not drawn), all three edge types and a styled node.

```mermaid
---
title: Support Ticket Pipeline
---
agentflow-beta LR
  connector helpdesk["Helpdesk API"]
  helpdesk@{ protocol: "http", endpoint: "https://helpdesk.example.com/api" }

  global
    kb["Knowledge base"]@{ shape: refdoc }
  end

  ticket["New ticket"]@{ shape: input, example: "Cannot log in" }

  flow triage["Triage Agent"]
    classify["Classify ticket"]@{ shape: task }
    urgent["Urgent?"]@{ shape: decision }
    classify --> urgent
  end
  triage@{ model: "small-fast-model", instruction: "Label the ticket and judge urgency." }

  flow resolver["Resolver Agent"]
    lookup["search_kb"]@{ shape: tool, params: "query :: String", returns: "Articles" }
    draft["Draft reply"]@{ shape: task }
    lookup --> draft
    lookup -.- kb
  end

  send["Send reply"]@{ shape: action, connectorRef: "helpdesk.reply" }
  human["Escalate to human"]@{ shape: action }

  ticket --> classify
  urgent -- no --> lookup
  urgent -- yes --> human
  draft --> send
  draft -- no article found --x human
  send --> helpdesk

  classDef warn fill:#ffe3e3,stroke:#c92a2a
  class human warn
```

---

## Rules and Pitfalls

- **Only three edge operators.** Flowchart arrows such as `-.->`, `==>`, `---`, `--o` and `<-->` are syntax errors. A dotted reference has no arrowhead; if you need a direction, use `-->` with a label.
- **Label on a dotted edge only with pipes:** `a -.-|reads| b` works, `a -. reads .- b` is a syntax error.
- **Reserved ids:** `flow`, `end`, `global` and `connector` cannot be node ids (`end["End"]` fails). Use `finish`, `done` or similar. As label text they are fine.
- **`subgraph` does not exist here**, containers are written with `flow ... end`.
- **Use only the six shape names from the table.** An unknown name stops rendering with `No such shape`. Flowchart shape names such as `cyl`, `doc`, `stadium`, `circle` or `rect` are accepted but all come out as the plain rounded rectangle, so a database cannot be shown as a cylinder.
- **Metadata is invisible.** `model`, `instruction`, `params`, `returns`, `connectorRef` and so on do not appear in the picture, and `connectorRef` draws no line to the connector. Whatever the reader must see belongs in a label or needs its own edge.
- **Container title:** write `flow id["Title"]`. `flow "Title"` renders a container without any title.
- **Edges into a container in `TB` layout** enter from above and run through the container title. When nodes in different containers are linked directly, prefer `LR`, or link the containers themselves (`researcher --> writer`).
- **Mentioning a node inside a container pulls it into that container**, even if it was declared at the top level before. Write edges between containers outside of both, and put nodes that several containers refer to into `global`.
- The default look is colourful (each shape and each container gets its own colour) and the layout engine is ELK. This is fine as it is; no front matter is needed for it.

---

## References

- [Official Mermaid Agentflow Documentation](https://mermaid.js.org/syntax/agentflow.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)
