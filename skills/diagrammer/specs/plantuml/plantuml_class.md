# Class Diagram (PlantUML)

## Summary

A **PlantUML Class Diagram** is a UML static structure diagram that shows classes, interfaces, enums, and their relationships such as associations, inheritance, composition, and dependencies.  
It helps visualize the architecture of object-oriented systems and serves as an essential part of software documentation.

> **Note:** Class diagrams in PlantUML are stable and support advanced UML features like visibility modifiers, generics, packages, interfaces, and notes.

### Use Cases

- **Object-Oriented Design:** Model classes, interfaces, and their relationships.  
- **API Documentation:** Represent data models and service structures.  
- **System Architecture:** Show dependencies and interactions between components.  
- **Codebase Visualization:** Reverse-engineer existing code into readable UML.

### When to Use

- When you need to describe static structure (not behavior or sequence).  
- When documenting a system for onboarding or architecture review.  
- When designing new software components or refactoring existing ones.  
- When integrating class diagrams into a PlantUML-based documentation workflow.

---

## Syntax

- Start and end the diagram with `@startuml` and `@enduml`.  
- Define elements: `class`, `interface`, `abstract class`, `enum`.  
- Add attributes, methods, and relationships.  
- Optionally, include notes, packages, and skin parameters for styling.

### Basic Structure

```plantuml
@startuml
class ClassName {
  +attribute1 : Type
  -attribute2 : Type
  +method(param : Type) : ReturnType
}
@enduml
```

### Example

```plantuml
@startuml
title Example: Simple Class Diagram

class Customer {
  +id : int
  +name : String
  +email : String
  +placeOrder(order : Order) : void
}

class Order {
  +id : int
  +date : Date
  +total : float
}

Customer "1" --> "0..*" Order : places
@enduml
```

---

## Visibility Modifiers

| Symbol | Meaning    | Description                       |
|--------|-------------|-----------------------------------|
| `+`    | Public      | Visible to all classes.           |
| `-`    | Private     | Accessible only within the class. |
| `#`    | Protected   | Accessible to subclasses.         |
| `~`    | Package     | Accessible within the same package.|

### Example

```plantuml
@startuml
class Example {
  +publicAttribute : int
  -privateAttribute : String
  #protectedAttribute : float
  ~packageLevelAttribute : boolean
}
@enduml
```

---

## Relationships

PlantUML supports standard UML relationships using arrows and symbols.

| Type | Symbol | Example | Description |
|------|--------|----------|--------------|
| Association | `-->` | `Customer --> Order` | One class references another. |
| Inheritance | `--|>` | `PremiumCustomer --|> Customer` | A subclass inherits from a superclass. |
| Implementation | `..|>` | `Paypal ..|> PaymentProvider` | A class implements an interface. |
| Dependency | `..>` | `Order ..> PaymentService` | A class depends on another transiently. |
| Aggregation | `o--` | `Team o-- Player` | A class contains others (shared ownership). |
| Composition | `*--` | `Order *-- OrderLine` | A class strongly owns its components. |

### Example

```plantuml
@startuml
class Customer
class Order
class OrderLine

Customer "1" --> "0..*" Order : places >
Order "1" *-- "1..*" OrderLine : contains >
@enduml
```

---

## Packages and Grouping

Use `package` blocks to group related classes.

```plantuml
@startuml
package "E-Commerce" {
  class Customer
  class Order
  class Payment
}
@enduml
```

Packages help organize large diagrams into readable domains or layers.

---

## Interfaces and Abstract Classes

```plantuml
@startuml
interface PaymentProvider {
  +processPayment(amount : double) : boolean
}

abstract class PaymentService {
  +init() : void
}

class Paypal
Paypal ..|> PaymentProvider
Paypal --|> PaymentService
@enduml
```

---

## Enums and Constants

```plantuml
@startuml
enum OrderStatus {
  NEW
  PAID
  SHIPPED
  CANCELLED
}
@enduml
```

Enums are especially useful for representing states, constants, or type-safe values.

---

## Notes

Add notes to elements or relationships:

```plantuml
@startuml
class Order
note right of Order
  Represents a single purchase transaction.
end note

Order --> Customer : belongs to >
@enduml
```

---

## Styling and Themes

### Skin Parameters

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam class {
  BackgroundColor #f9f9f9
  BorderColor #333333
  FontColor black
}
@enduml
```

### Themes

PlantUML supports built-in and custom themes:

```plantuml
@startuml
!theme spacelab
class Product
class Category
Product --> Category
@enduml
```

See [PlantUML Themes](https://plantuml.com/theme) for available options.

---

## Advanced Features

### Generics

```plantuml
@startuml
class Repository<T> {
  +save(entity : T) : void
  +findById(id : int) : T
}
@enduml
```

### Abstract Classes and Interfaces in Use

```plantuml
@startuml
abstract class Shape {
  +draw() : void
}

class Circle
class Square

Circle --|> Shape
Square --|> Shape
@enduml
```

---

## Complete Example

```plantuml
@startuml
title Order Management System (PlantUML Class Diagram)
left to right direction
skinparam classAttributeIconSize 0

package "Customer Context" {
  class Customer {
    +id : int
    +name : String
    +email : String
    +register(email : String, pw : String) : void
  }
  class Address {
    +street : String
    +city : String
    +zip : String
  }
  Customer "1" o-- "0..*" Address : has >
}

package "Order Context" {
  class Order {
    +number : String
    +total : double
    +place() : void
  }
  class OrderLine {
    +quantity : int
    +price : double
  }
  enum OrderStatus {
    NEW
    PAID
    SHIPPED
  }
  Order "1" *-- "1..*" OrderLine
  Order --> OrderStatus
}

interface PaymentProvider {
  +charge(amount : double) : boolean
}

class CreditCardProvider
CreditCardProvider ..|> PaymentProvider
Order ..> PaymentProvider : pays via

note right of PaymentProvider
  Other providers can be added
  without modifying Order.
end note
@enduml
```

---

## Tips

- Use packages for logical grouping.  
- Apply `left to right direction` for wider layouts.  
- Combine notes and enums for clarity.  
- Customize appearance via `skinparam` or `!theme`.  
- Export with `plantuml -tpng`, `-tsvg`, or `-tpdf` as needed.

---

**References:**  
- [PlantUML Class Diagram Documentation](https://plantuml.com/class-diagram)  
- [PlantUML Themes](https://plantuml.com/theme)  
- [PlantUML Command Line Reference](https://plantuml.com/command-line)
