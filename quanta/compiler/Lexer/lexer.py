from .token import TokenType, Token, LexerError
 
class Lexer:
    KEYWORDS = {
        "hewar": TokenType.HEWAR,               
        "law": TokenType.LAW,                   
        "ya_emah": TokenType.YA_EMAH,           
        "laff": TokenType.LAFF,                 
        "sam3na": TokenType.SAM3NA,           
        "rkm": TokenType.TYPE_RKM,              
        "ya_ah_ya_la": TokenType.TYPE_YA_AH_YA_LA, 
        "eshta": TokenType.BOOL_ESHTA,          
        "faks": TokenType.BOOL_FAKS,      
    }

    SINGLE_CHAR_TOKENS = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.STAR,
        '/': TokenType.SLASH,
        '=': TokenType.EQUAL,
        '<': TokenType.LESS,
        '>': TokenType.GREATER,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _match(self, expected):
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _scan_token(self):
        c = self._advance()

        # Skip whitespace
        if c in ' \r\t':
            return
        if c == '\n':
            self.line += 1
            self.column = 1
            return

        # Operators (multi-character first)
        if c == '=':
            if self._match('='):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
            return
        if c == '!':
            if self._match('='):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                raise LexerError("Unexpected '!'", self.line, self.column)
            return
        if c == '<':
            if self._match('='):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
            return
        if c == '>':
            if self._match('='):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
            return
        if c == '&':
            if self._match('&'):
                self._add_token(TokenType.AND_AND)
            else:
                raise LexerError("Unexpected '&'", self.line, self.column)
            return
        if c == '|':
            if self._match('|'):
                self._add_token(TokenType.OR_OR)
            else:
                raise LexerError("Unexpected '|'", self.line, self.column)
            return
        if c == '-':
            if self._match('>'):
                self._add_token(TokenType.ARROW)
                return

        # Single character tokens
        if c in self.SINGLE_CHAR_TOKENS:
            self._add_token(self.SINGLE_CHAR_TOKENS[c])
            return

        # Number literals
        if c.isdigit():
            self._number()
            return

        # Identifiers or keywords
        if c.isalpha() or c == '_':
            self._identifier()
            return

        # Unknown character
        raise LexerError(f"Unexpected character '{c}'", self.line, self.column)

    def _number(self):
        start_column = self.column - 1
        while self._peek().isdigit():
            self._advance()
        value = self.source[self.start:self.current]
        self._add_token(TokenType.INT_LITERAL, value, start_column)

    def _identifier(self):
        start_column = self.column - 1
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        text = self.source[self.start:self.current]
        token_type = self.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(token_type, text, start_column)

    def _add_token(self, type_, lexeme=None, column=None):
        if lexeme is None:
            lexeme = self.source[self.start:self.current]
        if column is None:
            column = self.column - len(lexeme)
        self.tokens.append(Token(type_, lexeme, self.line, column))
