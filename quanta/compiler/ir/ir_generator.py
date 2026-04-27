from __future__ import annotations
from typing import Any
from quanta.compiler.parser.ast_nodes import (Assign, Binary, Block, Call, ExpressionStmt,
    FunctionDecl, Grouping, IfStmt, Literal, PrintStmt, ReturnStmt, Unary,
    VarDecl, Variable, WhileStmt,)
from .ir_instruction import Assign as IRAssign, BinaryOp, Call as IRCall, Goto, IfGoto, Label, Print, Return

class IRGenerator:
    def __init__(self) -> None:
        self.instructions: list[Any] = []
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, program: list) -> list[Any]:
        for stmt in program:
            self._visit_statement(stmt)
        return self.instructions

    def _new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def _new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"

    def _visit_statement(self, node: Any) -> None:
        method_name = f"_visit_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if method is None:
            raise ValueError(f"IR generation not implemented for '{type(node).__name__}'")
        method(node)

    def _visit_VarDecl(self, node: VarDecl) -> None:
        if node.initializer is None:
            return
        value = self._visit_expression(node.initializer)
        self.instructions.append(IRAssign(node.name.lexeme, value))

    def _visit_ExpressionStmt(self, node: ExpressionStmt) -> None:
        self._visit_expression(node.expression)

    def _visit_PrintStmt(self, node: PrintStmt) -> None:
        value = self._visit_expression(node.expression)
        self.instructions.append(Print(value))

    def _visit_Block(self, node: Block) -> None:
        for stmt in node.statements:
            self._visit_statement(stmt)

    def _visit_FunctionDecl(self, node: FunctionDecl) -> None:
        self.instructions.append(Label(node.name.lexeme))
        for stmt in node.body:
            self._visit_statement(stmt)

    def _visit_ReturnStmt(self, node: ReturnStmt) -> None:
        if node.value is None:
            self.instructions.append(Return())
            return
        value = self._visit_expression(node.value)
        self.instructions.append(Return(value))

    def _visit_IfStmt(self, node: IfStmt) -> None:
        end_label = self._new_label()
        else_label = self._new_label() if node.elif_branches or node.else_branch else end_label

        condition = self._visit_expression(node.condition)
        then_label = self._new_label()

        self.instructions.append(IfGoto(condition, then_label))
        self.instructions.append(Goto(else_label))
        self.instructions.append(Label(then_label))
        self._visit_statement(node.then_branch)
        self.instructions.append(Goto(end_label))

        current_false_label = else_label

        for index, (elif_condition, elif_stmt) in enumerate(node.elif_branches):
            next_label = self._new_label()
            next_false_label = self._new_label() if index < len(node.elif_branches) - 1 or node.else_branch else end_label

            self.instructions.append(Label(current_false_label))
            condition = self._visit_expression(elif_condition)
            self.instructions.append(IfGoto(condition, next_label))
            self.instructions.append(Goto(next_false_label))
            self.instructions.append(Label(next_label))
            self._visit_statement(elif_stmt)
            self.instructions.append(Goto(end_label))

            current_false_label = next_false_label

        if node.else_branch is not None:
            self.instructions.append(Label(current_false_label))
            self._visit_statement(node.else_branch)

        self.instructions.append(Label(end_label))

    def _visit_WhileStmt(self, node: WhileStmt) -> None:
        start_label = self._new_label()
        end_label = self._new_label()

        self.instructions.append(Label(start_label))
        condition = self._visit_expression(node.condition)
        self.instructions.append(IfGoto(f"NOT {condition}", end_label))
        self._visit_statement(node.body)
        self.instructions.append(Goto(start_label))
        self.instructions.append(Label(end_label))

    def _visit_expression(self, node: Any) -> str:
        method_name = f"_visit_expr_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if method is None:
            raise ValueError(f"IR generation not implemented for expression '{type(node).__name__}'")
        return method(node)

    def _visit_expr_Literal(self, node: Literal) -> str:
        if isinstance(node.value, str):
            return f'"{node.value}"'
        if isinstance(node.value, bool):
            return "true" if node.value else "false"
        return str(node.value)

    def _visit_expr_Variable(self, node: Variable) -> str:
        return node.name.lexeme

    def _visit_expr_Assign(self, node: Assign) -> str:
        value = self._visit_expression(node.value)
        self.instructions.append(IRAssign(node.name.lexeme, value))
        return node.name.lexeme

    def _visit_expr_Binary(self, node: Binary) -> str:
        left = self._visit_expression(node.left)
        right = self._visit_expression(node.right)
        target = self._new_temp()
        self.instructions.append(BinaryOp(target, left, node.operator.lexeme, right))
        return target

    def _visit_expr_Grouping(self, node: Grouping) -> str:
        return self._visit_expression(node.expression)

    def _visit_expr_Unary(self, node: Unary) -> str:
        operand = self._visit_expression(node.right)
        operator = node.operator.lexeme
        if operator == "-":
            target = self._new_temp()
            self.instructions.append(BinaryOp(target, "0", "-", operand))
            return target
        if operator == "!":
            return f"!{operand}"
        return operand

    def _visit_expr_Call(self, node: Call) -> str:
        args = [self._visit_expression(arg) for arg in node.arguments]
        if not isinstance(node.callee, Variable):
            raise ValueError("IR generation only supports named function calls.")
        target = self._new_temp()
        self.instructions.append(IRCall(target, node.callee.name.lexeme, args))
        return target
