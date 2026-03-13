""" semantic analyzer checks the meaning of the program 🧠 """
from __future__ import annotations
from typing import Optional
from quanta.compiler.parser.ast_nodes import (Assign, Binary, Block, Call, ExpressionStmt,
    FunctionDecl, Grouping, IfStmt, Literal, Parameter, PrintStmt, ReturnStmt,
    Unary, VarDecl, Variable, WhileStmt,)
from .results import SemanticResult
from .scope import Scope
from .symbols import FunctionSymbol, ParameterSymbol, VariableSymbol
from .type import (
    FATAFET_TYPE,
    KALAM_TYPE,
    RAKM_TYPE,
    TYPE_NAME_MAP,
    UNKNOWN_TYPE,
    VOID_TYPE,
    YA_AH_YA_LA_TYPE,
    QuantaType,
)

class SemanticAnalyzer:
    """
    Semantic analyzer for the current Quanta AST.

    Input:
        program: list[Stmt]

    Responsibilities:
    - collect function declarations
    - validate statements and expressions
    - manage scopes
    - detect type and name errors
    """

    def __init__(self) -> None:
        self.result = SemanticResult()

        self.global_scope = Scope("global")
        self.current_scope = self.global_scope

        self.current_function: Optional[FunctionSymbol] = None

    def analyze(self, program: list) -> SemanticResult:
        """
        Run semantic analysis in two passes.

        Pass 1:
            collect all function declarations in global scope

        Pass 2:
            validate all top-level declarations/statements
        """
        self._collect_function_declarations(program)
        self._validate_program(program)
        return self.result

    # ============================================================
    # PASS 1: collect function declarations
    # ============================================================

    def _collect_function_declarations(self, program: list) -> None:
        """
        Register all functions before validating bodies.

        This allows:
        - recursion
        - calling functions before their definitions
        """
        for stmt in program:
            if not isinstance(stmt, FunctionDecl):
                continue

            param_symbols: list[ParameterSymbol] = []
            seen_names: set[str] = set()

            for param in stmt.params:
                param_name = param.name.lexeme

                if param_name in seen_names:
                    self.result.add_error(
                        f"Duplicate parameter '{param_name}' in function '{stmt.name.lexeme}'",
                        param.name.line,
                        param.name.column,
                    )
                    continue

                seen_names.add(param_name)

                param_type = self._token_to_type(param.param_type)

                param_symbols.append(
                    ParameterSymbol(
                        name=param_name,
                        type=param_type,
                        line=param.name.line,
                        column=param.name.column,
                    )
                )

            function_symbol = FunctionSymbol(
                name=stmt.name.lexeme,
                line=stmt.name.line,
                column=stmt.name.column,
                parameters=param_symbols,
                type=UNKNOWN_TYPE,   # current AST has no declared return type
            )

            if not self.global_scope.define(function_symbol):
                self.result.add_error(
                    f"Duplicate function declaration '{stmt.name.lexeme}'",
                    stmt.name.line,
                    stmt.name.column,
                )

    # ============================================================
    # PASS 2: validate program
    # ============================================================

    def _validate_program(self, program: list) -> None:
        for stmt in program:
            self._visit_statement(stmt)

    # ============================================================
    # Statement visitors
    # ============================================================

    def _visit_statement(self, node) -> None:
        method_name = f"_visit_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            self.result.add_error(
                f"No semantic visitor implemented for statement '{type(node).__name__}'",
                0,
                0,
            )
            return

        method(node)

    def _visit_FunctionDecl(self, node: FunctionDecl) -> None:
        """
        Validate a function body in its own scope.
        """
        function_symbol = self.global_scope.lookup(node.name.lexeme)

        previous_scope = self.current_scope
        previous_function = self.current_function

        self.current_scope = Scope(f"function:{node.name.lexeme}", parent=self.global_scope)
        self.current_function = function_symbol if isinstance(function_symbol, FunctionSymbol) else None

        # Define parameters in function scope.
        seen_names: set[str] = set()
        for param in node.params:
            param_name = param.name.lexeme
            param_type = self._token_to_type(param.param_type)

            if param_name in seen_names:
                # Duplicate already reported in pass 1, so skip re-report.
                continue

            seen_names.add(param_name)

            ok = self.current_scope.define(
                ParameterSymbol(
                    name=param_name,
                    type=param_type,
                    line=param.name.line,
                    column=param.name.column,
                )
            )

            if not ok:
                self.result.add_error(
                    f"Duplicate parameter '{param_name}'",
                    param.name.line,
                    param.name.column,
                )

        for stmt in node.body:
            self._visit_statement(stmt)

        self.current_scope = previous_scope
        self.current_function = previous_function

    def _visit_Block(self, node: Block) -> None:
        """
        Each block gets its own nested scope.
        """
        previous_scope = self.current_scope
        self.current_scope = Scope("block", parent=previous_scope)

        for stmt in node.statements:
            self._visit_statement(stmt)

        self.current_scope = previous_scope

    def _visit_VarDecl(self, node: VarDecl) -> None:
        """
        Validate variable declaration and optional initializer.
        """
        var_name = node.name.lexeme
        declared_type = self._token_to_type(node.var_type)

        if not self.current_scope.define(
            VariableSymbol(
                name=var_name,
                type=declared_type,
                line=node.name.line,
                column=node.name.column,
            )
        ):
            self.result.add_error(
                f"Duplicate variable declaration '{var_name}'",
                node.name.line,
                node.name.column,
            )

        if node.initializer is not None:
            init_type = self._visit_expression(node.initializer)

            if not self._is_assignable(declared_type, init_type):
                self.result.add_error(
                    f"Cannot assign value of type '{init_type}' to variable '{var_name}' of type '{declared_type}'",
                    node.name.line,
                    node.name.column,
                )

    def _visit_PrintStmt(self, node: PrintStmt) -> None:
        self._visit_expression(node.expression)

    def _visit_ExpressionStmt(self, node: ExpressionStmt) -> None:
        self._visit_expression(node.expression)

    def _visit_IfStmt(self, node: IfStmt) -> None:
        cond_type = self._visit_expression(node.condition)

        if cond_type != YA_AH_YA_LA_TYPE and cond_type != UNKNOWN_TYPE:
            self.result.add_error(
                "If condition must be of type 'ya_ah_ya_la'",
                self._expr_line(node.condition),
                self._expr_column(node.condition),
            )

        self._visit_statement(node.then_branch)

        for elif_condition, elif_stmt in node.elif_branches:
            elif_type = self._visit_expression(elif_condition)

            if elif_type != YA_AH_YA_LA_TYPE and elif_type != UNKNOWN_TYPE:
                self.result.add_error(
                    "Else-if condition must be of type 'ya_ah_ya_la'",
                    self._expr_line(elif_condition),
                    self._expr_column(elif_condition),
                )

            self._visit_statement(elif_stmt)

        if node.else_branch is not None:
            self._visit_statement(node.else_branch)

    def _visit_WhileStmt(self, node: WhileStmt) -> None:
        cond_type = self._visit_expression(node.condition)

        if cond_type != YA_AH_YA_LA_TYPE and cond_type != UNKNOWN_TYPE:
            self.result.add_error(
                "While condition must be of type 'ya_ah_ya_la'",
                self._expr_line(node.condition),
                self._expr_column(node.condition),
            )

        self._visit_statement(node.body)

    def _visit_ReturnStmt(self, node: ReturnStmt) -> None:
        """
        Current AST limitation:
        we can detect 'return outside function', but not strict function
        return-type compatibility because FunctionDecl has no return_type yet.
        """
        if self.current_function is None:
            self.result.add_error(
                "Return statement used outside of function",
                node.keyword.line,
                node.keyword.column,
            )
            return

        if node.value is not None:
            self._visit_expression(node.value)

    # ============================================================
    # Expression visitors
    # ============================================================

    def _visit_expression(self, node) -> QuantaType:
        method_name = f"_visit_expr_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            self.result.add_error(
                f"No semantic visitor implemented for expression '{type(node).__name__}'",
                0,
                0,
            )
            return UNKNOWN_TYPE

        return method(node)

    def _visit_expr_Literal(self, node: Literal) -> QuantaType:
        if isinstance(node.value, bool):
            return YA_AH_YA_LA_TYPE

        if isinstance(node.value, int):
            return RAKM_TYPE

        if isinstance(node.value, float):
            return FATAFET_TYPE

        if isinstance(node.value, str):
            return KALAM_TYPE

        return UNKNOWN_TYPE

    def _visit_expr_Variable(self, node: Variable) -> QuantaType:
        symbol = self.current_scope.lookup(node.name.lexeme)

        if symbol is None:
            self.result.add_error(
                f"Use of undeclared identifier '{node.name.lexeme}'",
                node.name.line,
                node.name.column,
            )
            return UNKNOWN_TYPE

        return symbol.type

    def _visit_expr_Assign(self, node: Assign) -> QuantaType:
        symbol = self.current_scope.lookup(node.name.lexeme)

        value_type = self._visit_expression(node.value)

        if symbol is None:
            self.result.add_error(
                f"Assignment to undeclared variable '{node.name.lexeme}'",
                node.name.line,
                node.name.column,
            )
            return UNKNOWN_TYPE

        if isinstance(symbol, FunctionSymbol):
            self.result.add_error(
                f"Cannot assign to function '{node.name.lexeme}'",
                node.name.line,
                node.name.column,
            )
            return UNKNOWN_TYPE

        if not self._is_assignable(symbol.type, value_type):
            self.result.add_error(
                f"Cannot assign value of type '{value_type}' to variable '{node.name.lexeme}' of type '{symbol.type}'",
                node.name.line,
                node.name.column,
            )

        return symbol.type

    def _visit_expr_Grouping(self, node: Grouping) -> QuantaType:
        return self._visit_expression(node.expression)

    def _visit_expr_Unary(self, node: Unary) -> QuantaType:
        right_type = self._visit_expression(node.right)

        if node.operator.type.name == "MINUS":
            if right_type in (RAKM_TYPE, FATAFET_TYPE, UNKNOWN_TYPE):
                return right_type
            self.result.add_error(
                "Unary '-' requires numeric operand",
                node.operator.line,
                node.operator.column,
            )
            return UNKNOWN_TYPE

        if node.operator.type.name == "BANG":
            if right_type in (YA_AH_YA_LA_TYPE, UNKNOWN_TYPE):
                return YA_AH_YA_LA_TYPE
            self.result.add_error(
                "Unary '!' requires boolean operand",
                node.operator.line,
                node.operator.column,
            )
            return UNKNOWN_TYPE

        return UNKNOWN_TYPE

    def _visit_expr_Binary(self, node: Binary) -> QuantaType:
        left_type = self._visit_expression(node.left)
        right_type = self._visit_expression(node.right)
        op = node.operator.type.name

        # Arithmetic operators
        if op in ("PLUS", "MINUS", "STAR", "SLASH"):
            if op == "PLUS" and left_type == KALAM_TYPE and right_type == KALAM_TYPE:
                return KALAM_TYPE

            if self._is_numeric(left_type) and self._is_numeric(right_type):
                if left_type == FATAFET_TYPE or right_type == FATAFET_TYPE:
                    return FATAFET_TYPE
                return RAKM_TYPE

            if left_type != UNKNOWN_TYPE and right_type != UNKNOWN_TYPE:
                self.result.add_error(
                    f"Operator '{node.operator.lexeme}' requires compatible numeric operands",
                    node.operator.line,
                    node.operator.column,
                )
            return UNKNOWN_TYPE

        # Comparison operators
        if op in ("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            if self._is_numeric(left_type) and self._is_numeric(right_type):
                return YA_AH_YA_LA_TYPE

            if left_type != UNKNOWN_TYPE and right_type != UNKNOWN_TYPE:
                self.result.add_error(
                    f"Operator '{node.operator.lexeme}' requires numeric operands",
                    node.operator.line,
                    node.operator.column,
                )
            return UNKNOWN_TYPE

        # Equality operators
        if op in ("EQUAL_EQUAL", "BANG_EQUAL"):
            if (
                left_type == right_type
                or left_type == UNKNOWN_TYPE
                or right_type == UNKNOWN_TYPE
                or (self._is_numeric(left_type) and self._is_numeric(right_type))
            ):
                return YA_AH_YA_LA_TYPE

            self.result.add_error(
                f"Cannot compare values of type '{left_type}' and '{right_type}'",
                node.operator.line,
                node.operator.column,
            )
            return UNKNOWN_TYPE

        # Logical operators
        if op in ("WA", "AW"):
            if (
                left_type in (YA_AH_YA_LA_TYPE, UNKNOWN_TYPE)
                and right_type in (YA_AH_YA_LA_TYPE, UNKNOWN_TYPE)
            ):
                return YA_AH_YA_LA_TYPE

            self.result.add_error(
                f"Logical operator '{node.operator.lexeme}' requires boolean operands",
                node.operator.line,
                node.operator.column,
            )
            return UNKNOWN_TYPE

        return UNKNOWN_TYPE

    def _visit_expr_Call(self, node: Call) -> QuantaType:
        """
        Validate function call.

        Current AST/parser only allows calling identifiers normally,
        so we mainly support calls like:
            add(1, 2)
        """
        if not isinstance(node.callee, Variable):
            self.result.add_error(
                "Only named functions can be called",
                node.paren.line,
                node.paren.column,
            )

            for arg in node.arguments:
                self._visit_expression(arg)

            return UNKNOWN_TYPE

        function_name = node.callee.name.lexeme
        symbol = self.global_scope.lookup(function_name)

        if symbol is None or not isinstance(symbol, FunctionSymbol):
            self.result.add_error(
                f"Call to undeclared function '{function_name}'",
                node.callee.name.line,
                node.callee.name.column,
            )

            for arg in node.arguments:
                self._visit_expression(arg)

            return UNKNOWN_TYPE

        if len(node.arguments) != len(symbol.parameters):
            self.result.add_error(
                f"Function '{function_name}' expects {len(symbol.parameters)} argument(s) but got {len(node.arguments)}",
                node.paren.line,
                node.paren.column,
            )

        for index, arg in enumerate(node.arguments):
            arg_type = self._visit_expression(arg)

            if index < len(symbol.parameters):
                expected_type = symbol.parameters[index].type
                if not self._is_assignable(expected_type, arg_type):
                    self.result.add_error(
                        f"Argument {index + 1} of function '{function_name}' expects type '{expected_type}' but got '{arg_type}'",
                        self._expr_line(arg),
                        self._expr_column(arg),
                    )

        # Current AST has no explicit declared return type.
        return symbol.type

    # ============================================================
    # Helpers
    # ============================================================

    def _token_to_type(self, type_token) -> QuantaType:
        """
        Convert parser type token to semantic type.
        """
        return TYPE_NAME_MAP.get(type_token.lexeme, UNKNOWN_TYPE)

    def _is_numeric(self, typ: QuantaType) -> bool:
        return typ in (RAKM_TYPE, FATAFET_TYPE)

    def _is_assignable(self, target: QuantaType, value: QuantaType) -> bool:
        """
        Assignment compatibility rules.

        Current rule:
        - exact same type is allowed
        - rakm can go into fatafet
        - unknown is tolerated to avoid cascading errors
        """
        if target == UNKNOWN_TYPE or value == UNKNOWN_TYPE:
            return True

        if target == value:
            return True

        # int -> float is allowed
        if target == FATAFET_TYPE and value == RAKM_TYPE:
            return True

        return False

    def _expr_line(self, expr) -> int:
        """
        Best-effort line extraction for error reporting.
        """
        if hasattr(expr, "name") and hasattr(expr.name, "line"):
            return expr.name.line

        if hasattr(expr, "operator") and hasattr(expr.operator, "line"):
            return expr.operator.line

        if hasattr(expr, "paren") and hasattr(expr.paren, "line"):
            return expr.paren.line

        return 0

    def _expr_column(self, expr) -> int:
        """
        Best-effort column extraction for error reporting.
        """
        if hasattr(expr, "name") and hasattr(expr.name, "column"):
            return expr.name.column

        if hasattr(expr, "operator") and hasattr(expr.operator, "column"):
            return expr.operator.column

        if hasattr(expr, "paren") and hasattr(expr.paren, "column"):
            return expr.paren.column
        return 0