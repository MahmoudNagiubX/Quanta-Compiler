# quanta-compiler Language Specification v0.1

## 1. Overview

Project Mission:
The mission of quanta-compiler is to transform programming into a natural form of expression for Egyptian students by using familiar terminology and logic.

Remove Linguistic Barriers: Eliminate the struggle of learning English syntax alongside programming logic, allowing beginners to focus entirely on computational thinking.

Cultural Empowerment: Create a sense of ownership and pride in technology by showing that a powerful programming language can speak the same way its users do.

Bridge the Educational Gap: Serve as a progressive stepping stone that introduces structured "C-like" habits—such as mandatory braces and explicit typing—while keeping the entry point friendly and accessible.

Foster Logical Fluency: Use intuitive keywords like etba3 (print) and 2oly (input) to make the flow of data feel like a conversation, helping students visualize how a computer processes information.

Encourage Early Mastery: By simplifying the "front-end" experience of coding, students can master complex concepts like nested loops (tol lma) and function recursion (ya) much earlier in their educational journey.

Advanced features such as arrays, strings, boolean types, loops are intentionally excluded  to keep the language simple and focused.

---

## 2. Syntax Style

Quanta compiler follows a python syntax structure.

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

quanta-compiler supports two numeric types.

### 3.1 rakm (Integer)

Represents signed integers.

Example:

```
rakm x = 5;
```

---

### 3.2 fatafet (Float)

Represents floating-point numbers.

Example:

```
fatafet y = 7.3;
```

---

### 3.3 Type System Rules

- Variables are statically typed.
- Type is fixed at declaration.
- Redeclaring a variable in the same scope is an error.
- Assigning to an undeclared variable is an error.

---

### 3.4 Implicit Conversions

quanta-compiler allows implicit conversions:

- `rakm → fatafet` (integer to float) is allowed.
- `fatafet → rakm` (float to integer) is allowed.

Float-to-integer conversion:

- Always truncates toward zero.
- `5.5 → 5`
- `-10.2 → -10`

Truncation happens automatically wherever a `rakm` is expected.

---


### 3.5 ya_ah_ya_la (Boolean)
Native boolean type for conditions. 
- `eshta` represents true (1).
- `fakes` represents false (0).
Example:
`ya_ah_ya_la is_ready = eshta;`
---

### 3.6 kalam (String)
Represents text. Text must be wrapped in double quotes.
Example:
`kalam greeting = "Ahlan wa sahlan!";`

---

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

Functions are declared using the keyword `wasfa`.

Example:

```
wasfa add(rakm a, rakm b) {
    rakm result = a + b;
    raga3 result;
}
```

---

### 4.3 Scopes

rakm x = 10;        // Global scope (The Street)

{                   // <--- START of a new scope
    rakm y = 5;     // This 'y' only exists inside these braces
    etba3(x + y);   // Prints 15 (it can see 'x' outside)
}                   // <--- END of the scope

etba3(x);           // This works! (10)
etba3(y);           // ERROR! 'y' was destroyed when the block ended.

---

### 4.4 Variable Declaration Rules

Examples:

```
rakm x = 5;
fatafet y = 3.2;
```

Rules:

- Type remains fixed after declaration.
- Assignments must respect type rules and implicit conversions.

---

## 5. Control Flow

### 5.1 If Statement

Keyword: `law`

```
law (condition) {
    ...
}
```

---

### 5.2 Else If

Keyword sequence: `tb law`

```
law (condition1) {
    ...
}
tb law (condition2) {
    ...
}
ay haga {
    ...
}
```

---

### 5.3 Else

Keyword: `ay haga`

---

### 5.4 switch 

keyword: `ekhtar`

example:
rakm yom = 1;

ekhtar (yom):
    law_kan 1:
        etba3("El 7ad");
    law_kan 2:
        etba3("El Etneen");
    ay_7aga:
        etba3("Yom tani");
---
### 5.4 While Loop

Keyword sequence: `khalik`

Only while loops are supported in v0.1.

```
khalik (condition) {
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

Division `/` always returns `fatafet`.

Example:

```
rakm x = 5 / 2;   // 5 / 2 = 2.5 → it will be 2
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

- `eshta` if true
- `fakes` if false

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

Built-in function: `oly(prompt_string);`
Halts the program and waits for the user to type something and press Enter. Always returns a `kalam` (string).
Example:

```
kalam name = 2oly("Esmak eh ya basha? ");
etba3("Ahlan " + name);

```
---

## 8. Keywords

Reserved keywords:

- `rakm`
- `fatafet`
- `ya`
- `law`
- `tb law`
- `ekhtar`
- `raga3`
- `khalik`
- `etba3`
- `wa`
- `kalam`
- `ya_ah_ya_la`, `eshta`, `faks`
- `taboor`
- `lef`
- `wasfa`
- `etba3`
- `raga3`
- `eshta`
- `fakes`
- `law_kan`
- `oly`




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