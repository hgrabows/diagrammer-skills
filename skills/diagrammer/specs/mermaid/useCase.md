# Use Case Diagram

## Summary

A **UML use case diagram** shows what a system offers to the outside world: actors (people or external systems), the use cases they take part in, the system boundary around the use cases, and the relationships include, extend and generalization.

> **Note:** Use case diagrams are a beta feature. The keyword is the single token `usecase-beta`; `usecase` and `usecaseDiagram` are not recognized.

**Use Cases:**
- Scoping a system: what is inside, who uses it
- Collecting functional requirements per user role
- Giving stakeholders an overview before details are specified
- Showing shared behaviour (include) and optional behaviour (extend)

**When to Use:**
- The focus is on goals of actors, not on the order of steps
- Use a sequence diagram or flowchart for the flow inside a single use case

---

## Syntax

### Declaration and direction

```text
usecase-beta
direction LR
```

`direction` is a statement on its own line and takes `LR`, `RL`, `TB`, `TD` or `BT`. `LR` (actors left, system right) is the conventional layout. One statement per line; there is no statement separator.

### Actors

```text
actor Customer                          %% id is also the label
actor Admin("Main administrator")       %% id plus label
actor Clerk, Auditor                    %% several at once
actor Bot("Import job")@{ type: awesome }
```

Actor ids and use case ids consist of letters, digits and `_`. Actors must be declared with `actor`; an undeclared name in a relationship always becomes a use case. Metadata keys: `type: hollow` or `type: awesome` (alternative figures), `business: true` (business actor with a slash).

### Use cases

```text
Login("Sign in")            %% ellipse with label
Report[Generate report]     %% rectangle
Checkout                    %% ellipse, id is the label
"Reset password"            %% quoted label, id becomes Reset_password
```

A stereotype is added with `<<Text>>` after the element: `Checkout("Checkout") <<Core>>`. Order of suffixes: label, `@{ ... }`, `<<...>>`, `:::class`.

### System boundary

```text
systemBoundary Shop
  Browse("Browse catalogue")
end
systemBoundary pay["Payment service"]@{ type: package }
  Authorize("Authorize payment")
end
```

Only declarations go inside the block. `type: package` draws a folder tab with the title instead of a plain rectangle.

### Relationships

| Syntax | Meaning |
| --- | --- |
| `A --> B` | association with arrowhead |
| `A -- B` | association without arrowhead |
| `A -- "label" --> B` | labelled association (unquoted text works too) |
| `A <-- B`, `A --o B`, `A o-- B`, `A --x B`, `A x-- B` | reversed, circle and cross ends |
| `Base ..> : include Part` | Base includes Part, drawn dashed with `«include»` |
| `Extra ..> : extend Base` | Extra extends Base, drawn dashed with `«extend»` |
| `Special --\|> General` | generalization (hollow triangle), actor to actor or use case to use case |

Use cases may be declared inline in a relationship: `Customer --> Pay("Pay order")`.

### Notes, labels, styling

- `note for Checkout "Text"` attaches a yellow note to one actor or use case.
- Labels: unquoted inside `( )` or `[ ]`, quoted `"..."`, or Markdown ``"`**bold** text`"``. A Markdown string may contain a real line break.
- `classDef name stroke:#c33,stroke-width:3px`, `class A,B name`, `A:::name`, `style A stroke:#06c`. Declarations are comma-separated, without semicolons. Classes show clearly on use cases and boundaries; on an actor figure a stroke class had no visible effect in tests.
- An edge gets an id by writing `id@` before the operator (`Customer pay@--> Checkout`) and can then be styled with `style pay ...`.
- `%%` starts a comment line. `accTitle:` and `accDescr:` are accepted.

---

## Examples

### Minimal

```mermaid
usecase-beta
direction LR
actor Customer
systemBoundary "Order system"
  Checkout("Place order")
end
Customer --> Checkout
```

### Two actors, two boundaries, include and extend

```mermaid
usecase-beta
direction LR
actor Customer
actor Support("Support agent")
systemBoundary Storefront
  Browse("Browse catalogue")
  Checkout("Checkout")
  Coupon("Apply coupon")
end
systemBoundary Fulfilment
  Track("Track delivery")
end
Customer --> Browse
Customer --> Checkout
Customer --> Track
Support --> Track
Checkout ..> : include Browse
Coupon ..> : extend Checkout
```

### Generalization, actor variants and stereotypes

```mermaid
usecase-beta
direction LR
actor User
actor Admin("Administrator") <<Internal>>
actor Clerk("Sales clerk")@{ business: true }
actor Job("Nightly job")@{ type: awesome }
Admin --|> User
Login("Sign in")
Manage("Manage accounts") <<Core>>
Export[Export report]
User --> Login
Admin --> Manage
Clerk --> Export
Job --> Export
```

### Notes, edge labels and multi-line labels

```mermaid
usecase-beta
direction LR
actor Member
Borrow("Borrow book")
Renew("`Renew loan
**once** per item`")
Refund("Refund #40;partial#41;")
Member -- "at the desk" --> Borrow
Member -- online --> Renew
Member --> Refund
note for Borrow "Requires a valid card"
```

### Realistic system: online ordering

```mermaid
usecase-beta
direction LR
actor Customer
actor Staff("Order staff")@{ type: hollow } <<Employee>>
actor Gateway("Payment gateway")
systemBoundary ordering["Ordering system"]@{ type: package }:::system
  Browse("Browse products")
  Checkout("Checkout") <<Core>>:::critical
  Payment("Process payment")
  Gift("Add gift wrapping")
  Review[Review order]
end
note for Checkout "`Validates the **cart** first`"
Customer --> Browse
Customer -- "places order" --> Checkout
Checkout pays@..> : include Payment
Gift ..> : extend Checkout
Staff --> Review
Payment -- Gateway
classDef system stroke:#c8a02a,stroke-width:2px
classDef critical stroke:#c33,stroke-width:3px
style pays stroke:#6b46c1,stroke-width:2px
```

---

## Rules and Pitfalls

- **Include and extend have their own form:** `A ..> : include B`. All the familiar variants fail: `A ..> B`, `A ..> B : <<include>>`, `A .-> B`. A solid association labelled "include" stays an ordinary association.
- **Include and extend connect use cases only**, generalization connects two actors or two use cases. `Actor ..> : include UseCase` is rejected ("include relationship requires use-case endpoints").
- **No flowchart or class diagram labels.** `A -->|uses| B` and `A --> B : uses` are parse errors. Write `A -- uses --> B` or `A -- "uses" --> B`.
- **Declare every actor.** Without `actor X`, the name `X` in a relationship becomes an ellipse.
- **Relationships go outside the boundary.** A `-->` line inside `systemBoundary ... end` is a parse error; so are notes, styles and nested boundaries. A boundary cannot be the end of a relationship either.
- **One statement per line, no semicolons.** `actor A; A --> B` and a trailing `;` both fail.
- **Ids are `[A-Za-z0-9_]+`.** `my-actor` fails; use `my_actor` and put the readable text into the label. `end` cannot be an id. PlantUML aliases (`actor A as Alice`) fail; write `actor A("Alice")`.
- **Parentheses in an unquoted label fail.** `R(Refund (partial))` breaks; use the entity codes `#40;` and `#41;` inside a quoted label, as in the example above. `\n` is shown literally; for a line break use a Markdown string with a real newline. Colon, comma, percent sign and umlauts are fine in unquoted labels.
- **No title.** A `title` line is a parse error and a front matter `title:` is not drawn. Use the boundary title to name the system.
- **Icon actors do not work with the CLI.** `@{ icon: "fa:user" }` renders a question-mark placeholder because no icon pack is registered. Use `type: hollow` or `type: awesome` instead.
- **Notes have no fixed side.** The layout places a note like any other node, and it can push elements apart. Use them sparingly.
- **Secondary actors:** to get an external system on the far side of the boundary, point the relationship from the use case to the actor (`Payment -- Gateway` or `Payment --> Gateway`).
- The classic appearance is available through front matter (`config:` with `theme: default`, `look: classic`, `layout: dagre`); the default is the colourful look with orthogonal edges.

---

## References

- [Official Mermaid Use Case Diagram Documentation](https://mermaid.js.org/syntax/usecase.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)
