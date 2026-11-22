# Cynefin Diagram

## Summary

A **Cynefin diagram** in Mermaid draws the Cynefin sense-making framework: four quadrants (Complex, Complicated, Chaotic, Clear) with a Confusion area in the center, wavy boundaries and the "cliff" between Clear and Chaotic. Items such as tasks, problems or decisions are placed as small badges in the domain they belong to.

**Use Cases:**
- Sorting problems, incidents or backlog items by how predictable they are
- Choosing a fitting way of working per item (best practice, expert analysis, experiment, immediate action)
- Workshop and retrospective results
- An empty framework as a teaching or worksheet template

**When to Use:**
- When the content is explicitly about the Cynefin domains
- When there are only a few items per domain (up to four)
- Not as a general 2x2 matrix: the domain names and positions are fixed. Use a quadrant chart for other matrices

---

## Syntax Description

- Start with the `cynefin-beta` keyword.
- `title <text>` is optional. Write the text without quotes.
- A domain block starts with one of the five lowercase keywords on its own line: `complex`, `complicated`, `clear`, `chaotic`, `confusion`.
- Every item is a **double-quoted string** on its own line below the domain keyword.
- Domains can be listed in any order and can be left out; all five areas are always drawn at their fixed position.
- `%%` starts a comment line. `accTitle:` and `accDescr:` are accepted.

**Basic Syntax:**
```text
cynefin-beta
  title <Title without quotes>

  complex
    "<Item>"
  complicated
    "<Item>"
  clear
    "<Item>"
  chaotic
    "<Item>"
  confusion
    "<Item>"
```

**Fixed positions and built-in subtitles:**

| Keyword       | Position     | Subtitle drawn by Mermaid                      |
| ------------- | ------------ | ---------------------------------------------- |
| `complex`     | top left     | Probe → Sense → Respond, Emergent Practices    |
| `complicated` | top right    | Sense → Analyse → Respond, Good Practices      |
| `chaotic`     | bottom left  | Act → Sense → Respond, Novel Practices         |
| `clear`       | bottom right | Sense → Categorise → Respond, Best Practices   |
| `confusion`   | center       | Disorder                                       |

**Configuration (front matter, key `cynefin`):**

| Option                   | Default | Effect                                                    |
| ------------------------ | ------- | --------------------------------------------------------- |
| `showDomainDescriptions` | `true`  | `false` hides the subtitles listed above                  |
| `boundaryAmplitude`      | `8`     | Waviness of the boundaries; `0` gives straight lines      |
| `width`, `height`        | 800/600 | Size of the drawing area                                  |
| `seed`                   | `0`     | Any other number fixes the shape of the wavy boundaries   |

**Colors:** `themeVariables.cynefin` accepts `complexBg`, `complicatedBg`, `clearBg`, `chaoticBg`, `confusionBg`, `boundaryColor`, `cliffColor`, `labelColor`, `textColor`.

**Transitions (parsed, but not recommended in this version):**
```text
complex --> complicated : "Pattern identified"
clear --> chaotic
```
A transition is written on its own line between two different domain keywords, with an optional double-quoted label. See Rules and Pitfalls for why the examples below do not use them.

---

## Examples

### Minimal

```mermaid
cynefin-beta
  complex
    "Enter a new market"
  clear
    "Reset a password"
```

### Incident Triage with All Five Domains

```mermaid
cynefin-beta
  title Incident triage

  complex
    "Intermittent data loss"
    "Run chaos experiment"
  complicated
    "Analyze performance data"
    "Expert review needed"
  clear
    "Restart service"
    "Apply known fix"
  chaotic
    "Page on-call immediately"
  confusion
    "Unknown failure mode"
```

### Fully Loaded (Four Items per Quadrant)

Four items per quadrant and one in the center is the most that fits.

```mermaid
cynefin-beta
  title Work items by domain

  complex
    "Enter a new market"
    "Redesign onboarding"
    "Pricing experiment"
    "Team restructuring"
  complicated
    "Capacity planning"
    "Database index tuning"
    "Security audit"
    "Tax filing"
  chaotic
    "Data breach"
    "Site-wide outage"
    "Key supplier bankrupt"
    "PR crisis"
  clear
    "Password reset"
    "Invoice approval"
    "Backup rotation"
    "Expense report"
  confusion
    "Slow churn increase"
```

### Empty Framework (Template)

```mermaid
cynefin-beta
  title Cynefin Framework
  complex
  complicated
  clear
  chaotic
```

### Straight Grid, No Subtitles, Custom Colors

```mermaid
---
config:
  cynefin:
    showDomainDescriptions: false
    boundaryAmplitude: 0
  themeVariables:
    cynefin:
      complexBg: '#ffd6d6'
      clearBg: '#d6ffd6'
---
cynefin-beta
  title Where to automate
  complex
    "Explore"
  clear
    "Automate"
```

---

## Rules and Pitfalls

- **Items must be in double quotes.** An unquoted item line is a syntax error, and the parser only reports "syntax error" without a line number.
- **Domain keywords are lowercase and fixed.** `Complex` or any other name (for example `simple`, `obvious`, `disorder`) is a syntax error.
- **Do not quote the title.** `title "Incident triage"` shows the quotation marks in the picture.
- **One block per domain.** If the same domain keyword appears twice, only the items of the last block are drawn; the earlier ones disappear without a warning.
- **At most four items per quadrant.** The fifth item is drawn across the boundary into the quadrant below (top row) or outside the colored area (bottom row).
- **At most one item in `confusion`.** With the subtitles on, two items already reach the lower edge of the ellipse; three hang outside it, and from the fourth on Mermaid shows a `+N more` badge instead.
- **Keep items short** (up to about 35 characters). Items are never wrapped; a label of about 55 characters fills the whole width of a quadrant.
- **Avoid transitions.** `a --> b : "label"` renders, but the arrows start and end on top of the domain names and subtitles, run straight through the item badges, and diagonal arrows cross the Confusion area; the labels are printed on the boundary lines. If movement between domains matters, write it into the item text (for example `"Outage (stabilized: move to complex)"`) or explain it next to the diagram. A transition label must be double-quoted (an unquoted label is a syntax error); a transition from a domain to itself is ignored.
- Characters such as `'`, `(`, `)`, `&`, `,`, `:`, `;`, `#`, `%` and `/` are fine inside the quoted item.
- Hand-drawn look is not supported.

---

## References

- [Official Mermaid Cynefin Diagram Documentation](https://mermaid.js.org/syntax/cynefin.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)
