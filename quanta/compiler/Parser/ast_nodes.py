from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# ============================================================
# Base node classes
# ============================================================

class Expr:
    """
    Base class for all expression nodes.

    Expressions produce values.
    Example:
        5
        x + 1
        add(a, b)
    """
    pass


class Stmt:
    """
    Base class for all statement nodes.

    Statements do actions / side effects.
    Example:
        rakm x = 5;
        etba3(x);
        law (...) { ... }
    """
    pass

# ============================================================
# Expression nodes
# ============================================================

@dataclass
class Literal(Expr):
    """
    Literal value such as:
    - integer
    - float
    - string
    - boolean
    """
    value: Any

@dataclass
class Variable(Expr):
    """
    Read a variable by name.
    Example:
        x
    """
    name: Any   # Token

@dataclass
class Assign(Expr):
    """
    Assignment expression.
    Example:
        x = 10
    """
    name: Any   # Token
    value: Expr

@dataclass
class Binary(Expr):
    """
    Binary operation.
    Examples:
        a + b
        x > y
        p wa q
    """
    left: Expr
    operator: Any   # Token
    right: Expr

@dataclass
class Unary(Expr):
    """
    Unary operation.
    Examples:
        -x
        !flag
    """
    operator: Any   # Token
    right: Expr

@dataclass
class Grouping(Expr):
    """
    Expression inside parentheses.
    Example:
        (a + b)
    """
    expression: Expr

@dataclass
class Call(Expr):
    """
    Function call.
    Example:
        add(1, 2)
    """
    callee: Expr
    paren: Any      # closing ')' token
    arguments: list[Expr]

# ============================================================
# Helper nodes
# ============================================================

@dataclass
class Parameter:
    """
    One function parameter.

    Example:
        rakm a
    """
    param_type: Any   # Token
    name: Any         # Token

# ============================================================
# Statement nodes
# ============================================================

@dataclass
class ExpressionStmt(Stmt):
    """
    Plain expression used as a statement.
    Example:
        x + 1;
    """
    expression: Expr

@dataclass
class PrintStmt(Stmt):
    """
    Built-in print statement.
    Example:
        etba3(x);
    """
    expression: Expr

@dataclass
class VarDecl(Stmt):
    """
    Variable declaration.

    Example:
        rakm x = 5;
        kalam name;
    """
    var_type: Any      # Token
    name: Any          # Token
    initializer: Expr | None

@dataclass
class Block(Stmt):
    """
    A scoped block.
    Example:
        {
            rakm x = 1;
            etba3(x);
        }
    """
    statements: list[Stmt]

@dataclass
class IfStmt(Stmt):
    """
    if / else-if / else chain.
    """
    condition: Expr
    then_branch: Stmt
    elif_branches: list[tuple[Expr, Stmt]]
    else_branch: Stmt | None

@dataclass
class WhileStmt(Stmt):
    """
    while loop.
    """
    condition: Expr
    body: Stmt

@dataclass
class FunctionDecl(Stmt):
    """
    Function declaration.

    Examples:
        rakm add(rakm a, rakm b) {
            raga3 a + b;
        }

        wasfa main() {
            etba3("hello");
        }
    """
    return_type: Any             # Token
    name: Any                    # Token
    params: list[Parameter]
    body: list[Stmt]

@dataclass
class ReturnStmt(Stmt):
    """
    Return statement inside function.
    Example:
        raga3 result;
    """
    keyword: Any                 # Token
    value: Expr | None