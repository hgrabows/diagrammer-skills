# Pie Chart

## Summary

A Pie Chart is a circular statistical graphic divided into slices to illustrate numerical proportions. Each slice's arc length, central angle, and area are proportional to the quantity it represents. Pie charts are ideal for visualizing part-to-whole relationships in datasets.

### Use Cases

- **Data Proportion Visualization**: Show how different categories contribute to a whole.
- **Survey Results**: Display the distribution of responses.
- **Market Share**: Illustrate the share of different companies or products.
- **Resource Allocation**: Visualize budget or resource splits.

### When to Use

- When you need to show the relative sizes of parts of a whole.
- When comparing a small number of categories.
- When you want a quick, visual representation of proportions.

## Syntax

Drawing a pie chart in Mermaid is simple:

- Start with the `pie` keyword.
- Optionally, use `showData` to display actual data values after the legend text.
- Optionally, use the `title` keyword to give the chart a title.
- List each data entry as `"Label" : value` (label in quotes, colon, positive numeric value).

**Note:** Pie chart values must be positive numbers greater than zero. Negative values are not allowed.

### Basic Structure

```mermaid
pie title Chart Title
    "Label 1" : value1
    "Label 2" : value2
    "Label 3" : value3
```

### With Data Values

```mermaid
pie showData
    title Example with Data
    "A" : 10
    "B" : 20
    "C" : 30
```

### Syntax Details

- `pie` [showData] (OPTIONAL)
- `title` [titleValue] (OPTIONAL)
- `"Label"` : value (repeat for each slice)

## Examples

### Basic Example

```mermaid
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15
```

### Example with Data Values and Custom Title

```mermaid
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" : 5
```

### Configuration

| Parameter      | Description                                                        | Default value |
| -------------- | ------------------------------------------------------------------ | ------------- |
| `textPosition` | Axial position of pie slice labels (0.0=center, 1.0=outer edge)    | `0.75`        |

Example with configuration (YAML frontmatter):

```mermaid
---
config:
  pie:
    textPosition: 0.5
  themeVariables:
    pieOuterStrokeWidth: "5px"
---
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" : 5
```

## Tips

- Use pie charts for simple, clear part-to-whole comparisons.
- Avoid using too many slices; 5-7 categories is ideal.
- Always label slices clearly for readability.

**References:**
- [Mermaid.js Pie Chart Documentation](https://mermaid.js.org/syntax/pie.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)