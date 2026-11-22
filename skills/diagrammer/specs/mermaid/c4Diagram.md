# C4 Diagrams

## Summary

C4 diagrams are a set of hierarchical diagrams for visualizing the architecture of software systems. They provide multiple levels of abstraction, from high-level system context down to detailed component and deployment views. Mermaid supports C4 diagrams with syntax compatible with PlantUML's C4-PlantUML.

> **Note:** C4 diagrams in Mermaid are experimental. Syntax and properties may change in future releases.

### Use Cases

- **System Architecture**: Visualize the structure and boundaries of software systems.
- **Documentation**: Communicate system context, containers, components, and deployment.
- **Stakeholder Communication**: Provide different levels of detail for technical and non-technical audiences.
- **DevOps**: Map out infrastructure and deployment strategies.

### When to Use

- When you need to document or communicate software architecture at multiple abstraction levels.
- When onboarding new team members to a system's structure.
- When planning or reviewing system design.

## Syntax

Mermaid supports five types of C4 diagrams:

- System Context (`C4Context`)
- Container diagram (`C4Container`)
- Component diagram (`C4Component`)
- Dynamic diagram (`C4Dynamic`)
- Deployment diagram (`C4Deployment`)

### Basic Structure

```mermaid
C4Context
  title System Context diagram for Internet Banking System
  Enterprise_Boundary(b0, "BankBoundary0") {
    Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
    System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")
  }
  BiRel(customerA, SystemAA, "Uses")
```

### Example: System Context

```mermaid
C4Context
  title System Context diagram for Internet Banking System
  Enterprise_Boundary(b0, "BankBoundary0") {
    Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
    System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")
  }
  BiRel(customerA, SystemAA, "Uses")
```

### Example: Container Diagram

```mermaid
C4Container
  title Container diagram for Internet Banking System
  Person(customer, Customer, "A customer of the bank, with personal bank accounts")
  Container_Boundary(c1, "Internet Banking") {
    Container(spa, "Single-Page App", "JavaScript, Angular", "Provides all the Internet banking functionality to customers via their web browser")
    ContainerDb(database, "Database", "SQL Database", "Stores user registration information, hashed auth credentials, access logs, etc.")
  }
  Rel(customer, spa, "Uses", "HTTPS")
```

### Example: Component Diagram

```mermaid
C4Component
  title Component diagram for Internet Banking System - API Application
  Container_Boundary(api, "API Application") {
    Component(sign, "Sign In Controller", "MVC Rest Controller", "Allows users to sign in to the internet banking system")
    Component(accounts, "Accounts Summary Controller", "MVC Rest Controller", "Provides customers with a summary of their bank accounts")
  }
  Rel(sign, accounts, "Uses")
```

### Example: Deployment Diagram

```mermaid
C4Deployment
  title Deployment Diagram for Internet Banking System - Live
  Deployment_Node(mob, "Customer's mobile device", "Apple iOS or Android") {
    Container(mobile, "Mobile App", "Xamarin", "Provides a limited subset of the Internet Banking functionality to customers via their mobile device.")
  }
  Deployment_Node(plc, "Big Bank plc", "Big Bank plc data center") {
    Deployment_Node(dn, "bigbank-api x8", "Ubuntu 16.04 LTS") {
      Container(api, "API Application", "Java and Spring MVC", "Provides Internet Banking functionality via a JSON/HTTPS API.")
    }
    Deployment_Node(dbn, "bigbank-db01", "Ubuntu 16.04 LTS") {
      ContainerDb(db, "Database", "Relational Database Schema", "Stores user registration information, hashed authentication credentials, access logs, etc.")
    }
  }
  Rel(mobile, api, "API calls", "JSON/HTTPS")
  Rel(api, db, "Reads/writes", "JDBC")
```

Every alias used in `Rel(...)` must be defined as an element somewhere in the diagram; a relation to an undefined alias is an error ("references an unknown shape or boundary"). Deployment nodes can be nested.

### Styling and Layout

- Use `UpdateElementStyle` and `UpdateRelStyle` to customize element and relationship styles.
- Use `UpdateLayoutConfig` to adjust layout (e.g., number of shapes per row).
- These statements go at the end of the diagram, after the elements and relations they refer to.
- There is no automatic layout: elements are placed in the order they are written, and relation labels can overlap shapes. Keep relation labels short, or move them with `$offsetX`/`$offsetY` in `UpdateRelStyle`.

```mermaid
C4Context
  title Styled context diagram
  Person(customer, "Customer", "Uses online banking")
  System(bank, "Internet Banking System", "Shows accounts and takes payments")
  System_Ext(mail, "E-mail System", "Sends notifications")
  Rel(customer, bank, "Uses")
  Rel(bank, mail, "Sends e-mail via", "SMTP")
  UpdateElementStyle(customer, $fontColor="white", $bgColor="darkgreen", $borderColor="black")
  UpdateRelStyle(bank, mail, $textColor="red", $lineColor="red", $offsetY="-10")
  UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Tips

- Use the appropriate C4 diagram type for the level of abstraction you need.
- Group related elements within boundaries for clarity.
- Use relationships (`Rel`, `BiRel`) to show interactions.
- Refer to [C4-PlantUML syntax](https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md) for advanced features.

**References:**
- [Mermaid.js C4 Diagram Documentation](https://mermaid.js.org/syntax/c4.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)