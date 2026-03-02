# 🚀 Quanta Compiler

Welcome to the **Quanta Compiler** project! This is our university Compiler Design project where we are building a complete, statically-typed, C-like programming language from scratch. 

Our ultimate goal is to translate our custom Quanta source code (`.qn` files) all the way down to native machine code using the LLVM infrastructure.

---

## 🎯 Project Goals
We are building a classical 3-stage compiler pipeline:
1. **Frontend:** Lexer, Parser, and Semantic Analyzer (turning text into a verified Abstract Syntax Tree).
2. **Middle-End:** Custom Intermediate Representation (IR) and code optimization passes.
3. **Backend:** Converting our IR to LLVM IR to generate an executable file.

---

## 🌌 Quanta Programming Language
```
Language Name: Quanta
File Extension: .qt
Compiler: quanta
IDE: Quanta Studio
AI Assistant: QMind
```

---

## 🏗 Compiler Architecture
```
Source (.qt)
      ↓
Lexer (Python)
      ↓
Parser (Recursive Descent / Lark)
      ↓
AST
      ↓
Semantic Analyzer
      ↓
IR Generator
      ↓
(Optional: LLVM via llvmlite)
      ↓
Bytecode / Machine Code
```

--- 

## 📁 Project Structure
To keep our code clean and avoid merge conflicts, we are dividing the project into modular folders. Here is where everything lives:
```
/quanta-ecosystem
│
├── /compiler
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── semantic.py
│   ├── ir.py
│   ├── optimizer.py
│   ├── backend.py
│   └── main.py
│
├── /language_server
│   ├── lsp.py
│   └── diagnostics.py
│
├── /studio
│   ├── /frontend (React + Monaco)
│   ├── /backend (FastAPI)
│
├── /ai_assistant
│   ├── context_engine.py
│   ├── prompt_builder.py
│   └── ai_client.py
│
├── /assets
│   ├── icons
│   ├── themes
│
└── README.md
```

---

## 🧠 Architecture
Layered design:
```
UI Layer (Quanta Studio)
        ↓
Language Server
        ↓
Compiler Frontend
        ↓
IR Layer
        ↓
Backend (LLVM or Bytecode)
```

---

## 🤝 Team Workflow & Tasks
To build this efficiently, we are splitting up the pipeline. 

* **[Friend 1 Name] - The Frontend:** Focuses on `src/frontend/lexer` and `src/frontend/parser`. Your mission is to tokenize the text and build the AST!
* **[Friend 2 Name] - The Enforcer:** Focuses on `src/frontend/semantic`. Your mission is to build the Symbol Table and handle type-checking (making sure we don't add a string to an int).
* **[Your Name] - The Translator:** Focuses on `src/middle_end` and `src/backend`. Your mission is to handle the IR and connect our tree to LLVM.

*(Note: Always remember to write tests in the `tests/` folder for your section before moving on!)*

## 🛠️ Setup Instructions
[Add instructions here on how your team should install any dependencies, like LLVM, and how to compile the project itself.]
