# Radar Diagram

## Summary

A **Radar diagram** (also known as a radar chart, spider chart, star chart, cobweb chart, polar chart, or Kiviat diagram) is a way to plot low-dimensional data in a circular format. It is useful for graphically summarizing and comparing the performance of multiple entities across multiple dimensions.

**Use Cases:**
- Comparing multiple entities (e.g., people, products, teams) across several quantitative attributes
- Visualizing skill sets, performance metrics, or survey results
- Summarizing multi-dimensional data in a compact, visual way

**When to Use:**
- When you want to compare several items across the same set of variables
- When you need to show strengths and weaknesses in a visual, circular format

---

## Syntax Description

- Start with the `radar-beta` keyword.
- Define axes using the `axis` keyword, with optional IDs and labels.
- Define data series (curves) using the `curve` keyword, with an ID, optional label, and a list of values.
- Optionally set `title`, `max`, `min`, `graticule`, `ticks`, and `showLegend`.
- Curves can use ordered values or key-value pairs for axis mapping.

**Basic Syntax:**
```
radar-beta
axis A, B, C, D, E
curve c1{1,2,3,4,5}
curve c2{5,4,3,2,1}
```

---

## Examples

### Grades Example

```mermaid
---
title: "Grades"
---
radar-beta
  axis m["Math"], s["Science"], e["English"]
  axis h["History"], g["Geography"], a["Art"]
  curve a["Alice"]{85, 90, 80, 70, 75, 90}
  curve b["Bob"]{70, 75, 85, 80, 90, 85}
  max 100
  min 0
```

### Restaurant Comparison

```mermaid
radar-beta
  title Restaurant Comparison
  axis food["Food Quality"], service["Service"], price["Price"]
  axis ambiance["Ambiance"]
  curve a["Restaurant A"]{4, 3, 2, 4}
  curve b["Restaurant B"]{3, 4, 3, 3}
  curve c["Restaurant C"]{2, 3, 4, 2}
  curve d["Restaurant D"]{2, 2, 4, 3}
  graticule polygon
  max 5
```

### Advanced Syntax

```mermaid
radar-beta
  axis axis1, axis2, axis3
  curve id1["Label1"]{1, 2, 3}
  curve id2["Label2"]{4, 5, 6}, id3{7, 8, 9}
  curve id4{ axis3: 30, axis1: 20, axis2: 10 }
  showLegend true
  max 100
  min 0
  graticule circle
  ticks 5
```

### Theme and Configuration Example

```mermaid
---
config:
  radar:
    axisScaleFactor: 0.25
    curveTension: 0.1
  theme: base
  themeVariables:
    cScale0: "#FF0000"
    cScale1: "#00FF00"
    cScale2: "#0000FF"
    radar:
      curveOpacity: 0
---
radar-beta
  axis A, B, C, D, E
  curve c1{1,2,3,4,5}
  curve c2{5,4,3,2,1}
  curve c3{3,3,3,3,3}
```

---

## Tips

- Use `axis` to define each dimension; you can provide labels for clarity.
- Use `curve` for each entity or data series.
- Use `max` and `min` to control the scale.
- Use `graticule` to choose between circular or polygonal grid lines.
- Use the configuration block to customize appearance and theme.

---

## References

- [Official Mermaid Radar Diagram Documentation](https://mermaid.js.org/syntax/radar.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)