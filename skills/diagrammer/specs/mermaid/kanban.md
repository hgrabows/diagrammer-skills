# Kanban Diagram

## Summary

A **Kanban diagram** in Mermaid allows you to visually represent tasks as they move through different stages of a workflow. It is ideal for project management, tracking progress, and visualizing work in progress.

**Use Cases:**
- Visualizing project workflows (e.g., Todo, In Progress, Done)
- Task management and tracking
- Agile and Lean process boards
- Team collaboration and status reporting

**When to Use:**
- When you want to track tasks through various workflow stages
- When you need a visual board for project or process management

---

## Syntax Description

- Start with the `kanban` keyword.
- Define columns (stages) using a unique identifier and a title in square brackets: `columnId[Column Title]`.
- List tasks under each column, indented, with a unique identifier and a description in square brackets: `taskId[Task Description]`.
- Add metadata to tasks using the `@{ ... }` syntax for key-value pairs (e.g., assigned, ticket, priority).
- Use a configuration block at the top for global settings (e.g., ticketBaseUrl).

**Basic Syntax:**
```
kanban
  column1[Column Title]
    task1[Task Description]
```

**Column Definition:**
```
columnId[Column Title]
```

**Task Definition:**
```
taskId[Task Description]
```

**Task Metadata:**
```
taskId[Task Description]@{ ticket: MC-2037, assigned: 'knsv', priority: 'High' }
```

**Configuration Block Example:**
```yaml
---
config:
  kanban:
    ticketBaseUrl: 'https://yourproject.atlassian.net/browse/#TICKET#'
---
```

---

## Examples

### Basic Kanban

```mermaid
kanban
  todo[Todo]
    docs[Create Documentation]
```

### Kanban with Metadata

```mermaid
kanban
  todo[Todo]
    id3[Update Database Function]@{ ticket: MC-2037, assigned: 'knsv', priority: 'High' }
```

### Full Example

```mermaid
---
config:
  kanban:
    ticketBaseUrl: 'https://mermaidchart.atlassian.net/browse/#TICKET#'
---
kanban
  Todo
    [Create Documentation]
    docs[Create Blog about the new diagram]
  [In progress]
    id6[Create renderer so that it works in all cases. We also add some extra text here for testing purposes. And some more just for the extra flare.]
  id9[Ready for deploy]
    id8[Design grammar]@{ assigned: 'knsv' }
  id10[Ready for test]
    id4[Create parsing tests]@{ ticket: MC-2038, assigned: 'K.Sveidqvist', priority: 'High' }
    id66[last item]@{ priority: 'Very Low', assigned: 'knsv' }
  id11[Done]
    id5[define getData]
    id2[Title of diagram is more than 100 chars when user duplicates diagram with 100 char]@{ ticket: MC-2036, priority: 'Very High'}
    id3[Update DB function]@{ ticket: MC-2037, assigned: knsv, priority: 'High' }
  id12[Can't reproduce]
    id3[Weird flickering in Firefox]
```

---

## Tips

- Use unique identifiers for columns and tasks.
- Indent tasks under their parent columns.
- Use metadata to add context (assignee, ticket, priority).
- Use the configuration block to enable ticket linking.

---

## References

- [Official Mermaid Kanban Diagram Documentation](https://mermaid.js.org/syntax/kanban.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)