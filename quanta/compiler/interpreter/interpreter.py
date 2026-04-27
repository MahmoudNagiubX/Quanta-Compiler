from __future__ import annotations
from typing import Any
from .environment import Environment
from .runtime_errors import InterpreterRuntimeError, ReturnException
from quanta.compiler.parser.ast_nodes import (
    Assign,
    Binary,
    Block,
    Call,
    ExpressionStmt,
    FunctionDecl,
    Grouping,
    IfStmt,
    Literal,
    PrintStmt,
    ReturnStmt,
    Unary,
    VarDecl,
    Variable,
    WhileStmt,
)

class QuantaFunction:
    def __init__(self, declaration: FunctionDecl, closure: Environment) -> None:
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        environment = Environment(self.closure)

        for index, param in enumerate(self.declaration.params):
            environment.define(param.name.lexeme, arguments[index])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_exception:
            return return_exception.value

        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"

class Interpreter:
    def __init__(self) -> None:
        self.globals = Environment()
        self.environment = self.globals

    def interpret(self, statements: list[object]) -> None:
        for statement in statements:
            self.execute(statement)

    def execute(self, stmt: object) -> Any:
        method_name = f"_execute_{type(stmt).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            raise InterpreterRuntimeError(f"No interpreter implemented for statement '{type(stmt).__name__}'")

        return method(stmt)

    def execute_block(self, statements: list[object], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, expr: object) -> Any:
        method_name = f"_evaluate_{type(expr).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            raise InterpreterRuntimeError(f"No interpreter implemented for expression '{type(expr).__name__}'")

        return method(expr)

    def _execute_VarDecl(self, stmt: VarDecl) -> None:
        value = self.evaluate(stmt.initializer) if stmt.initializer is not None else None
        self.environment.define(stmt.name.lexeme, value)

    def _execute_PrintStmt(self, stmt: PrintStmt) -> None:
        value = self.evaluate(stmt.expression)
        print(value)

    def _execute_ExpressionStmt(self, stmt: ExpressionStmt) -> Any:
        return self.evaluate(stmt.expression)

    def _execute_Block(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def _execute_IfStmt(self, stmt: IfStmt) -> None:
        if self._is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
            return

        for elif_condition, elif_branch in stmt.elif_branches:
            if self._is_truthy(self.evaluate(elif_condition)):
                self.execute(elif_branch)
                return

        if stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def _execute_WhileStmt(self, stmt: WhileStmt) -> None:
        while self._is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def _execute_FunctionDecl(self, stmt: FunctionDecl) -> None:
        function = QuantaFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def _execute_ReturnStmt(self, stmt: ReturnStmt) -> None:
        value = self.evaluate(stmt.value) if stmt.value is not None else None
        raise ReturnException(value)

    def _evaluate_Literal(self, expr: Literal) -> Any:
        return expr.value

    def _evaluate_Variable(self, expr: Variable) -> Any:
        return self.environment.get(expr.name.lexeme)

    def _evaluate_Assign(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name.lexeme, value)
        return value

    def _evaluate_Grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def _evaluate_Unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.type.name == "MINUS":
            self._check_number_operand(expr.operator, right)
            return -right

        if expr.operator.type.name == "BANG":
            return not self._is_truthy(right)

        raise InterpreterRuntimeError(f"Unknown unary operator '{expr.operator.lexeme}'")

    def _evaluate_Binary(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operator = expr.operator.type.name

        if operator == "PLUS":
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if self._is_number(left) and self._is_number(right):
                return left + right
            raise InterpreterRuntimeError("'+' requires two numbers or two strings")

        if operator == "MINUS":
            self._check_number_operands(expr.operator, left, right)
            return left - right

        if operator == "STAR":
            self._check_number_operands(expr.operator, left, right)
            return left * right

        if operator == "SLASH":
            self._check_number_operands(expr.operator, left, right)
            if right == 0:
                raise InterpreterRuntimeError("Division by zero")
            return left / right

        if operator == "GREATER":
            self._check_number_operands(expr.operator, left, right)
            return left > right

        if operator == "GREATER_EQUAL":
            self._check_number_operands(expr.operator, left, right)
            return left >= right

        if operator == "LESS":
            self._check_number_operands(expr.operator, left, right)
            return left < right

        if operator == "LESS_EQUAL":
            self._check_number_operands(expr.operator, left, right)
            return left <= right

        if operator == "EQUAL_EQUAL":
            return self._is_equal(left, right)

        if operator == "BANG_EQUAL":
            return not self._is_equal(left, right)

        if operator == "WA":
            return self._is_truthy(left) and self._is_truthy(right)

        if operator == "AW":
            return self._is_truthy(left) or self._is_truthy(right)

        raise InterpreterRuntimeError(f"Unknown binary operator '{expr.operator.lexeme}'")

    def _evaluate_Call(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)

        if not isinstance(callee, QuantaFunction):
            raise InterpreterRuntimeError("Can only call functions")

        arguments = [self.evaluate(arg) for arg in expr.arguments]

        if len(arguments) != callee.arity():
            raise InterpreterRuntimeError(
                f"Expected {callee.arity()} arguments but got {len(arguments)}"
            )

        return callee.call(self, arguments)

    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return bool(value)

    def _is_equal(self, a: Any, b: Any) -> bool:
        return a == b

    def _is_number(self, value: Any) -> bool:
        return isinstance(value, (int, float))

    def _check_number_operand(self, operator: Any, operand: Any) -> None:
        if not self._is_number(operand):
            raise InterpreterRuntimeError(f"Operand must be a number at '{operator.lexeme}'")

    def _check_number_operands(self, operator: Any, left: Any, right: Any) -> None:
        if not self._is_number(left) or not self._is_number(right):
            raise InterpreterRuntimeError(f"Operands must be numbers at '{operator.lexeme}'")
