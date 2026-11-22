# XY Chart

## Summary

An **XY Chart** in Mermaid is a general charting module for visualizing data along two axes — an X-axis and a Y-axis. It currently supports two fundamental chart types, **bar** and **line**, and is designed to display numeric or categorical series over a shared axis. XY charts are suitable for trend visualization, category comparison, and simple analytics dashboards.

> **Note:** XY charts in Mermaid are evolving. Syntax, configuration, and supported chart types may change in future releases.  
> See the official docs: https://mermaid.js.org/syntax/xyChart.html

### Use Cases

- **Time series / trends**: Show how a value changes over months/quarters.
- **Category comparison**: Compare KPI values across products, regions, or teams.
- **Combined views**: Overlay a line over bars to compare “actual vs. target.”
- **Lightweight dashboards**: Embed simple charts directly in Markdown docs.

### When to Use

- When you have **two dimensions** (category/time on X, numeric values on Y).
- When a **bar or line chart** is sufficient — no need for full BI tooling.
- When you want charts in **text-based documentation** (Git, wikis, code repos).
- When you need to **configure orientation** (vertical/horizontal) for readability.

---

## Syntax

- Start with the `xychart` keyword.
- Optionally specify orientation: `xychart horizontal`.
- Add a `title` to describe the chart.
- Define `x-axis` (categories or labeled axis).
- Define `y-axis` with label and numeric range.
- Add one or more data series: `bar [...]` or `line [...]`.
- Give a series a name to show it in the legend: `bar "name" [...]`, `line "name" [...]`.
- Values in a series must align with the X-axis items.
- Axis and series lines only work inside a chart that starts with `xychart`; a chart needs at least one `bar` or `line`.

### Basic Structure

```mermaid
xychart
    title "Sales per Quarter"
    x-axis ["Q1", "Q2", "Q3", "Q4"]
    y-axis "Revenue ($)" 0 --> 12000
    bar [5000, 7500, 9000, 11000]
```

This renders a vertical bar chart with four categories.

---

### Example: Bar + Line

```mermaid
xychart
    title "Monthly Revenue vs. Target"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Amount ($)" 0 --> 12000
    bar  [5000, 6400, 7200, 8800, 9900, 11500]
    line [4800, 6000, 7000, 9000, 10000, 11000]
```

- `bar [...]` shows actuals.
- `line [...]` shows target/forecast.
- Both series share the same X-axis.

---

### Orientations

You can switch to a horizontal layout (better for long labels):

```mermaid
xychart horizontal
    title "Top Products by Units"
    x-axis ["Prod A", "Prod B", "Prod C", "Prod D"]
    y-axis "Units" 0 --> 400
    bar [320, 280, 210, 150]
```

---

### Axes

**X-Axis**  
- Typically a **list of categories**, optionally with a title in front: `x-axis "Month" ["Jan", "Feb", "Mar"]`
- Or a numeric range: `x-axis "Concurrent users" 0 --> 500` (the values of a series are then spread evenly over the range).
- If a title or category has spaces, wrap it in quotes: `"New York"`, `"Total Sales"`.

**Y-Axis**  
- Always numeric, with a **title** and an optional **range**: `y-axis "Value" 0 --> 100`
- Without a range (`y-axis "Value"`) the range is derived from the data.

```mermaid
xychart
    title "Signups"
    x-axis "Month" ["Jan", "Feb", "Mar"]
    y-axis "New users" 0 --> 100
    line [35, 60, 85]
```

Make sure the range covers all your data values; otherwise bars/lines may be clipped.

---

### Legend and Colors

Named series appear in a legend to the right of the plot; unnamed series are left out of it. The default colours are pale (a single unnamed line is hard to see), so set `plotColorPalette` when contrast matters: the colours are assigned to the series in the order they are written.

```mermaid
---
config:
  themeVariables:
    xyChart:
      plotColorPalette: "#4c78a8, #f58518, #54a24b"
---
xychart
    title "Response Time by Release"
    x-axis ["v1.0", "v1.1", "v1.2", "v2.0"]
    y-axis "Milliseconds" 0 --> 400
    bar "p95" [320, 290, 240, 180]
    line "median" [120, 110, 95, 70]
    line "target" [150, 150, 150, 150]
```

---

### Configuration (frontmatter style)

You can configure width, height, and theming via Mermaid’s config block:

```mermaid
---
config:
  xyChart:
    width: 800
    height: 450
---
xychart
    title "Configured Chart"
    x-axis [A, B, C, D]
    y-axis "Score" 0 --> 100
    bar [40, 55, 70, 90]
```

Colors are set via `themeVariables.xyChart` (e.g. `plotColorPalette`, `titleColor`), see above. `showDataLabel: true` under `xyChart` prints each value into its bar, but the labels are drawn very large in this renderer.

---

## Tips

- Keep the number of categories reasonable; rotate to `horizontal` for long names.
- Use a **line** series to show trend or target on top of **bars**.
- Always set a **descriptive title** so readers understand context immediately.
- Ensure the **Y-axis range** includes your max value.
- For multi-word labels, always quote them.
- Name every series when there is more than one, so the legend explains them.

---

**References:**  
- [Mermaid.js XY Chart Documentation](https://mermaid.js.org/syntax/xyChart.html)  
- [Mermaid.js Documentation](https://mermaid.js.org/)
