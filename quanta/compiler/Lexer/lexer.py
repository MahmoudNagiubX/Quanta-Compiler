from __future__ import annotations
from .token import LexerError, Token, TokenType

class Lexer:    # Converts Quanta source code into tokens.
    """ Why we need this:
            - The parser should work with tokens, not raw characters.
            - The lexer groups characters into meaningful units such as:
                    ( identifiers | numbers | strings | operators | keywords ) """

    # Single Word Keywords.
    KEYWORDS = {
        # ===== Types =====
        "rakm": TokenType.RAKM,
        "fatafet": TokenType.FATAFET,
        "kasr": TokenType.FATAFET,       # legacy alias
        "kalam": TokenType.KALAM,
        "ya_ah_ya_la": TokenType.YA_AH_YA_LA,
        "taboor": TokenType.TABOOR,

        # ===== Boolean values =====
        "eshta": TokenType.ESHTA,
        "sa7": TokenType.ESHTA,          # true (arabic)
        "fakes": TokenType.FAKES,
        "ghalat": TokenType.FAKES,       # false (arabic)
        "faks": TokenType.FAKES,         # tolerate old spelling

        # ===== Functions / return =====
        "wasfa": TokenType.WASFA,
        "ya": TokenType.YA,              # old grammar alias
        "raga3": TokenType.RAGA3,
        "fady": TokenType.FADY,

        # ===== Control flow =====
        "law": TokenType.LAW,
        "lw": TokenType.LAW,             # old grammar alias
        "aw": TokenType.AW,
        "wa": TokenType.WA,
        "khalik": TokenType.KHALIK,
        "lef": TokenType.LEF,
        "ekhtar": TokenType.EKHTAR,
        "law_kan": TokenType.LAW_KAN,

        # ===== Builtins =====
        "etba3": TokenType.ETBA3,
        "oly": TokenType.OLY,
        "2oly": TokenType.OLY,           # special alias
    }

    # Multi Word Keywords
    PHRASE_KEYWORDS = (     # These should become one token, not two separate identifiers.
        ("tb law", TokenType.TB_LAW),
        ("tb lw", TokenType.TB_LAW),
        ("aw law", TokenType.TB_LAW),
        ("ay haga", TokenType.AY_HAGA),
        ("ay_7aga", TokenType.AY_HAGA),
        ("tol lma", TokenType.KHALIK),   # old alias for while
    )

    # Single Character Tokens
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
        "/": TokenType.SLASH,
        "=": TokenType.EQUAL,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
        "!": TokenType.BANG,
    }

    INVISIBLE_CHARS = {"\ufeff", "\u200b", "\u200c", "\u200d"}

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.current = 0
        self.line = 1
        self.column = 1
        self.start = 0
        self.start_col = 1

    def tokenize(self) -> list[Token]:  # Scan full source code and return list of tokens.
       
        while not self._is_at_end():
            self.start = self.current
            self.start_col = self.column
            self._scan_token()

        # Add EOF token at the end so parser knows input finished.
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        self.column += 1
        return ch

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:    # Consume next char only if it matches expected.
                                                            # Useful for ==, !=, <=, >= and comments.
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _scan_token(self) -> None:  # Read one token from source.
        c = self._advance()

        # Ignore spaces, tabs, carriage returns.
        if c in " \r\t" or c in self.INVISIBLE_CHARS:
            return

        # Handle new line.
        if c == "\n":
            self.line += 1
            self.column = 1
            return

        # Handle comments and slash operator.
        if c == "/":
            # Single-line comment: // ....
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
                return

            # Block comment: /* ... */
            if self._match("*"):
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

            self._add(TokenType.SLASH, "/")
            return

        # Handle two-character operators.
        if c == "=":
            self._add(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
            return

        if c == "!":
            self._add(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
            return

        if c == "<":
            self._add(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
            return

        if c == ">":
            self._add(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
            return

        # Handle string literals.
        if c == '"':
            self._string()
            return

        # Special case for 2oly before reading normal numbers.
        if c == "2" and self.source[self.start:self.start + 4] == "2oly":
            next_index = self.start + 4
            next_char = self.source[next_index] if next_index < len(self.source) else "\0"

            # Make sure it is actually the full keyword, not part of a bigger word.
            if not (next_char.isalnum() or next_char == "_"):
                self.current = self.start + 4
                self.column = self.start_col + 4
                self._add(TokenType.OLY, "2oly")
                return

        # Handle numbers.
        if c.isdigit():
            self._number()
            return

        # Handle identifiers / keywords.
        if c.isalpha() or c == "_":
            if self._phrase_keyword():
                return
            self._identifier()
            return

        # Handle simple single-character tokens.
        if c in self.SINGLE_CHAR:
            self._add(self.SINGLE_CHAR[c], c)
            return

        # Any other character is invalid.
        raise LexerError(f"Unexpected character '{c}'", self.line, self.start_col)

    def _phrase_keyword(self) -> bool:  # Match multi word keywords like 'tb law' and 'ay haga'.
        # We check these before normal identifiers so they become one token.
        
        remaining = self.source[self.start:]
        for phrase, token_type in self.PHRASE_KEYWORDS:
            if not remaining.startswith(phrase):
                continue

            end_index = self.start + len(phrase)
            next_char = self.source[end_index] if end_index < len(self.source) else "\0"

            # Make sure phrase is not part of a larger identifier.
            if next_char.isalnum() or next_char == "_":
                continue

            self.current = self.start + len(phrase)
            self.column = self.start_col + len(phrase)
            self._add(token_type, phrase)
            return True

        return False

    def _string(self) -> None:  # Read string literal until closing quote.

        start_line = self.line
        start_col = self.start_col
        
        while self._peek() != '"' and not self._is_at_end():
            ch = self._advance()
            if ch == "\n":
                self.line += 1
                self.column = 1

        if self._is_at_end():
            raise LexerError("Unterminated string literal", start_line, start_col)

        # Consume closing quote.
        self._advance()
        self._add(TokenType.STRING_LITERAL, self.source[self.start:self.current])

    def _number(self) -> None:  # Read integer or float literal.

        while self._peek().isdigit():
            self._advance()

        is_float = False

        # If we see dot followed by digit, it is a float.
        if self._peek() == "." and self._peek_next().isdigit():
            is_float = True
            self._advance()  # consume dot

            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start:self.current]
        self._add(TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL, lexeme)

    def _identifier(self) -> None:  # Read identifier or keyword.
        
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        token_type = self.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add(token_type, text)

    def _add(self, token_type: TokenType, lexeme: str | None = None) -> None:   # Add token to token list.
    
        if lexeme is None:
            lexeme = self.source[self.start:self.current]

        self.tokens.append(Token(token_type, lexeme, self.line, self.start_col))