# Codawy Language Specification v0.1

## 1. Overview

Codawy v0.1 is a custom programming language implemented in Python.

The goal of Codawy is to serve as an educational programming language designed to introduce children and beginners to core programming concepts in a structured and culturally adapted way.

Codawy is designed to teach programming fundamentals clearly and progressively, particularly in an Egyptian educational context, using simplified Arabic-inspired keywords.

Version 0.1 focuses on introducing the following core programming concepts:

- Integer and floating-point arithmetic
- Statically typed variables
- Conditional statements (including nested conditionals)
- Loops (including nested loops)
- Functions
- Basic printing

Advanced features such as arrays, strings, boolean types, classes, and complex data structures are intentionally excluded in v0.1 to keep the language simple and focused.

---

## 2. Syntax Style

Codawy follows a C-like syntax structure.

### 2.1 Blocks

Blocks are defined using curly braces:

```
{
    statement1;
    statement2;
}
```

Braces are mandatory for control flow bodies.  
Single-line bodies without `{}` are not allowed.

---

### 2.2 Statement Termination

Each statement must end with a semicolon `;`.

Example:

```
rakm x = 5;
x = x + 1;
```

---

### 2.3 Comments

Single-line comment:

```
// this is a comment
```

Multi-line comment:

```
/*
   multi-line
   comment
*/
```

---

## 3. Data Types

Codawy v0.1 supports two numeric types.

### 3.1 rakm (Integer)

Represents signed integers.

Example:

```
rakm x = 5;
```

---

### 3.2 kasr (Float)

Represents floating-point numbers.

Example:

```
kasr y = 7.3;
```

---

### 3.3 Type System Rules

- Variables are statically typed.
- Type is fixed at declaration.
- Redeclaring a variable in the same scope is an error.
- Assigning to an undeclared variable is an error.

---

### 3.4 Implicit Conversions

Codawy allows implicit conversions:

- `rakm → kasr` (integer to float) is allowed.
- `kasr → rakm` (float to integer) is allowed.

Float-to-integer conversion:

- Always truncates toward zero.
- `7.7 → 7`
- `-7.7 → -7`

Truncation happens automatically wherever a `rakm` is expected.

---

### 3.5 Boolean Semantics

Codawy does not have a boolean type.

Instead:

- `1` represents true.
- `0` represents false.
- Any value other than `1` or `0` inside a condition is an error.

Valid:

```
lw (1) { ... }
```

Error:

```
lw (3) { ... }
```

---
### 3.6 kalam (String)
Represents text. Text must be wrapped in double quotes.
Example:
`kalam greeting = "Ahlan wa sahlan!";`

### 3.7 ya_ah_ya_la (Boolean)
Native boolean type for conditions. 
- `eshta` represents true (1).
- `fakes` represents false (0).
Example:
`ya_ah_ya_la is_ready = eshta;`

### 3.8 taboor (Arrays)
Represents a fixed list of items of the same type.
Example:
`taboor daragat = [90, 85, 95];`

---

## 4. Program Structure and Scope

### 4.1 Program Structure

A program consists of:

- Function definitions
- Top-level statements

Top-level statements execute in order from top to bottom.

---

### 4.2 Function Declaration

Functions are declared using the keyword `ya`.

Example:

```
ya add(rakm a, rakm b) {
    rakm result = a + b;
    raga3 result;
}
```

---

### 4.3 Scopes

Scopes are created by:

- The global program
- Each function body
- Each block `{ ... }`

Variable lookup follows lexical scoping:

- Search current scope first
- Then outer scope
- If not found → error

---

### 4.4 Variable Declaration Rules

Examples:

```
rakm x = 5;
kasr y = 3.2;
```

Rules:

- Type remains fixed after declaration.
- Assignments must respect type rules and implicit conversions.

---

## 5. Control Flow

### 5.1 If Statement

Keyword: `lw`

```
lw (condition) {
    ...
}
```

---

### 5.2 Else If

Keyword sequence: `tb lw`

```
lw (condition1) {
    ...
}
tb lw (condition2) {
    ...
}
aw {
    ...
}
```

---

### 5.3 Else

Keyword: `aw`

---

### 5.4 While Loop

Keyword sequence: `tol lma`

Only while loops are supported in v0.1.

```
tol lma (condition) {
    ...
}
```

---

### 5.5 For Loop
Keyword: `lef`
Used to loop a specific number of times. It includes an initializer, a condition, and a step.
Example:
```

lef (rakm i = 0; i < 5; i = i + 1) {
    etba3(i);
}

```

---

## 6. Expressions and Operators

### 6.1 Arithmetic Operators

- `+`
- `-`
- `*`
- `/`

Division `/` always returns `kasr`.

Example:

```
rakm x = 5 / 2;   // 5 / 2 = 2.5 → truncated to 2
```

---

### 6.2 Comparison Operators

- `==`
- `!=`
- `<`
- `>`
- `<=`
- `>=`

Comparison results:

- `1` if true
- `0` if false

---

### 6.3 Logical Operators

Logical operators are used to combine multiple conditions together. 

- `wa` (Logical AND): Returns `1` if both sides are true, otherwise `0`.
- `aw` (Logical OR): Returns `1` if at least one side is true, otherwise `0`.

Example:
```
lw (x > 5 wa x < 10) {
    etba3(x);
}
```

---

### 6.4 Operator Precedence

From highest to lowest:

1. Parentheses `( )`
2. `* /`
3. `+ -`
4. Comparisons `< > <= >= == !=`
5. `wa` (AND)
6. `aw` (OR)

All arithmetic operators are left-associative.

---

## 7. Built-in Function

### 7.1 Printing (Output)

Built-in function: `etba3(expression);`
Used to output variables or string literals to the screen.

### 7.2 Asking for Input (User Input)

Built-in function: `2oly(prompt_string);`
Halts the program and waits for the user to type something and press Enter. Always returns a `kalam` (string).
Example:

```
kalam name = weshweshny("Esmak eh ya basha? ");
etba3("Ahlan " + name);

```
---

## 8. Keywords

Reserved keywords:

- `rakm`
- `kasr`
- `ya`
- `lw`
- `aw`
- `tb`
- `tol`
- `lma`
- `raga3`
- `etba3`
- `wa`
- `kalam`
- `ya_ah_ya_la`, `eshta`, `faks`
- `rasa`
- `laff`
- `2oly`


Identifiers cannot use these names.

---

## 9. Identifiers

Rules:

- Must start with a letter or underscore.
- Followed by letters, digits, or underscores.
- Case-sensitive.

Examples:

```
x
_sum
value1
```

---

## 10. Whitespace

Whitespace is ignored except as separator between tokens.

---

## 11. Formal Grammar (BNF)

To build the Parser, Codawy uses a formal grammar to define exactly how tokens can be combined to form valid code. This ensures the syntax is predictable and mathematically sound.

### 11.1 Program and Functions
A program is a list of top-level statements or function declarations.

* `<program>` ::= `<declaration>*`
* `<declaration>` ::= `<function_decl> | <statement>`
* `<function_decl>` ::= `"ya"` `<identifier>` `"("` `<parameters>?` `")"` `<block>`
* `<parameters>` ::= `<type>` `<identifier>` ( `","` `<type>` `<identifier>` )*

### 11.2 Types and Blocks
* `<type>` ::= `"rakm" | "kasr"`
* `<block>` ::= `"{"` `<statement>*` `"}"`

### 11.3 Statements
Every statement (except blocks and control flow) must end with a semicolon.

* `<statement>` ::= `<var_decl> | <assignment> | <if_stmt> | <while_stmt> | <return_stmt> | <print_stmt> | <block>`
* `<var_decl>` ::= `<type>` `<identifier>` `"="` `<expression>` `";"`
* `<assignment>` ::= `<identifier>` `"="` `<expression>` `";"`
* `<return_stmt>` ::= `"raga3"` `<expression>` `";"`
* `<print_stmt>` ::= `"etba3"` `"("` `<print_arg>` `")"` `";"`
* `<print_arg>` ::= `<expression> | <string_literal>`

### 11.4 Control Flow
Notice how the `tb lw` (else if) and `aw` (else) chain together!

* `<if_stmt>` ::= `"lw"` `"("` `<expression>` `")"` `<block>` ( `"tb lw"` `"("` `<expression>` `")"` `<block>` )* ( `"aw"` `<block>` )?
* `<while_stmt>` ::= `"tol lma"` `"("` `<expression>` `")"` `<block>`

### 11.5 Expressions & Operator Precedence
Expressions are ordered from lowest precedence (Logical OR) to highest precedence (Primary numbers/variables). This enforces the correct order of operations!

* `<expression>` ::= `<logical_or>`
* `<logical_or>` ::= `<logical_and>` ( `"aw"` `<logical_and>` )*
* `<logical_and>` ::= `<equality>` ( `"wa"` `<equality>` )*
* `<equality>` ::= `<comparison>` ( ( `"==" | "!="` ) `<comparison>` )*
* `<comparison>` ::= `<term>` ( ( `"<" | ">" | "<=" | ">="` ) `<term>` )*
* `<term>` ::= `<factor>` ( ( `"+" | "-"` ) `<factor>` )*
* `<factor>` ::= `<primary>` ( ( `"*" | "/"` ) `<primary>` )*

### 11.6 Primary Values
The most basic building blocks of math and logic.

* `<primary>` ::= `<integer_literal> | <float_literal> | <identifier> | <function_call> | "(" <expression> ")"`
* `<function_call>` ::= `<identifier>` `"("` `<arguments>?` `")"`
* `<arguments>` ::= `<expression>` ( `","` `<expression>` )*
* `<integer_literal>` ::= `-?` `[0-9]+`
* `<float_literal>` ::= `-?` `[0-9]+ "." [0-9]+`
* `<string_literal>` ::= `"\"" [^"]* "\""`