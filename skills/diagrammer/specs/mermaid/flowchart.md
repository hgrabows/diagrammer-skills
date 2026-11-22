# Flowchart

## Summary

Flowcharts are composed of **nodes** (geometric shapes) and **edges** (arrows or lines). They are one of the most fundamental and widely-used diagram types for visualizing processes, workflows, and decision paths.

### Use Cases

Flowcharts are best used for:

- **Process Visualization**: Mapping out step-by-step processes and workflows
- **Decision Making**: Showing conditional logic and decision points with multiple outcomes
- **System Design**: Illustrating system architectures and component interactions
- **Algorithm Representation**: Visualizing algorithmic flow and logic
- **Business Processes**: Documenting business workflows and procedures
- **Troubleshooting Guides**: Creating step-by-step problem-solving flows
- **Educational Materials**: Teaching concepts through visual process representation

### When to Use

Flowcharts are ideal when you need to:
- Show sequential steps in a process
- Represent decision points with multiple branches
- Communicate complex processes to non-technical audiences
- Document existing workflows for analysis or improvement
- Create visual documentation for procedures

## Syntax

### Basic Structure

Template (placeholders, not runnable):

```text
flowchart <direction>
    <node definitions>
    <connections>
```

Minimal complete diagram:

```mermaid
flowchart LR
    A[Start] --> B[Finish]
```

Comments start with `%%` and must stand on a line of their own. A comment after a statement on the same line (`A --> B %% note`, or with a single `%`) is a parse error.

### Direction Declaration

- `TB` - Top to bottom (default)
- `TD` - Top-down (same as top to bottom)
- `BT` - Bottom to top
- `RL` - Right to left
- `LR` - Left to right

### Node Syntax

#### Basic Node
```mermaid
flowchart LR
    id
```

#### Node with Text
```mermaid
flowchart LR
    id1[This is text in the box]
```

#### Node Shapes (Traditional Syntax)

| Shape | Syntax | Example |
|--------|---------|---------|
| Rectangle | `id[text]` | `A[Process]` |
| Rounded Rectangle | `id(text)` | `A(Start)` |
| Stadium | `id([text])` | `A([Terminal])` |
| Subroutine | `id[[text]]` | `A[[Subroutine]]` |
| Cylinder | `id[(text)]` | `A[(Database)]` |
| Circle | `id((text))` | `A((Loop))` |
| Asymmetric | `id>text]` | `A>Input]` |
| Diamond | `id{text}` | `A{Decision}` |
| Hexagon | `id{{text}}` | `A{{Prepare}}` |
| Parallelogram | `id[/text/]` | `A[/Data/]` |
| Parallelogram (alt) | `id[\text\]` | `A[\Data\]` |
| Trapezoid | `id[/text\]` | `A[/Operation\]` |
| Trapezoid (alt) | `id[\text/]` | `A[\Manual/]` |
| Double Circle | `id(((text)))` | `A(((Stop)))` |

Put the label in double quotes whenever it contains anything other than letters, digits and spaces: `A["Dashboard (logged in)"]`.

#### Node Shapes (New Syntax v11.3.0+)

`id@{ shape: <name>, label: "<text>" }` selects a shape by name. Edges are written separately and refer to the id.

```mermaid
flowchart LR
    A@{ shape: stadium, label: "Start" }
    B@{ shape: doc, label: "Read report" }
    C@{ shape: diamond, label: "Valid?" }
    D@{ shape: cyl, label: "Store" }
    E@{ shape: manual-input, label: "Fix by hand" }
    F@{ shape: docs, label: "Archive copies" }
    G@{ shape: dbl-circ, label: "End" }
    A --> B --> C
    C -->|Yes| D --> F --> G
    C -->|No| E --> B
```

Shape names verified with this renderer: `rect`, `rounded`, `stadium`, `subproc`, `cyl`, `circle`, `dbl-circ`, `diamond`, `hex`, `lean-r`, `lean-l`, `trap-b`, `trap-t`, `odd`, `doc`, `docs`, `procs`, `manual-input`, `manual-file`, `paper-tape`, `delay`, `das`, `lin-cyl`, `datastore`, `notch-rect`, `text`, `braces`. The shapes `fork`, `hourglass`, `sm-circ`, `framed-circle` and `bolt` are drawn without their label.

### Connection Syntax

#### Basic Connections
```mermaid
flowchart LR
    %% Arrow
    A --> B
    %% Open line
    B --- C
    %% Arrow with text, two spellings
    C -- text --> D
    D -->|text| E
    %% Line with text
    E ---|text| F
```

#### Advanced Connections
```mermaid
flowchart LR
    %% Thick arrow
    A ==> B
    %% Dotted arrow
    B -.-> C
    %% Thick arrow with text
    C == text ==> D
    %% Dotted arrow with text
    D -. text .-> E
    %% Extra dashes make a link span more ranks
    A ---> E
```

#### Special Connections
```mermaid
flowchart LR
    %% Circle end
    A --o B
    %% Cross end
    B --x C
    %% Arrowheads on both ends
    C <--> D
    %% Chain and fan-out in one line
    D --> E & F --> G
```

Keep a space between the link and a node id that starts with `o` or `x`: `A---oB` is read as a circle edge, not as a link to `oB`.

### Subgraphs

A subgraph that is the source or target of an edge needs an id. Write `subgraph <id> [<Title>]` and use the id in edges; a title with spaces cannot be used as an edge endpoint.

```mermaid
flowchart TB
    subgraph sg1 [Subgraph Title]
        A --> B
    end
    C --> sg1
```

`direction TB|LR|...` as the first line inside a subgraph sets its own layout direction. The word `end` in lower case is reserved; do not use it as a node id.

### Styling Links

Links have no ids. `linkStyle` addresses them by the order in which they are defined, starting at 0; several numbers can be separated by commas, and `default` applies to all links.

```mermaid
flowchart LR
    A[Order] --> B{In stock?}
    B -->|Yes| C[Ship]
    B -->|No| D[Backorder]
    D --> B
    linkStyle 2 stroke:#d33,stroke-width:3px,color:#d33
    linkStyle 3 stroke:#d33,stroke-dasharray:5 5
    linkStyle default stroke:#555
```

Here link 2 (`B -->|No| D`) is drawn thick and red with a red label, link 3 (`D --> B`) dashed red, and the other links grey.

## Examples

### Simple Process Flow

```mermaid
flowchart TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Troubleshoot]
    D --> B
```

### Complex Workflow with Subgraphs

```mermaid
flowchart LR
    subgraph input [Input Phase]
        A[User Input] --> B[Validation]
    end

    subgraph processing [Processing Phase]
        C[Process Data] --> D[Transform]
    end

    subgraph output [Output Phase]
        E[Generate Report] --> F[Display Results]
    end

    input --> processing
    processing --> output
```

### Decision Tree with Multiple Outcomes

```mermaid
flowchart TD
    A[Start] --> B{Type of Request}
    B -->|API| C[Call Service]
    B -->|Database| D[Query Database]
    B -->|File| E[Read File]
    C --> F[Process Response]
    D --> G[Format Results]
    E --> H[Parse Content]
    F --> I[Display Output]
    G --> I
    H --> I
```

### Styling Example

```mermaid
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    
    classDef start fill:#90EE90,stroke:#333,stroke-width:2px
    classDef decision fill:#F9E79F,stroke:#333,stroke-width:2px
    classDef process fill:#E1F5FE,stroke:#333,stroke-width:2px
    
    class A start
    class B decision
    class C,D process
```

### Interactive Flowchart with Click Events

Links only work in the SVG; the PNG is a static picture.

```mermaid
flowchart LR
    A[Docs] --> B[Repo]
    click A "https://example.com" "Open documentation"
    click B href "https://example.com/repo" "Open repository" _blank
```



### Project-specific validator constraints

In this project, diagrams are validated via `mmdc` using a strict Mermaid parser.
To avoid parse errors, please follow these additional constraints when using the classic `id[text]` syntax:

- Unquoted labels must not contain parentheses `(` `)` or the pipe character `|`: `D[Dashboard (logged in)]` and `D[Dashboard | admin]` are parse errors.
- Quote such labels instead: `D["Dashboard (logged in) | admin"]`. Inside a quoted label write a double quote as `#quot;`.
- The new syntax `id@{ shape: ..., label: "..." }` always takes a quoted label and has the same effect.
- Comments are `%%` lines of their own, never trailing text after a statement.
- Subgraphs used in edges need an id: `subgraph id [Title]`.


## Tips and Best Practices

1. **Use meaningful node IDs** that describe the function of each step
2. **Keep flowcharts simple** - avoid overcrowding with too many nodes
3. **Use consistent direction** throughout your diagram
4. **Group related processes** using subgraphs for better organization
5. **Add descriptive text** to connections to clarify relationships
6. **Use appropriate shapes** for different types of operations (diamonds for decisions, cylinders for data, etc.)
7. **Consider color coding** different types of operations or process phases

**References:**
- [Mermaid.js Flowchart Documentation](https://mermaid.js.org/syntax/flowchart.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)