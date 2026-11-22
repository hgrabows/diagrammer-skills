# Block Diagram

## Summary

Block diagrams are intuitive and efficient tools for visually representing complex systems, processes, or architectures. They consist of blocks (representing components or functions) and connectors (showing relationships or flows). Block diagrams provide a high-level view, making them ideal for simplifying and explaining the structure and interactions within a system.

### Use Cases

- **Software Architecture**: Illustrate application modules, services, and their interactions.
- **Network Diagrams**: Represent network devices, services, and data flow.
- **Process Flowcharts**: Visualize business or manufacturing processes.
- **Electrical Systems**: Show high-level structure and component interactions.
- **Education**: Explain complex concepts in a simplified manner.

### When to Use

- When you need a high-level overview of a system.
- When you want full control over block positioning (unlike flowcharts).
- When explaining or analyzing system structure and relationships.

## Syntax

- Start with the `block` keyword.
- Use simple labels for blocks.
- Use `columns N` to define the number of columns.
- Use connectors (`-->`, `---`, etc.) to show relationships.
- Use `block`/`end` for composite (nested) blocks.
- Use `space` to add empty space between blocks (`space:2` leaves two cells empty).
- Use `id:N` or `id["Label"]:N` to let a block span N columns.
- Comments are `%%` lines of their own.

### Basic Structure

```mermaid
block
  a b c
```

### Multi-Column Layout

```mermaid
block
  columns 3
  a b c d
```

### Block Width

```mermaid
block
  columns 3
  header["Header spans all columns"]:3
  nav["Nav"] content["Content spans two"]:2
```

### Composite Blocks

```mermaid
block
  block
    D
  end
  A["A: I am a wide one"]
```

Give a composite block an id with `block:id` (optionally `block:id:N` for its width) so that it can be styled or linked.

### Block Shapes

- Rectangle: `A`
- Rounded: `id1("Text")`
- Stadium: `id1(["Text"])`
- Subroutine: `id1[["Text"]]`
- Cylinder: `id1[("Database")]`
- Circle: `id1(("Text"))`
- Asymmetric: `id1>"Text"]`
- Rhombus: `id1{"Text"}`
- Hexagon: `id1{{"Text"}}`
- Parallelogram: `id1[/"Text"/]` (alt: `id1[\"Text"\]`)
- Trapezoid: `id1[/"Text"\]` (alt: `id1[\"Text"/]`)
- Double Circle: `id1((("Text")))`

Slanted shapes (parallelogram, trapezoid) and the double circle are drawn wider than their cell and overlap neighbours in a dense grid; put a `space` next to them. Long labels in hexagons are cut off, keep them short.

### Block Arrows and Space

```mermaid
block
  blockArrowId<["Label"]>(right)
  blockArrowId2<["Label"]>(left)
  blockArrowId3<["Label"]>(up)
  blockArrowId4<["Label"]>(down)
  space:2
```

A block arrow is `id<["Label"]>(direction)` with direction `right`, `left`, `up`, `down`, `x` or `y`. For an arrow without text use `<[" "]>`; there must be no space between the closing quote and `]` (`<[" " ]>` is a lexical error). Every arrow needs its own unique id.

### Connecting Blocks

```mermaid
block
  A space B
  A --> B
  A -- "X" --> B
```

### Styling

- Individual: `style id fill:#969,stroke:#333,stroke-width:4px`
- Class: `classDef blue fill:#6e6ce6,stroke:#333,stroke-width:4px; class A blue`

## Examples

### System Architecture

```mermaid
block
  columns 3
  Frontend toBackend<[" "]>(right) Backend
  space:2 down<[" "]>(down)
  Disk left<[" "]>(left) Database[("Database")]
  classDef front fill:#696,stroke:#333;
  classDef back fill:#969,stroke:#333;
  class Frontend front
  class Backend,Database back
```

### Business Process Flow

```mermaid
block
  columns 3
  Start(("Start")) space:2
  down1<[" "]>(down) space:2
  Decision{{"Decide"}} yes<["Yes"]>(right) Process1["Process A"]
  no<["No"]>(down) space done1<["Done"]>(down)
  Process2["Process B"] done2<["Done"]>(right) End(("End"))
  style Start fill:#969;
  style End fill:#696;
```

### Nested Services with Links

```mermaid
block
  columns 3
  client["Client"]
  block:services:2
    columns 2
    api["API"] worker["Worker"]
  end
  space:3
  db[("Database")]:3
  client --> api
  api -- "SQL" --> db
  style services fill:#eef,stroke:#669
```

## Tips

- Use columns and spaces for precise layout control.
- Use composite blocks for hierarchical systems.
- Style blocks and connectors for clarity and emphasis.
- Use comments (`%%`) for documentation within diagrams.

**References:**
- [Mermaid.js Block Diagram Documentation](https://mermaid.js.org/syntax/block.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)