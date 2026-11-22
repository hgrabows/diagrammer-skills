# Railroad Diagram (Syntax Diagram)

## Summary

A **railroad diagram** draws the rules of a grammar as tracks: a reader follows the line from the start dot to the end dot and passes every token that a valid input must contain. Branches are alternatives, a bypass track is an optional part, a track that curves back is a repetition.

> **Note:** Railroad diagrams are a beta feature. All four keywords end in `-beta`; the plain names (`railroad`, `railroad-ebnf`) are not recognized.

**Use Cases:**
- Documenting the syntax of a language, DSL, config format or command line
- Explaining a protocol field or message format taken from an RFC (ABNF)
- Showing a parser grammar (PEG) to people who do not read grammar notation
- Illustrating a single rule, for example the shape of a number or an identifier

**When to Use:**
- The source is a grammar or can be written as one (rules, alternatives, repetition)
- Use a flowchart instead when the content is a process with decisions and side effects

---

## Syntax

### Declaration

The first line picks the notation the rules are written in. The picture is the same for all four.

| Keyword | Rules are written as | Rule form |
| --- | --- | --- |
| `railroad-ebnf-beta` | EBNF, W3C or ISO 14977 style, may be mixed | `name = definition ;` (or `::=`) |
| `railroad-abnf-beta` | ABNF as in RFC 5234 | `name = definition ;` |
| `railroad-peg-beta` | Parsing Expression Grammar | `Name <- definition ;` |
| `railroad-beta` | explicit constructor calls | `name = constructor(...) ;` |

Every rule ends with a semicolon, in all four notations. Each rule becomes one row: the rule name followed by `=` on the left, then the track. Rows are stacked in source order. A rule may span several lines.

### What is drawn

| Element | Looks like |
| --- | --- |
| Terminal (quoted literal) | rounded yellow box |
| Non-terminal (reference to a rule) | square-cornered purple box |
| Special sequence, PEG predicate, PEG `.` | dashed green box, text shown between question marks |
| Choice | stacked branches |
| Optional | bypass track above the element |
| One or more | loop back below the element |
| Zero or more | bypass above and loop below |

### EBNF operators (`railroad-ebnf-beta`)

| Meaning | W3C style | ISO style |
| --- | --- | --- |
| Terminal | `"text"` or `'text'` | same |
| Sequence | `a b` | `a , b` |
| Choice | `a \| b` | same |
| Optional | `a?` (at most one `?` per rule, see pitfalls) | `[ a ]` (preferred) |
| Zero or more | `a*` | `{ a }` |
| One or more | `a+` | (none) |
| Grouping | `( a b )` | same |
| Special sequence | (none) | `? free text ?` |
| Comment | `/* text */` | `(* text *)` |

Rule names may contain letters, digits, `_` and `-` (`if-stmt`, `my_rule`). Inside a double-quoted terminal `\"` gives a literal quote.

### ABNF operators (`railroad-abnf-beta`)

- Choice is `/`, sequence is whitespace, grouping `( a b )`, optional `[ a ]`.
- Repetition is a prefix: `*a` zero or more, `1*a` one or more.
- Numeric values (`%x41`, `%d65`, `%x30-39`, `%x0D.0A`) are drawn as terminals showing that text.
- A comment starts with `;` and must be on a line of its own.

### PEG operators (`railroad-peg-beta`)

- Ordered choice is `/`, sequence is whitespace, grouping `( a b )`.
- Suffixes `a?`, `a*`, `a+`.
- Predicates `&a` and `!a` and the any-character dot `.` are accepted and drawn as dashed boxes (`? !Keyword ?`, `? . ?`).
- A comment starts with `#` and runs to the end of the line.

### Constructors (`railroad-beta`)

`terminal("x")`, `nonterminal("name")`, `special("text")`, `sequence(a, b, ...)`, `choice(a, b, ...)`, `optional(a)`, `zeroOrMore(a)`, `oneOrMore(a)`. Names are case-sensitive, strings are quoted, the last three take exactly one argument. Use this form when the picture should not follow a grammar notation literally, for example to label a non-terminal with spaces.

`%%` comment lines work in all four notations.

---

## Examples

### Minimal rule

```mermaid
railroad-ebnf-beta
sign = "+" | "-" ;
```

### EBNF with optional parts and repetition

```mermaid
railroad-ebnf-beta
number = [ sign ] digit+ [ "." digit+ ] ;
sign = "+" | "-" ;
identifier = letter ( letter | digit | "_" )* ;
```

### EBNF in ISO style with comments and a special sequence

```mermaid
railroad-ebnf-beta
(* brackets = optional, braces = repetition, comma = sequence *)
string = '"' , { character } , '"' ;
character = ? any character except the quote ? ;
list = "[" , [ value , { "," , value } ] , "]" ;
```

### ABNF from an RFC-style specification

```mermaid
railroad-abnf-beta
; simplified address grammar
address = local-part "@" domain ;
local-part = 1*( ALPHA / DIGIT / "." / "-" ) ;
domain = label *( "." label ) ;
label = 1*( ALPHA / DIGIT ) ;
```

### PEG with a lookahead predicate

```mermaid
railroad-peg-beta
# keywords are not identifiers
Identifier <- !Keyword Letter ( Letter / Digit )* ;
Keyword <- "if" / "else" / "while" ;
Expression <- Term ( ( "+" / "-" ) Term )* ;
```

### Explicit constructors

```mermaid
railroad-beta
assignment = sequence(
    nonterminal("variable name"),
    terminal("="),
    choice(nonterminal("number"), nonterminal("quoted string")),
    optional(terminal(";"))
) ;
arguments = sequence(
    terminal("("),
    optional(sequence(
        nonterminal("expression"),
        zeroOrMore(sequence(terminal(","), nonterminal("expression")))
    )),
    terminal(")")
) ;
```

### Realistic grammar: a small query language

```mermaid
railroad-ebnf-beta
query = "SELECT" columns "FROM" table [ where-clause ] [ order-clause ] ;
columns = "*" | column ( "," column )* ;
where-clause = "WHERE" condition ( ( "AND" | "OR" ) condition )* ;
condition = column operator value ;
operator = "=" | "!=" | "LIKE" | "IN" ;
value = number | string | "NULL" ;
order-clause = "ORDER" "BY" column [ "ASC" | "DESC" ] ;
```

---

## Rules and Pitfalls

- **Semicolon after every rule.** A grammar without them (as ABNF and PEG are normally written) is a syntax error. The parser message is only "syntax error" without a position, so check the semicolons first.
- **In EBNF write optional parts as `[ a ]`, not `a?`.** A single `?` suffix in a rule works, but two of them are paired up as an ISO special sequence: `a = sign? digit tail? ;` is drawn as `sign` followed by a dashed box with the text `? digit tail ?`, without any error. PEG is not affected; there `a?` is safe.
- **No title is drawn.** `title "..."` is accepted and a front matter `title:` too, but neither appears in the picture. Do not rely on it; name the first rule meaningfully instead.
- **Never name a rule `title`.** `title = "x" ;` is read as the title statement and the diagram comes out empty without an error.
- **No `<` or `>` in a terminal.** `"<"` is drawn as the text `&lt;`, and `"<tag>"` is drawn as an empty box. Write the operator as a word or non-terminal (`less-than`) instead. `&`, quotes, brackets and non-ASCII text inside terminals are fine.
- **Rule names are ASCII only.** `Über = ...` fails. Hyphen and underscore are allowed.
- **ABNF comments need their own line.** `rule = a ; note` fails, because the first `;` already ended the rule.
- **ABNF counts are not shown.** `3DIGIT` and `2*4DIGIT` parse, but both are drawn as a plain "one or more" loop. If the exact count matters, spell it out (`DIGIT DIGIT DIGIT`) or say it in the rule name.
- **Not supported in ABNF:** incremental alternatives `=/`, prose values `<text>`, case markers `%s"..."`.
- **Not supported in EBNF:** character classes `[a-z]`, code points `#x20`, the repetition factor `3 * a`, `{ a }+`, BNF angle brackets `<name>`, a period as rule terminator, an empty alternative (`a | ;`). The exception `a - b` parses but is drawn as a plain sequence with a `-` terminal between the two, so avoid it.
- **Not supported in PEG:** character classes `[a-z]` and `=` as the rule operator. List the characters as alternatives or reference a named rule (`Letter`, `Digit`) that you leave undefined.
- **A non-terminal does not have to be defined.** Referencing `digit` without a `digit` rule is fine; it is simply a box. Leave out trivial rules to keep the picture short.
- **`railroad-beta` accepts only constructors.** `a = "x" b ;` fails there; `sequence()` without arguments fails; `(* *)` comments fail (use `%%` or `/* */`).
- **Rows do not wrap.** A long sequence makes a very wide picture. Split it into sub-rules of at most six to eight elements.
- An empty terminal `""` is drawn as an empty bubble; use `optional` / `?` to express "nothing".

---

## References

- [Official Mermaid Railroad Diagram Documentation](https://mermaid.js.org/syntax/railroad.html)
- [Mermaid.js Documentation](https://mermaid.js.org/)
