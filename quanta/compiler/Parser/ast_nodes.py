from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

# Base Node Types

class Expr:
    """Base class for all expression nodes.(produce values)"""
    pass


class Stmt:
    """Base class for all statement nodes.(produce side effects Not values)"""
    pass


# Expression Nodes

@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Variable(Expr):
    name: Any   # Token


@dataclass
class Assign(Expr):
    name: Any   # Token
    value: Expr


@dataclass
class Binary(Expr):
    left: Expr
    operator: Any   # Token
    right: Expr


@dataclass
class Unary(Expr):
    operator: Any   # Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Call(Expr):
    callee: Expr
    paren: Any      # closing paren token
    arguments: list[Expr]



# Statement Nodes


@dataclass
class ExpressionStmt(Stmt):
    expression: Expr


@dataclass
class PrintStmt(Stmt):
    expression: Expr


@dataclass
class VarDecl(Stmt):
    var_type: Any   # Token
    name: Any       # Token
    initializer: Optional[Expr]


@dataclass
class Block(Stmt):
    statements: list[Stmt]


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    elif_branches: list[tuple[Expr, Stmt]]
    else_branch: Optional[Stmt]


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt


@dataclass
class FunctionDecl(Stmt):
    name: Any               # Token
    params: list[Any]       # list[Token]
    body: list[Stmt]


@dataclass
class ReturnStmt(Stmt):
    keyword: Any            # Token
    value: Optional[Expr]