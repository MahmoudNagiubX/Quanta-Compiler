from __future__ import annotations
from .token import TokenType, Token, LexerError


class Lexer:
    # Keyword normalization + aliases based on the spec
    KEYWORDS = {
        # types
        "rakm": TokenType.RAKM,
        "fatafet": TokenType.FATAFET,
        "kasr": TokenType.FATAFET,  # alias from BNF
        "kalam": TokenType.KALAM,
        "ya_ah_ya_la": TokenType.BOOL,

        # booleans (support inconsistent spellings)
        "eshta": TokenType.ESHTA,
        "faks": TokenType.FAKS,
        "fakes": TokenType.FAKS,

        # functions / returns
        "wasfa": TokenType.WASFA,
        "ya": TokenType.YA,   # alias from BNF
        "raga3": TokenType.RAGA3,

        # if/else
        "law": TokenType.LAW,     # alias from BNF
        "tb law": TokenType.TB_LAW,  # "tb law" is a single keyword for else-if
        "ay haga": TokenType.AY_HAGA,  # "ay haga" is a single keyword for else default case
        "aw": TokenType.AW,      # OR
        "wa": TokenType.WA,      # AND

        # loops
        "khalik": TokenType.KHALIK, #while loop
        "lef": TokenType.LEF,

        # builtins
        "etba3": TokenType.ETBA3,
        "2oly": TokenType.OLY,

        # optional
        "ekhtar": TokenType.EKHTAR,
        "law_kan": TokenType.LAW_KAN,
        "ay_7aga": TokenType.AY_7AGA,
        "taboor": TokenType.TABOOR,
    }

    SINGLE_CHAR = {
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
        ":": TokenType.COLON,
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,   # note: comments handled before emitting
        "=": TokenType.EQUAL,   # == handled before emitting
        "<": TokenType.LESS,    # <= handled before emitting
        ">": TokenType.GREATER, # >= handled before emitting
        "!": TokenType.BANG,    # != handled before emitting
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:           # Main function that converts the whole source code into list of tokens  
        while not self._is_at_end():
            self.start = self.current
            self.start_col = self.column
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _is_at_end(self) -> bool:                # Checks if we reached the end of the source code.
        return self.current >= len(self.source)

    def _advance(self) -> str:                   # Consumes the current character and moves forward.
                                                 # Returns the consumed character.
        ch = self.source[self.current]
        self.current += 1
        self.column += 1
        return ch

    def _peek(self) -> str:                      # Looks at the current character without consuming it.
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:                 # Looks at the next character (current + 1) without consuming it.
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:     # Checks if the current character matches the expected one.
                                                 # If it does, consumes it and returns True. Otherwise, returns False.
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _scan_token(self) -> None:               # Scans the next token from the source code and adds it to the tokens list.
        c = self._advance()

        # whitespace
        if c in " \r\t":
            return
        if c == "\n":
            self.line += 1
            self.column = 1
            return

        # comments or slash
        if c == "/":
            if self._match("/"):
                # single-line comment
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
                return
            if self._match("*"):
                # multi-line comment
                while not self._is_at_end():
                    if self._peek() == "*" and self._peek_next() == "/":
                        self._advance()
                        self._advance()
                        return
                    ch = self._advance()
                    if ch == "\n":
                        self.line += 1
                        self.column = 1
                raise LexerError("Unterminated block comment", self.line, self.column)
            # not a comment: emit SLASH
            self._add(TokenType.SLASH, "/")
            return

        # two-char operators
        if c == "=":
            self._add(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
            return
        if c == "!":
            if self._match("="):
                self._add(TokenType.BANG_EQUAL)
            else:
                self._add(TokenType.BANG)
            return
        if c == "<":
            self._add(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
            return
        if c == ">":
            self._add(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
            return

        # strings
        if c == '"':
            self._string()
            return

        # numbers (int/float)
        if c.isdigit():
            self._number(first_digit_already_consumed=True)
            return

        # identifiers / keywords (allow underscore and leading digit
        if c.isalpha() or c == "_":
            self._identifier()
            return

        # single-char tokens
        if c in self.SINGLE_CHAR:
            self._add(self.SINGLE_CHAR[c], c)
            return

        raise LexerError(f"Unexpected character '{c}'", self.line, self.start_col)

    def _string(self) -> None:
        start_line = self.line
        start_col = self.start_col

        while self._peek() != '"' and not self._is_at_end():
            ch = self._advance()
            if ch == "\n":
                self.line += 1
                self.column = 1

        if self._is_at_end():
            raise LexerError("Unterminated string literal", start_line, start_col)

        # closing quote
        self._advance()

        # lexeme includes quotes; interpreter will strip or keep as needed
        lexeme = self.source[self.start:self.current]
        self._add(TokenType.STRING_LITERAL, lexeme)

    def _number(self, first_digit_already_consumed: bool) -> None:
        # we already consumed first digit
        while self._peek().isdigit():
            self._advance()

        is_float = False
        if self._peek() == "." and self._peek_next().isdigit():
            is_float = True
            self._advance()  # consume '.'
            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start:self.current]
        self._add(TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL, lexeme)

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        ttype = self.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add(ttype, text)

    def _add(self, ttype: TokenType, lexeme: str | None = None) -> None:
        if lexeme is None:
            lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(ttype, lexeme, self.line, self.start_col))