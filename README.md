# 🚀 Quanta Compiler

Welcome to the **Quanta Compiler** project! This is our university Compiler Design project where we are building a complete, statically-typed, C-like programming language from scratch. 

Our ultimate goal is to translate our custom Quanta source code (`.ax` files) all the way down to native machine code using the LLVM infrastructure.

## 🎯 Project Goals
We are building a classical 3-stage compiler pipeline:
1. **Frontend:** Lexer, Parser, and Semantic Analyzer (turning text into a verified Abstract Syntax Tree).
2. **Middle-End:** Custom Intermediate Representation (IR) and code optimization passes.
3. **Backend:** Converting our IR to LLVM IR to generate an executable file.

## 📁 Project Structure
To keep our code clean and avoid merge conflicts, we are dividing the project into modular folders. Here is where everything lives:

* `src/frontend/` - Code for reading and validating the source code (Lexer, Parser, AST, Semantic Analysis).
* `src/middle_end/` - Code for our custom IR and optimizations (like Constant Folding).
* `src/backend/` - Code for hooking into LLVM and generating machine code.
* `tests/` - **Important:** All tests go here! We must test each module (lexer, parser, etc.) separately.
* `examples/` - Sample `.ax` Quanta programs to test our compiler.

## 🤝 Team Workflow & Tasks
To build this efficiently, we are splitting up the pipeline. 

* **[Friend 1 Name] - The Frontend:** Focuses on `src/frontend/lexer` and `src/frontend/parser`. Your mission is to tokenize the text and build the AST!
* **[Friend 2 Name] - The Enforcer:** Focuses on `src/frontend/semantic`. Your mission is to build the Symbol Table and handle type-checking (making sure we don't add a string to an int).
* **[Your Name] - The Translator:** Focuses on `src/middle_end` and `src/backend`. Your mission is to handle the IR and connect our tree to LLVM.

*(Note: Always remember to write tests in the `tests/` folder for your section before moving on!)*

## 🛠️ Setup Instructions
[Add instructions here on how your team should install any dependencies, like LLVM, and how to compile the project itself.]
