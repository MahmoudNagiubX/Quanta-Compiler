# 🚀 Quanta Compiler

Welcome to the Quanta Compiler project!
This repository contains the full implementation of Quanta, a statically-typed, C-like programming language designed and built from scratch as part of a university Compiler Design project.
The goal of this project is to build a complete modern compiler pipeline, translating Quanta source code (`.qn` files) into native machine code using the LLVM infrastructure.

---

## 🌌 The Quanta Ecosystem
Quanta is not just a compiler — it is a complete programming ecosystem.

| Component | Description |
|---|---|
| **Quanta Language** | Custom statically-typed programming language |
| **Quanta Compiler** | Translates `.qn` files into executable code |
| **Quanta Studio** | IDE built for the language |
| **Language Server** | Provides IDE features like diagnostics |
| **QMind AI Assistant** | AI assistant for Quanta developers |

Core details of the ecosystem: 

| Item | Value |
|---|---|
| **Language Name** | Quanta |
| **File Extension** | `.qt` |
| **Compiler** | `quanta` |
| **IDE** | Quanta Studio |
| **AI Assistant** | QMind |

---

## 🎯 Project Goals
We are building a full production-style compiler architecture consisting of three major layers:

### 1️⃣ Frontend
Transforms raw source code into a validated Abstract Syntax Tree (AST).
Components:
* Lexer
* Parser
* AST Builder
* Semantic Analyzer

### 2️⃣ Middle-End
Transforms the AST into an Intermediate Representation (IR) and applies optimizations.
Components:
* IR Generator
* Optimization Passes

Examples of optimizations:
* Constant Folding
* Dead Code Elimination
* Algebraic Simplification
* Control Flow Simplification

### 3️⃣ Backend
Transforms IR into machine code.
Backend options:
* LLVM IR (via llvmlite)
* Custom bytecode VM

---

## 🏗 Compiler Pipeline
The data flow through our compiler follows this architecture: 

```text
Source (.qn)
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

## 🔎 Compiler Stages Explained

### 🧾 1. Lexer
The Lexer converts raw text into tokens.
Example source code:
```c
rakm x = 5;
```
Token stream produced:
```text
TYPE IDENTIFIER ASSIGN NUMBER SEMICOLON
```
Lexer responsibilities:
* Identify keywords
* Parse identifiers
* Parse numbers
* Recognize operators
* Handle comments
* Track source positions

### 🌳 2. Parser
The Parser converts tokens into an Abstract Syntax Tree (AST).
Example AST:
```text
Program
 └── VariableDeclaration
     ├── Type: rakm
     ├── Name: x
     └── Value: 5
```
Parser responsibilities:
* Syntax validation
* Operator precedence
* Grammar rule enforcement
* AST node creation

### 🌲 3. Abstract Syntax Tree (AST)
The AST is the structural representation of the program.
Example Quanta code:
```c
rakm x = 10;
rakm y = x + 5;
```
AST representation:
```text
Program
 ├── VarDecl
 │   ├── type: rakm
 │   ├── name: x
 │   └── value: 10
 │
 └── VarDecl
     ├── type: rakm
     ├── name: y
     └── value:
         BinaryExpression(+)
             ├── Identifier(x)
             └── Literal(5)
```

### 🧠 4. Semantic Analyzer
The semantic analyzer ensures logical correctness.
Checks include:
* Undeclared variables
* Type mismatches
* Function argument validation
* Return type validation
* Scope resolution

Example error:
```c
rakm x = "hello";
```
Error produced:
```text
TypeError: cannot assign string to rakm
```

### ⚙️ 5. IR Generator
The IR Generator converts AST into a lower-level representation.
Example AST:
```text
x = 5 + 3
```
Generated IR:
```text
t1 = 5
t2 = 3
t3 = t1 + t2
x = t3
```
Why IR exists:
* Simplifies optimization
* Removes high-level syntax
* Enables efficient code generation

### ⚡ 6. Optimizer
Optimizes the Intermediate Representation.
Example optimization:
Original IR:
```text
t1 = 2
t2 = 3
t3 = t1 + t2
x = t3
```
Optimized IR:
```text
x = 5
```
Optimizations implemented:
* Constant Folding
* Dead Code Elimination
* Copy Propagation
* Strength Reduction

### 🧩 7. Backend
The backend converts IR into machine code.
Process:
```text
IR → LLVM IR → Assembly → Executable
```

---

## 📁 Complete Project Structure

```text
quanta-ecosystem
│
├── compiler
│   │
│   ├── Lexer
│   │   ├── lexer.py
│   │   └── token.py
│   │
│   ├── Parser
│   │   ├── parser.py
│   │   └── ast_nodes.py
│   │
│   ├── Semantic
│   │   ├── analyzer.py
│   │   ├── symbols.py
│   │   └── types.py
│   │
│   ├── IR
│   │   ├── ir_generator.py
│   │   ├── ir_nodes.py
│   │   └── ir_builder.py
│   │
│   ├── Optimizer
│   │   └── optimizer.py
│   │
│   ├── Backend
│   │   ├── llvm_backend.py
│   │   └── codegen.py
│   │
│   ├── tests
│   │   ├── test_lexer.py
│   │   ├── test_parser.py
│   │   └── test_semantic.py
│   │
│   └── main.py
│
├── language_server
│   ├── lsp.py
│   └── diagnostics.py
│
├── studio
│   ├── frontend (React + Monaco Editor)
│   └── backend (FastAPI)
│
├── ai_assistant
│   ├── context_engine.py
│   ├── prompt_builder.py
│   └── ai_client.py
│
├── assets
│   ├── icons
│   └── themes
│
└── README.md
```

---

## 🧠 System Architecture
The Quanta ecosystem uses a layered architecture. 

```text
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
Each layer communicates only with the one below it.
Benefits:
* Modular design
* Easier debugging
* Parallel team development

---

## 🤝 Team Workflow & Responsibilities
Suggested roles for the team:

| Role | Responsibility |
|---|---|
| **Lexer Engineer** | Tokenization |
| **Parser Engineer** | Grammar + AST |
| **Semantic Engineer** | Type system + symbol tables |
| **IR Engineer** | Intermediate representation |
| **Optimization Engineer** | Optimization passes |
| **Backend Engineer** | LLVM code generation |

---

## 🧑‍💻 Development Workflow
Recommended Git branch strategy:

```text
main
│
├── lexer
├── parser
├── semantic
├── ir
├── optimizer
└── backend
```
Workflow:
1️⃣ Create feature branch
2️⃣ Implement module
3️⃣ Write tests
4️⃣ Open pull request
5️⃣ Merge into main

---

## 🛠️ Setup Instructions
Install dependencies:
```bash
pip install -r requirements.txt
```
Install LLVM (optional backend):
Linux:
```bash
sudo apt install llvm
```
Mac:
```bash
brew install llvm
```

---

## ▶️ Running the Compiler
Compile a Quanta program:
```bash
python compiler/main.py program.qn
```

---

## 🧪 Running Tests
Run individual tests:
```bash
python compiler/tests/test_lexer.py
python compiler/tests/test_parser.py
python compiler/tests/test_semantic.py
```

---

## 🗺️ Development Roadmap

### Phase 1 — Frontend
* Lexer
* Parser
* AST
* Semantic Analyzer

### Phase 2 — Middle-End
* IR Generator
* Optimization passes

### Phase 3 — Backend
* LLVM integration
* Machine code generation

### Phase 4 — Ecosystem
* IDE
* Language server
* AI assistant

---

## 📚 Learning Goals
This project helps us understand:
* Compiler design
* Language implementation
* Static typing systems
* IR design
* Optimization algorithms
* LLVM architecture

---

## 💡 Vision
Quanta aims to become a complete educational programming ecosystem that demonstrates how modern compilers are built.
The project integrates:
* programming language design
* compiler architecture
* development tooling
* AI-assisted coding

---

## 🏁 Final Goal
Transform this:
```c
rakm x = 5;
etba3(x);
```
Into:
```text
Executable machine code
```
Through a fully functional compiler pipeline.