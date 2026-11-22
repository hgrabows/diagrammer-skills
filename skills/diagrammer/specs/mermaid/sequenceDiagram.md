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

```mermaid
sequenceDiagram
    [participant definitions]
    [messages and interactions]
```

### Participants

#### Basic Participants
```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello
```

#### Actor vs Participant
```mermaid
sequenceDiagram
    actor Alice      % Uses actor symbol
    participant Bob     % Uses rectangle symbol
```

#### Participant Types (v10.3.0+)
```mermaid
sequenceDiagram
    participant Alice@{ "type": "boundary" }     % Boundary
    participant Bob@{ "type": "control" }       % Control
    participant DB@{ "type": "database" }     % Database
    participant Queue@{ "type": "queue" }      % Queue
```

### Message Types

| Arrow Type | Syntax | Description |
|------------|---------|-----------|
| Solid Arrow | `A->B` | Standard message |
| Dotted Arrow | `A-->B` | Reply message |
| Solid with Open Arrow | `A-)B` | Asynchronous message |
| Dotted with Open Arrow | `A--)B` | Asynchronous reply |
| Bidirectional | `A<->B` | Bidirectional communication |
| Cross End | `A-xB` | Message with cross (error/cancel) |
| Circle End | `A-oB` | Message with circle end |

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

#### Notes
```mermaid
sequenceDiagram
    Note right of Alice: Important note
    Note over Alice,John: Note about both
```

#### Grouping
```mermaid
sequenceDiagram
    box Group Name
    participant Alice
    participant Bob
    end
    box Another Group
    participant Carol
    participant Dave
    end
```

## Examples

### Basic Communication

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: Great!
    Alice-)Bob: See you later!
```

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

### E-commerce Transaction Flow

```mermaid
sequenceDiagram
    participant Customer
    participant WebApp
    participant PaymentService
    participant Bank
    
    Customer->>WebApp: Browse products
    WebApp->>PaymentService: Initiate payment
    PaymentService->>Bank: Process payment
    Bank-->>PaymentService: Payment confirmation
    PaymentService-->>WebApp: Update order status
    WebApp-->>Customer: Show confirmation
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
8. **Use appropriate arrow types** - solid for requests, dotted for replies, open for async
9. **Consider time flow** - arrange messages to show clear temporal progression
10. **Keep diagrams focused** - avoid overcrowding with too many participants or messages

**References:**
- [Mermaid.js Sequence Diagram Documentation](https://mermaid.js.org/syntax/sequenceDiagram.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)