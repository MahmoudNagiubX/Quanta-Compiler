from __future__ import annotations

from Lexer.token import TokenType, Token
from Parser.ast_nodes import (
    Literal,
    Variable,
    Assign,
    Binary,
    Unary,
    Grouping,
    Call,
    ExpressionStmt,
    PrintStmt,
    VarDecl,
    Block,
    IfStmt,
    WhileStmt,
    FunctionDecl,
    ReturnStmt,
)
from Parser.errors import ParseError


class Parser:
    """
    Recursive-descent parser for Quanta.

    Input:
        list[Token]

    Output:
        list[Stmt]   -> the program AST
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    # Parse the token stream into an AST (list of statements)
    
    def parse(self) -> list:  
        
        statements = []

        while not self._is_at_end():   #Keep parsing until we reach EOF(end of file)
            statements.append(self.declaration())

        return statements
    
    # Declarations ->  varDecl - funcDecl - statement
    
    def declaration(self):

        if self._match(TokenType.RAKM , TokenType.FATAFET , TokenType.KALAM , TokenType.BOOL):
            return self.var_declaration(self._previous())

        if self._match(TokenType.WASFA):
            return self.function_declaration()

        return self.statement()

    def var_declaration(self, var_type: Token):
        """
        varDecl -> type IDENTIFIER ("=" expression)? ";"
        """
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self.expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return VarDecl(var_type, name, initializer)

    def function_declaration(self):
        """
        funcDecl -> "wasfa" IDENTIFIER "(" parameters? ")" block
        """
        name = self._consume(TokenType.IDENTIFIER, "Expected function name.")
        self._consume(TokenType.LPAREN, "Expected '(' after function name.")

        params = []
        if not self._check(TokenType.RPAREN):
            while True:
                params.append(
                    self._consume(TokenType.IDENTIFIER, "Expected parameter name.")
                )
                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RPAREN, "Expected ')' after parameters.")
        self._consume(TokenType.LBRACE, "Expected '{' before function body.")

        body = self.block_statements()
        return FunctionDecl(name, params, body)

    # ============================================================
    # Statements
    # ============================================================

    def statement(self):
        """
        statement ->
              printStmt
            | ifStmt
            | whileStmt
            | returnStmt
            | block
            | exprStmt
        """

        if self._match(TokenType.ETBA3):
            return self.print_statement()

        if self._match(TokenType.LAW):
            return self.if_statement()

        if self._match(TokenType.KHALIK):
            return self.while_statement()

        if self._match(TokenType.RAGA3):
            return self.return_statement()

        if self._match(TokenType.LBRACE):
            return Block(self.block_statements())

        return self.expression_statement()

    def print_statement(self):
        """
        printStmt -> "etba3" "(" expression ")" ";"
        """
        self._consume(TokenType.LPAREN, "Expected '(' after etba3.")
        value = self.expression()
        self._consume(TokenType.RPAREN, "Expected ')' after value.")
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
        return PrintStmt(value)

    def if_statement(self):
        """
        ifStmt -> "law" "(" expression ")" statement
                  ("tb_law" "(" expression ")" statement)*
                  ("ay_haga" statement)?
        """
        self._consume(TokenType.LPAREN, "Expected '(' after law.")
        condition = self.expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition.")

        then_branch = self.statement()

        elif_branches = []
        while self._match(TokenType.TB_LAW):
            self._consume(TokenType.LPAREN, "Expected '(' after tb_law.")
            elif_condition = self.expression()
            self._consume(TokenType.RPAREN, "Expected ')' after elif condition.")
            elif_body = self.statement()
            elif_branches.append((elif_condition, elif_body))

        else_branch = None
        if self._match(TokenType.AY_HAGA):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, elif_branches, else_branch)

    def while_statement(self):
        """
        whileStmt -> "khalik" "(" expression ")" statement
        """
        self._consume(TokenType.LPAREN, "Expected '(' after khalik.")
        condition = self.expression()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition.")
        body = self.statement()
        return WhileStmt(condition, body)

    def return_statement(self):
        """
        returnStmt -> "raga3" expression? ";"
        """
        keyword = self._previous()

        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self.expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after return statement.")
        return ReturnStmt(keyword, value)

    def block_statements(self) -> list:
        """
        block -> "{" declaration* "}"
        Assumes the opening '{' was already consumed.
        """
        statements = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self.declaration())

        self._consume(TokenType.RBRACE, "Expected '}' after block.")
        return statements

    def expression_statement(self):
        """
        exprStmt -> expression ";"
        """
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExpressionStmt(expr)

    # ============================================================
    # Expressions
    # ============================================================

    def expression(self):
        return self.assignment()

    def assignment(self):
        """
        assignment -> IDENTIFIER "=" assignment | logic_or
        """
        expr = self.logic_or()

        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

            raise self._error(equals, "Invalid assignment target.")

        return expr

    def logic_or(self):
        """
        logic_or -> logic_and ("aw" logic_and)*
        """
        expr = self.logic_and()

        while self._match(TokenType.AW):
            operator = self._previous()
            right = self.logic_and()
            expr = Binary(expr, operator, right)

        return expr

    def logic_and(self):
        """
        logic_and -> equality ("wa" equality)*
        """
        expr = self.equality()

        while self._match(TokenType.WA):
            operator = self._previous()
            right = self.equality()
            expr = Binary(expr, operator, right)

        return expr

    def equality(self):
        """
        equality -> comparison (("==" | "!=") comparison)*
        """
        expr = self.comparison()

        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        """
        comparison -> term ((">" | ">=" | "<" | "<=") term)*
        """
        expr = self.term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        """
        term -> factor (("+" | "-") factor)*
        """
        expr = self.factor()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        """
        factor -> unary (("*" | "/") unary)*
        """
        expr = self.unary()

        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        """
        unary -> ("!" | "-") unary | call
        """
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def call(self):
        """
        call -> primary ("(" arguments? ")")*
        """
        expr = self.primary()

        while True:
            if self._match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def finish_call(self, callee):
        """
        Parse function call arguments after '(' has already been consumed.
        """
        arguments = []

        if not self._check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())
                if not self._match(TokenType.COMMA):
                    break

        paren = self._consume(TokenType.RPAREN, "Expected ')' after arguments.")
        return Call(callee, paren, arguments)

    def primary(self):
        """
        primary ->
              INT_LITERAL
            | FLOAT_LITERAL
            | STRING_LITERAL
            | ESHTA
            | FAKS
            | IDENTIFIER
            | "(" expression ")"
        """

        if self._match(TokenType.ESHTA):
            return Literal(True)

        if self._match(TokenType.FAKS):
            return Literal(False)

        if self._match(TokenType.INT_LITERAL):
            return Literal(int(self._previous().lexeme))

        if self._match(TokenType.FLOAT_LITERAL):
            return Literal(float(self._previous().lexeme))

        if self._match(TokenType.STRING_LITERAL):
            lexeme = self._previous().lexeme

            # Remove quotes if the lexer stores them
            if len(lexeme) >= 2 and lexeme[0] == '"' and lexeme[-1] == '"':
                lexeme = lexeme[1:-1]

            return Literal(lexeme)

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())

        if self._match(TokenType.LPAREN):
            expr = self.expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression.")
            return Grouping(expr)

        token = self._peek()
        raise self._error(token, "Expected expression.")

    # ============================================================
    # Helpers
    # ============================================================

    def _match(self, *types: TokenType) -> bool:
        """
        If current token matches any given type, consume it and return True.
        Otherwise return False.
        """
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        """
        Consume the current token if it matches token_type.
        Otherwise raise ParseError.
        """
        if self._check(token_type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        """
        Check whether current token is of the given type.
        """
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        """
        Move to the next token and return the previous one.
        """
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        """
        True if current token is EOF.
        """
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        """
        Return current token without consuming it.
        """
        return self.tokens[self.current]

    def _previous(self) -> Token:
        """
        Return most recently consumed token.
        """
        return self.tokens[self.current - 1]

    def _error(self, token: Token, message: str) -> ParseError:
        """
        Create a ParseError using token position information.
        """
        return ParseError(message, token.line, token.column)