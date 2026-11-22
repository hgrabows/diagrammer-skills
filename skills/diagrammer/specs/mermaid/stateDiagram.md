# State Diagram

## Summary

State diagrams are a type of diagram used in computer science and related fields to describe the behavior of systems. They require that the system described is composed of a finite number of states, and sometimes this is indeed the case, while at other times this is a reasonable abstraction. State diagrams are excellent for modeling the lifecycle of objects, systems, or processes.

### Use Cases

State diagrams are best used for:

- **System Behavior Modeling**: Showing how different components or systems transition between states
- **Object Lifecycle**: Visualizing the lifecycle of objects from creation to destruction
- **Process Flows**: Documenting state transitions in business processes
- **User Interface Design**: Modeling user interactions and screen flows
- **Protocol Design**: Illustrating communication protocols and state changes
- **Finite State Machines**: Representing systems with discrete states and transitions
- **Error Handling**: Modeling exception flows and recovery states

### When to Use

State diagrams are ideal when you need to:
- Model systems with discrete states and transitions
- Show the lifecycle of objects or processes
- Document complex behavior in a clear, visual way
- Design state machines and controllers
- Analyze system behavior and identify edge cases
- Create technical documentation for state-based systems

## Syntax

### Basic Structure

```mermaid
stateDiagram
    [*] --> InitialState
    InitialState --> NextState
    NextState --> FinalState
    FinalState --> [*]
```

### State Declaration

#### Simple State
```mermaid
stateDiagram
    StateName
```

#### State with Description
```mermaid
stateDiagram
    StateName: Description of the state
```

### Transitions

#### Basic Transition
```mermaid
stateDiagram
    FromState --> ToState
```

#### Transition with Label
```mermaid
stateDiagram
    FromState --> ToState: Transition description
```

### Start and End States

```mermaid
stateDiagram
    [*] --> StartState
    EndState --> [*]
```

### Composite States

```mermaid
stateDiagram
    state CompositeState {
        [*] --> SubState1
        SubState1 --> [*]
        [*] --> SubState2
        SubState2 --> [*]
    }
```

### Choice States

```mermaid
stateDiagram
    state ChoiceState <<choice>>
    [*] --> Check
    Check --> ChoiceState
    ChoiceState --> Option1 : condition A
    ChoiceState --> Option2 : condition B
    Option1 --> [*]
    Option2 --> [*]
```

Declare the choice state once with `<<choice>>`, then use it like any other state as the
source of the alternative transitions. There is no `end` keyword in state diagrams.

### Fork and Join

```mermaid
stateDiagram
    state ForkState <<fork>>
    state JoinState <<join>>
    [*] --> ForkState
    ForkState --> State1
    ForkState --> State2
    State1 --> JoinState
    State2 --> JoinState
    JoinState --> State3
    State3 --> [*]
```

Declare fork and join states on their own lines before using them in transitions.

### Notes

```mermaid
stateDiagram
    State1
    note right of State1: Important note about this state
    State1 --> State2
    note left of State2: Note on the left
```

### Concurrency

```mermaid
stateDiagram
    [*] --> ActiveState
    state ActiveState {
        [*] --> NumLockOff
        NumLockOff --> NumLockOn : EvNumLockPressed
        NumLockOn --> NumLockOff : EvNumLockPressed
        --
        [*] --> CapsLockOff
        CapsLockOff --> CapsLockOn : EvCapsLockPressed
        CapsLockOn --> CapsLockOff : EvCapsLockPressed
        --
        [*] --> ScrollLockOff
        ScrollLockOff --> ScrollLockOn : EvScrollLockPressed
        ScrollLockOn --> ScrollLockOff : EvScrollLockPressed
    }
```

## Examples

### Simple State Machine

```mermaid
stateDiagram
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```

### E-commerce Order State

```mermaid
stateDiagram
    [*] --> Browsing
    Browsing --> AddingToCart
    AddingToCart --> Checkout
    Checkout --> Payment
    Payment --> Processing
    Processing --> Shipped
    Shipped --> Delivered
    Delivered --> [*]
```

### User Authentication Flow

```mermaid
stateDiagram
    [*] --> LoggedOut
    LoggedOut --> LoggingIn
    LoggingIn --> ViewingProfile
    ViewingProfile --> EditingProfile
    EditingProfile --> ViewingProfile
    ViewingProfile --> [*]
    LoggedOut --> [*]
```

### Composite State Example

```mermaid
stateDiagram
    state Active {
        [*] --> Idle
        Idle --> Processing
        Processing --> Complete
        Complete --> Idle
    }
    Idle --> [*]
```

### Choice with Multiple Options

```mermaid
stateDiagram
    state StockDecision <<choice>>
    [*] --> CheckInventory
    CheckInventory --> StockDecision
    StockDecision --> ProcessOrder : in stock
    StockDecision --> NotifyCustomer : out of stock
    ProcessOrder --> [*]
    NotifyCustomer --> [*]
```

### Concurrent States

```mermaid
stateDiagram
    [*] --> Active
    state Active {
        [*] --> NumLockOff
        NumLockOff --> NumLockOn : EvNumLockPressed
        NumLockOn --> NumLockOff : EvNumLockPressed
        --
        [*] --> CapsLockOff
        CapsLockOff --> CapsLockOn : EvCapsLockPressed
        CapsLockOn --> CapsLockOff : EvCapsLockPressed
        --
        [*] --> ScrollLockOff
        ScrollLockOff --> ScrollLockOn : EvScrollLockPressed
        ScrollLockOn --> ScrollLockOff : EvScrollLockPressed
    }
```

## Tips and Best Practices

1. **Use meaningful state names** that clearly describe the system's condition
2. **Keep diagrams simple** - avoid overcrowding with too many states
3. **Group related states** using composite states for better organization
4. **Use appropriate transitions** - show clear state changes
5. **Document entry and exit points** - clearly mark start and end states
6. **Use choice states** for decision points and conditional logic
7. **Employ fork/join** for parallel processing paths
8. **Add notes** to explain complex transitions or state meanings
9. **Consider state hierarchy** - organize states in logical groups
10. **Use consistent naming** - follow established conventions for state names

**References:**
- [Mermaid.js State Diagram Documentation](https://mermaid.js.org/syntax/stateDiagram.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)