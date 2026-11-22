# Mindmap (PlantUML)

## Summary

A **Mindmap** in PlantUML is a hierarchical diagram that visually organizes ideas, concepts, or topics around a central theme.  
Each node represents a concept, and child nodes represent subtopics branching from their parent.  
PlantUML mindmaps provide an elegant, text-based way to model relationships and conceptual hierarchies directly in source code.

> **Note:** Mindmap diagrams in PlantUML are stable and part of the core syntax.  
> They can be rendered in multiple formats (PNG, SVG, PDF, etc.) via the standard `@startmindmap` / `@endmindmap` syntax.

### Use Cases

- **Brainstorming:** Capture ideas and structure them around a main concept.  
- **Project Planning:** Break projects into hierarchical components.  
- **Knowledge Representation:** Show relationships between concepts or entities.  
- **Documentation:** Represent high-level summaries of complex systems or reports.

### When to Use

- When you need to represent hierarchical or tree-like relationships.  
- When visualizing concept hierarchies, system structures, or plans.  
- When integrating conceptual maps directly within technical documentation.

---

## Syntax

- Start and end the diagram with `@startmindmap` and `@endmindmap`.  
- Use indentation (`*`, `**`, `***`, etc.) to define hierarchy levels.  
- Add formatting, icons, or colors for emphasis.  
- Each line defines a node; deeper levels indicate subtopics.

### Basic Structure

```plantuml
@startmindmap
* Root
** First Branch
*** Sub-branch A
*** Sub-branch B
** Second Branch
@endmindmap
```

### Example

```plantuml
@startmindmap
* **Mindmap**
** Origins
*** Long history
*** Popularisation
**** British author Tony Buzan
** Research
*** On effectiveness and features
*** On automatic creation
**** Uses
***** Creative techniques
***** Strategic planning
***** Argument mapping
** Tools
*** Pen and paper
*** PlantUML
@endmindmap
```

---

## Node Styling and Formatting

### Colors

You can assign background and text colors using standard PlantUML color syntax.

```plantuml
@startmindmap
* Root
** <back:lightblue>Blue Branch
*** <back:lightgreen>Green Sub-branch
@endmindmap
```

### Fonts and Emphasis

PlantUML supports inline formatting with Markdown-like syntax:

- **Bold:** `**text**`
- *Italic:* `//text//`
- `__Underlined__`
- `~~Strikethrough~~`

```plantuml
@startmindmap
* **Main Topic**
** //Italic Subtopic//
*** __Underline Example__
*** ~~Deprecated Concept~~
@endmindmap
```

---

## Icons

Icons can be added via the [OpenIconic](https://useiconic.com/open) or [Font Awesome](https://fontawesome.com) sets if your renderer supports them.

```plantuml
@startmindmap
* :fa-lightbulb: Innovation
** :fa-cogs: Engineering
** :fa-brain: Research
@endmindmap
```

---

## Layouts and Orientation

By default, PlantUML renders mindmaps **from left to right**.  
You can change the layout using the `!theme` directive or by setting styles.

```plantuml
@startmindmap
* <back:lightyellow>Project Plan
** :fa-flag: Initiation
** :fa-tasks: Execution
** :fa-check: Closure
@endmindmap
```

PlantUML automatically balances branches for tidy tree layouts.  
Unlike Mermaid, layout parameters (e.g., tidy-tree) are **inherent** and not defined via YAML frontmatter.

---

## Themes and Styles

PlantUML mindmaps fully support theming and style sheets:

```plantuml
@startmindmap
!theme spacelab
* Root
** Subtopic 1
** Subtopic 2
@endmindmap
```

You can also define your own style blocks:

```plantuml
@startmindmap
<style>
mindmapDiagram {
  node {
    BackgroundColor lightgray
    FontColor black
    FontSize 14
  }
}
</style>
* Themed Mindmap
** Node A
** Node B
@endmindmap
```

---

## Tips

- Use consistent indentation to maintain hierarchy clarity.  
- Combine bold and color styling for readability.  
- Themes can drastically change the diagram’s appearance — use `!theme` or custom `<back:color>` tags.  
- Export diagrams with `plantuml -tpng` or `plantuml -tsvg` for different outputs.

---

**References:**  
- [PlantUML Mindmap Documentation](https://plantuml.com/mindmap-diagram)  
- [PlantUML Style and Themes Guide](https://plantuml.com/theme)  
- [PlantUML Command Line Reference](https://plantuml.com/command-line)
