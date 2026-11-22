# Quadrant Chart

## Summary

A Quadrant Chart is a visual representation of data divided into four quadrants on a two-dimensional grid. Each axis represents a variable, and data points are plotted according to their values. Quadrant charts are useful for identifying patterns, trends, and priorities based on the position of data points within the chart.

### Use Cases

- **Business Analysis**: Prioritize projects, products, or actions based on two key metrics.
- **Marketing**: Segment campaigns or customers by reach and engagement.
- **Risk Management**: Plot risks by likelihood and impact.
- **Performance Assessment**: Compare entities across two performance dimensions.

### When to Use

- When you need to compare items across two variables.
- When you want to visually segment data into four categories for decision-making.
- When prioritizing actions based on position in the chart.

## Syntax

- Start with the `quadrantChart` keyword.
- Use `title` to set the chart title (optional).
- Define axes with `x-axis` and `y-axis` (use `-->` to separate left/right or bottom/top labels).
- Label each quadrant with `quadrant-1` to `quadrant-4`.
- Plot points as `Label: [x, y]` where x and y are between 0 and 1.
- Points can be styled directly or with classes.

### Basic Structure

```mermaid
quadrantChart
    title Chart Title
    x-axis Left Label --> Right Label
    y-axis Bottom Label --> Top Label
    quadrant-1 Top Right
    quadrant-2 Top Left
    quadrant-3 Bottom Left
    quadrant-4 Bottom Right
    Point A: [0.75, 0.80]
    Point B: [0.35, 0.24]
```

### Example

```mermaid
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]
```

### Point Styling

- Direct styling: `Label: [x, y] color: #hex, radius: N, stroke-color: #hex, stroke-width: Npx`
- Class styling: `Label:::className: [x, y]`
- Define classes with `classDef`

#### Example

```mermaid
quadrantChart
  title Reach and engagement of campaigns
  x-axis Low Reach --> High Reach
  y-axis Low Engagement --> High Engagement
  quadrant-1 We should expand
  quadrant-2 Need to promote
  quadrant-3 Re-evaluate
  quadrant-4 May be improved
  Campaign A: [0.9, 0.0] radius: 12
  Campaign B:::class1: [0.8, 0.1] color: #ff3300, radius: 10
  Campaign C: [0.7, 0.2] radius: 25, color: #00ff33, stroke-color: #10f0f0
  Campaign D: [0.6, 0.3] radius: 15, stroke-color: #00ff0f, stroke-width: 5px ,color: #ff33f0
  Campaign E:::class2: [0.5, 0.4]
  Campaign F:::class3: [0.4, 0.5] color: #0000ff
  classDef class1 color: #109060
  classDef class2 color: #908342, radius : 10, stroke-color: #310085, stroke-width: 10px
  classDef class3 color: #f00fff, radius : 10
```

## Configuration

| Parameter                        | Description                                         | Default |
|-----------------------------------|-----------------------------------------------------|---------|
| chartWidth                        | Width of the chart                                  | 500     |
| chartHeight                       | Height of the chart                                 | 500     |
| titlePadding                      | Top and bottom padding of the title                 | 10      |
| titleFontSize                     | Title font size                                     | 20      |
| quadrantPadding                   | Padding outside all quadrants                       | 5       |
| quadrantTextTopPadding            | Quadrant text top padding                           | 5       |
| quadrantLabelFontSize             | Quadrant text font size                             | 16      |
| quadrantInternalBorderStrokeWidth | Border stroke width inside quadrants                | 1       |
| quadrantExternalBorderStrokeWidth | Quadrant external border stroke width               | 2       |
| xAxisLabelPadding                 | Top and bottom padding of x-axis text               | 5       |
| xAxisLabelFontSize                | X-axis text font size                               | 16      |
| xAxisPosition                     | Position of x-axis (top, bottom)                    | 'top'   |
| yAxisLabelPadding                 | Left and right padding of y-axis text               | 5       |
| yAxisLabelFontSize                | Y-axis text font size                               | 16      |
| yAxisPosition                     | Position of y-axis (left, right)                    | 'left'  |
| pointTextPadding                  | Padding between point and below text                | 5       |
| pointLabelFontSize                | Point text font size                                | 12      |
| pointRadius                       | Radius of the point                                 | 5       |

## Tips

- Use quadrant charts for clear, actionable segmentation.
- Keep axis and quadrant labels concise.
- Style points for emphasis and clarity.

**References:**
- [Mermaid.js Quadrant Chart Documentation](https://mermaid.js.org/syntax/quadrantChart.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)