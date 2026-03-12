"""
analyzer.py

Main semantic analyzer for the Quanta language.

This module is responsible for checking the meaning of the program
after parsing has already succeeded.

Semantic analysis checks things like:
- duplicate function declarations
- duplicate variable declarations in the same scope
- undeclared identifiers
- assignment type mismatches
- invalid condition types for when/loop
- invalid return types
- invalid binary expression operand types
- invalid function calls

This analyzer is designed in a professional multi-pass style:

Pass 1:
    Collect all function declarations into the global scope.

Pass 2:
    Validate function bodies, statements, and expressions.

Important:
This file depends on the supporting semantic files:
- scope.py
- symbols.py
- types.py
- result.py
"""

from __future__ import annotations

from typing import Optional
from .scope import Scope
from .results import SemanticResult
from .symbols import FunctionSymbol, ParameterSymbol, VariableSymbol
from .type import TYPE_NAME_MAP, NUM_TYPE, FLAG_TYPE, UNKNOWN_TYPE, QuantaType


class SemanticAnalyzer:
    """
    Main semantic analyzer class.

    Internal state:
    - result: stores collected semantic errors
    - global_scope: root scope containing global declarations (mainly functions)
    - current_scope: scope currently active during traversal
    - current_function: function currently being analyzed
    """

    def __init__(self) -> None:
        """
        Initialize the semantic analyzer.
        """
        # Final semantic result object that stores all errors.
        self.result = SemanticResult()

        # Global scope lives for the entire program.
        # All top-level function declarations are stored here.
        self.global_scope = Scope("global")

        # Current scope starts at global scope.
        self.current_scope = self.global_scope

        # Tracks the function currently being analyzed.
        # Used when checking return statements.
        self.current_function: Optional[FunctionSymbol] = None

    def analyze(self, program) -> SemanticResult:
        """
        Entry point for semantic analysis.

        Steps:
        1. Collect all function declarations into the global scope.
        2. Validate all function bodies.

        Args:
            program: root AST node of the whole program

        Returns:
            SemanticResult containing collected semantic errors.
        """
        self._collect_function_declarations(program)
        self._validate_program(program)
        return self.result

    # ============================================================
    # PASS 1: COLLECT FUNCTION DECLARATIONS
    # ============================================================

    def _collect_function_declarations(self, program) -> None:
        """
        First semantic pass.

        Purpose:
        Register all functions in the global scope before checking bodies.

        Why this matters:
        It allows recursion and forward references to functions.

        Example:
            forge fact(num n) -> num {
                emit fact(n - 1);
            }

        Assumes:
            program.functions is a list of function declaration AST nodes.
        """
        for fn in program.functions:
            # Resolve the declared return type of the function.
            return_type = self._resolve_type_name(
                fn.return_type_name,
                fn.line,
                fn.column,
            )

            parameters = []
            seen_names = set()

            # Build parameter symbols and check for duplicate parameter names.
            for param in fn.parameters:
                if param.name in seen_names:
                    self.result.add_error(
                        f"Duplicate parameter '{param.name}' in function '{fn.name}'",
                        param.line,
                        param.column,
                    )
                    continue

                seen_names.add(param.name)

                param_type = self._resolve_type_name(
                    param.type_name,
                    param.line,
                    param.column,
                )

                parameters.append(
                    ParameterSymbol(
                        name=param.name,
                        type=param_type,
                        line=param.line,
                        column=param.column,
                    )
                )

            # Create function symbol.
            function_symbol = FunctionSymbol(
                name=fn.name,
                type=return_type,  # In FunctionSymbol, 'type' means return type.
                line=fn.line,
                column=fn.column,
                parameters=parameters,
            )

            # Define function in global scope.
            # If already exists, that means duplicate function declaration.
            if not self.global_scope.define(function_symbol):
                self.result.add_error(
                    f"Duplicate function declaration '{fn.name}'",
                    fn.line,
                    fn.column,
                )

    # ============================================================
    # PASS 2: VALIDATE FUNCTION BODIES
    # ============================================================

    def _validate_program(self, program) -> None:
        """
        Second semantic pass.

        Walk through all function bodies and validate semantics.
        """
        for fn in program.functions:
            self._visit_function_decl(fn)

    def _visit_function_decl(self, node) -> None:
        """
        Validate one function declaration.

        Responsibilities:
        - lookup function symbol in global scope
        - set current_function
        - create a function scope
        - define parameters inside the function scope
        - validate the function body
        """
        function_symbol = self.global_scope.lookup(node.name)

        # Save old state so we can restore it later.
        previous_function = self.current_function
        previous_scope = self.current_scope

        # Update analyzer state for this function.
        self.current_function = function_symbol
        self.current_scope = Scope(
            name=f"function:{node.name}",
            parent=self.global_scope,
        )

        # Define parameters in the function scope.
        for param_symbol in function_symbol.parameters:
            if not self.current_scope.define(param_symbol):
                self.result.add_error(
                    f"Duplicate parameter '{param_symbol.name}'",
                    param_symbol.line,
                    param_symbol.column,
                )

        # Visit function body.
        self._visit_block(node.body)

        # Restore previous state.
        self.current_scope = previous_scope
        self.current_function = previous_function

    def _visit_block(self, node) -> None:
        """
        Validate a block node.

        For MVP:
        Every block creates a new nested scope.

        This is clean and scalable for future nested scopes.

        Assumes:
            node.statements is a list of statement nodes.
        """
        previous_scope = self.current_scope

        # Create a new child scope for this block.
        self.current_scope = Scope("block", parent=previous_scope)

        # Validate all statements in the block.
        for statement in node.statements:
            self._visit_statement(statement)

        # Restore old scope when leaving block.
        self.current_scope = previous_scope

    def _visit_statement(self, node) -> None:
        """
        Generic statement dispatcher.

        Uses dynamic dispatch based on AST class name.

        Example:
            If node class is VarDeclNode,
            this method calls self._visit_VarDeclNode(node)
        """
        method_name = f"_visit_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            self.result.add_error(
                f"No semantic handler for node '{type(node).__name__}'",
                node.line,
                node.column,
            )
            return

        method(node)

    # ============================================================
    # STATEMENT VALIDATION
    # ============================================================

    def _visit_VarDeclNode(self, node) -> None:
        """
        Validate variable declaration.

        Rules:
        - declared type must exist
        - initializer type must match declared type
        - variable cannot be redeclared in the same scope

        Example:
            num x = 5;
        """
        declared_type = self._resolve_type_name(
            node.type_name,
            node.line,
            node.column,
        )

        initializer_type = self._visit_expression(node.initializer)

        # Type compatibility check for initialization.
        if declared_type != UNKNOWN_TYPE and initializer_type != UNKNOWN_TYPE:
            if declared_type != initializer_type:
                self.result.add_error(
                    f"Cannot initialize variable '{node.name}' of type '{declared_type}' "
                    f"with value of type '{initializer_type}'",
                    node.line,
                    node.column,
                )

        # Create variable symbol.
        symbol = VariableSymbol(
            name=node.name,
            type=declared_type,
            line=node.line,
            column=node.column,
        )

        # Add variable to current scope.
        if not self.current_scope.define(symbol):
            self.result.add_error(
                f"Duplicate declaration of variable '{node.name}'",
                node.line,
                node.column,
            )

    def _visit_AssignmentNode(self, node) -> None:
        """
        Validate assignment.

        Rules:
        - variable must already be declared
        - assigned value type must match variable type

        Example:
            x = 5;
        """
        symbol = self.current_scope.lookup(node.name)

        if symbol is None:
            self.result.add_error(
                f"Undeclared identifier '{node.name}'",
                node.line,
                node.column,
            )
            return

        value_type = self._visit_expression(node.value)

        if symbol.type != UNKNOWN_TYPE and value_type != UNKNOWN_TYPE:
            if symbol.type != value_type:
                self.result.add_error(
                    f"Cannot assign value of type '{value_type}' to variable '{node.name}' "
                    f"of type '{symbol.type}'",
                    node.line,
                    node.column,
                )

    def _visit_IfNode(self, node) -> None:
        """
        Validate if statement.

        Rule:
        - condition must be of type 'flag'

        Example:
            when (x < 5) { ... }
        """
        condition_type = self._visit_expression(node.condition)

        if condition_type != UNKNOWN_TYPE and condition_type != FLAG_TYPE:
            self.result.add_error(
                "Condition of 'when' must be of type 'flag'",
                node.condition.line,
                node.condition.column,
            )

        # Validate then block.
        self._visit_block(node.then_block)

        # Validate else block if present.
        if node.else_block is not None:
            self._visit_block(node.else_block)

    def _visit_WhileNode(self, node) -> None:
        """
        Validate while loop.

        Rule:
        - condition must be of type 'flag'

        Example:
            loop (x < 5) { ... }
        """
        condition_type = self._visit_expression(node.condition)

        if condition_type != UNKNOWN_TYPE and condition_type != FLAG_TYPE:
            self.result.add_error(
                "Condition of 'loop' must be of type 'flag'",
                node.condition.line,
                node.condition.column,
            )

        self._visit_block(node.body)

    def _visit_ReturnNode(self, node) -> None:
        """
        Validate return statement.

        Rules:
        - must appear inside a function
        - returned expression type must match current function return type

        Example:
            emit x;
        """
        if self.current_function is None:
            self.result.add_error(
                "Return statement outside of function",
                node.line,
                node.column,
            )
            return

        value_type = self._visit_expression(node.value)
        expected_type = self.current_function.type

        if value_type != UNKNOWN_TYPE and expected_type != UNKNOWN_TYPE:
            if value_type != expected_type:
                self.result.add_error(
                    f"Function '{self.current_function.name}' must return '{expected_type}', "
                    f"but got '{value_type}'",
                    node.line,
                    node.column,
                )

    # ============================================================
    # EXPRESSION VALIDATION
    # ============================================================

    def _visit_expression(self, node) -> QuantaType:
        """
        Generic expression dispatcher.

        Every expression visitor returns a QuantaType.

        This is a key professional design decision because it allows
        semantic analysis to infer and validate expression types.
        """
        method_name = f"_visit_{type(node).__name__}"
        method = getattr(self, method_name, None)

        if method is None:
            self.result.add_error(
                f"No semantic handler for expression '{type(node).__name__}'",
                node.line,
                node.column,
            )
            return UNKNOWN_TYPE

        return method(node)

    def _visit_IntLiteralNode(self, node) -> QuantaType:
        """
        Integer literals always have type 'num'.

        Example:
            5
        """
        return NUM_TYPE

    def _visit_BoolLiteralNode(self, node) -> QuantaType:
        """
        Boolean literals always have type 'flag'.

        Example:
            on
            off
        """
        return FLAG_TYPE

    def _visit_IdentifierNode(self, node) -> QuantaType:
        """
        Validate identifier expression.

        Rule:
        - identifier must exist in some visible scope

        Example:
            x
        """
        symbol = self.current_scope.lookup(node.name)

        if symbol is None:
            self.result.add_error(
                f"Undeclared identifier '{node.name}'",
                node.line,
                node.column,
            )
            return UNKNOWN_TYPE

        return symbol.type

    def _visit_BinaryExprNode(self, node) -> QuantaType:
        """
        Validate binary expression.

        Supported rule groups:

        Arithmetic:
            + - * /
            requires: num, num
            returns: num

        Comparison:
            < > <= >=
            requires: num, num
            returns: flag

        Equality:
            == !=
            requires: same type on both sides
            returns: flag

        Logical:
            && ||
            requires: flag, flag
            returns: flag
        """
        left_type = self._visit_expression(node.left)
        right_type = self._visit_expression(node.right)
        op = node.operator

        arithmetic_ops = {"+", "-", "*", "/"}
        comparison_ops = {"<", ">", "<=", ">="}
        equality_ops = {"==", "!="}
        logical_ops = {"&&", "||"}

        # Arithmetic operators
        if op in arithmetic_ops:
            if left_type != NUM_TYPE or right_type != NUM_TYPE:
                self.result.add_error(
                    f"Operator '{op}' requires operands of type 'num'",
                    node.line,
                    node.column,
                )
                return UNKNOWN_TYPE
            return NUM_TYPE

        # Comparison operators
        if op in comparison_ops:
            if left_type != NUM_TYPE or right_type != NUM_TYPE:
                self.result.add_error(
                    f"Operator '{op}' requires operands of type 'num'",
                    node.line,
                    node.column,
                )
                return UNKNOWN_TYPE
            return FLAG_TYPE

        # Equality operators
        if op in equality_ops:
            if left_type == UNKNOWN_TYPE or right_type == UNKNOWN_TYPE:
                return UNKNOWN_TYPE

            if left_type != right_type:
                self.result.add_error(
                    f"Operator '{op}' requires both operands to have the same type",
                    node.line,
                    node.column,
                )
                return UNKNOWN_TYPE

            return FLAG_TYPE

        # Logical operators
        if op in logical_ops:
            if left_type != FLAG_TYPE or right_type != FLAG_TYPE:
                self.result.add_error(
                    f"Operator '{op}' requires operands of type 'flag'",
                    node.line,
                    node.column,
                )
                return UNKNOWN_TYPE
            return FLAG_TYPE

        # Unknown operator
        self.result.add_error(
            f"Unknown binary operator '{op}'",
            node.line,
            node.column,
        )
        return UNKNOWN_TYPE

    def _visit_CallExprNode(self, node) -> QuantaType:
        """
        Validate function call expression.

        Rules:
        - function must exist
        - target must actually be a function
        - argument count must match
        - argument types must match parameter types

        Example:
            add(1, 2)
        """
        symbol = self.global_scope.lookup(node.name)

        if symbol is None:
            self.result.add_error(
                f"Call to undeclared function '{node.name}'",
                node.line,
                node.column,
            )
            return UNKNOWN_TYPE

        if not isinstance(symbol, FunctionSymbol):
            self.result.add_error(
                f"'{node.name}' is not a function",
                node.line,
                node.column,
            )
            return UNKNOWN_TYPE

        if len(node.arguments) != len(symbol.parameters):
            self.result.add_error(
                f"Function '{node.name}' expects {len(symbol.parameters)} arguments "
                f"but got {len(node.arguments)}",
                node.line,
                node.column,
            )
            return symbol.type

        for argument_node, parameter_symbol in zip(node.arguments, symbol.parameters):
            arg_type = self._visit_expression(argument_node)

            if arg_type != UNKNOWN_TYPE and arg_type != parameter_symbol.type:
                self.result.add_error(
                    f"Argument for parameter '{parameter_symbol.name}' must be "
                    f"'{parameter_symbol.type}', got '{arg_type}'",
                    argument_node.line,
                    argument_node.column,
                )

        return symbol.type

    # ============================================================
    # HELPERS
    # ============================================================

    def _resolve_type_name(self, type_name: str, line: int, column: int) -> QuantaType:
        """
        Convert a type name string into a QuantaType object.

        Example:
            "num"  -> NUM_TYPE
            "flag" -> FLAG_TYPE

        If type is unknown, record an error and return UNKNOWN_TYPE.
        """
        resolved = TYPE_NAME_MAP.get(type_name)

        if resolved is None:
            self.result.add_error(
                f"Unknown type '{type_name}'",
                line,
                column,
            )
            return UNKNOWN_TYPE

        return resolved