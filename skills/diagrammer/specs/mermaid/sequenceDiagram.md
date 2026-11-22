# Sequence Diagram

## Summary

Sequence diagrams are interaction diagrams that show how processes operate with one another and in what order. They are particularly useful for visualizing the chronological flow of messages between different components, actors, or systems in a time-ordered sequence.

### Use Cases

Sequence diagrams are best used for:

- **System Interactions**: Showing how different components or services communicate with each other
- **API Documentation**: Documenting the sequence of API calls between client and server
- **Use Case Modeling**: Visualizing user interactions with a system step by step
- **Protocol Design**: Illustrating communication protocols and message exchanges
- **Object-Oriented Design**: Showing method calls and object interactions in software
- **Business Process Flows**: Mapping out business transactions and handoffs between departments
- **Troubleshooting**: Analyzing communication patterns to identify issues

### When to Use

Sequence diagrams are ideal when you need to:
- Show the order of operations or events over time
- Document communication between multiple actors or systems
- Model complex interactions with clear temporal relationships
- Design and understand system architectures
- Create technical documentation for developers
- Analyze existing systems for improvement opportunities

## Syntax

### Basic Structure

Template (placeholders, not runnable):

```text
sequenceDiagram
    <participant definitions>
    <messages and interactions>
```

Minimal complete diagram:

```mermaid
sequenceDiagram
    participant A as Client
    participant B as Server
    A->>B: Request
    B-->>A: Response
```

Comments start with `%%` and must stand on a line of their own. Text after a statement, such as `actor Alice % note`, is not a comment: it becomes part of the participant name or message.

### Participants

#### Basic Participants
```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello
```

#### Actor vs Participant
`actor` draws a stick figure, `participant` a box. `as` gives a display name that differs from the id.

```mermaid
sequenceDiagram
    actor Alice
    participant Bob
    participant API as Public API
    Alice->>Bob: Hello
    Bob->>API: Forward
```

#### Participant Types
The JSON-style suffix `@{ "type": "..." }` selects a symbol: `boundary`, `control`, `entity`, `database`, `collections` or `queue`.

```mermaid
sequenceDiagram
    participant UI@{ "type": "boundary" }
    participant Ctl@{ "type": "control" }
    participant Ent@{ "type": "entity" }
    participant DB@{ "type": "database" }
    participant Coll@{ "type": "collections" }
    participant Q@{ "type": "queue" }
    UI->>Ctl: Submit
    Ctl->>Ent: Update
    Ent->>DB: Save
    Ctl->>Coll: Index
    Ctl-)Q: Publish event
```

#### Creating and Destroying Participants
`create participant X` (or `create actor X`) directly before a message makes X appear at that message instead of at the top; X must be the receiver. `destroy X` directly before a message ends X's lifeline at that message; X can be sender or receiver.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Start job
    create participant Worker
    Server->>Worker: Spawn
    Worker-->>Server: Result
    destroy Worker
    Server-xWorker: Terminate
    Server-->>Client: Job finished
```

### Message Types

| Arrow Type | Syntax | Description |
|------------|---------|-----------|
| Solid line, no arrowhead | `A->B` | Plain connection |
| Dotted line, no arrowhead | `A-->B` | Plain dotted connection |
| Solid with arrowhead | `A->>B` | Standard message / call |
| Dotted with arrowhead | `A-->>B` | Reply message |
| Solid, arrowheads on both ends | `A<<->>B` | Bidirectional communication |
| Dotted, arrowheads on both ends | `A<<-->>B` | Bidirectional, dotted |
| Solid with cross | `A-xB` | Lost or cancelled message |
| Dotted with cross | `A--xB` | Lost or cancelled reply |
| Solid with open arrow | `A-)B` | Asynchronous message |
| Dotted with open arrow | `A--)B` | Asynchronous reply |

`->` and `-->` have **no** arrowhead; use `->>` and `-->>` for normal messages. `A<->B` and `A-oB` do not exist and are parse errors.

```mermaid
sequenceDiagram
    participant A
    participant B
    A->B: Solid line, no arrowhead
    A-->B: Dotted line, no arrowhead
    A->>B: Solid line with arrowhead
    B-->>A: Dotted line with arrowhead
    A<<->>B: Solid, arrowheads on both ends
    A<<-->>B: Dotted, arrowheads on both ends
    A-xB: Solid line with cross
    A--xB: Dotted line with cross
    A-)B: Solid line with open arrow
    A--)B: Dotted line with open arrow
```

Message text ends at the line end. A semicolon in the text is a parse error, write `#59;` instead; `<br/>` breaks a line.

### Control Structures

#### Loops
```mermaid
sequenceDiagram
    loop Loop condition
        A->>B: Repeated message
    end
```

#### Alternative Paths
```mermaid
sequenceDiagram
    alt Condition A
        A->>B: Path A
    else Condition B
        A->>C: Path B
    end
```

#### Optional Paths
```mermaid
sequenceDiagram
    opt Optional condition
        A->>B: Optional message
    end
```

#### Parallel Actions
```mermaid
sequenceDiagram
    par Action 1
        A->>B: Parallel message 1
    and Action 2
        A->>C: Parallel message 2
    end
```

#### Critical Regions
```mermaid
sequenceDiagram
    critical Essential operation
        A->>B: Critical message
    option Normal operation
        A->>C: Normal message
    end
```

#### Break Points
```mermaid
sequenceDiagram
    A->>B: Normal flow
    break Error occurred
        A->>C: Error handling
    end
```

### Advanced Features

#### Activations
```mermaid
sequenceDiagram
    Alice->>John: Hello
    activate John
    John-->>Alice: Response
    deactivate John
```

Shorthand: a `+` after the arrow activates the receiver, a `-` deactivates the sender (`App->>+API: call`, `API-->>-App: result`).

#### Sequence Numbers
`autonumber` as the first statement numbers all messages in order.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App
    participant API
    User->>App: Click "Save"
    App->>+API: PUT /profile
    API-->>-App: 200 OK
    App-->>User: Show confirmation
```

#### Notes
`Note right of X`, `Note left of X` or `Note over X,Y`. `rect rgb(r, g, b) ... end` puts a coloured background behind a group of messages.

```mermaid
sequenceDiagram
    participant Alice
    participant John
    Alice->>John: Hello
    Note right of John: Important note
    Note over Alice,John: Note about both
    rect rgb(230, 245, 255)
        John-->>Alice: Hi<br/>second line
    end
```

#### Grouping
`box <colour> <title> ... end` frames participants; the colour is optional and comes before the title.

```mermaid
sequenceDiagram
    box LightBlue Frontend
    participant Alice
    participant Bob
    end
    box Backend Team
    participant Carol
    participant Dave
    end
    Alice->>Carol: Request
    Carol->>Dave: Delegate
```

## Examples

### System Interaction with Database

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB@{ "type": "database" }
    
    User->>API: Request data
    API->>DB: Query database
    DB-->>API: Return results
    API-->>User: Display data
```

### Error Handling with Critical Region

```mermaid
sequenceDiagram
    critical Database connection
        Service->>DB: Connect
    option Network timeout
        Service->>API: Log error
    option Authentication failed
        Service->>API: Log different error
    end
```

### Parallel Processing Example

```mermaid
sequenceDiagram
    par User authentication
        User->>AuthService: Login
        AuthService-->>User: Return token
    and Data loading
        User->>DataService: Request data
        DataService-->>User: Return data
    end
```

## Tips and Best Practices

1. **Use meaningful participant names** that clearly identify systems or actors
2. **Order participants logically** - place most active participants on the left
3. **Use consistent message naming** - make message purposes clear
4. **Group related interactions** using boxes to organize complex diagrams
5. **Use activations** to show when components are active
6. **Employ alt/opt/par blocks** for conditional, optional, and parallel flows
7. **Add notes** to explain complex interactions or decisions
8. **Use appropriate arrow types** - `->>` for requests, `-->>` for replies, `-)` for async
9. **Consider time flow** - arrange messages to show clear temporal progression
10. **Keep diagrams focused** - avoid overcrowding with too many participants or messages

**References:**
- [Mermaid.js Sequence Diagram Documentation](https://mermaid.js.org/syntax/sequenceDiagram.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)