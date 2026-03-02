from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):  # 1️⃣ Token Types
    # Keywords
    HEWAR = auto()
    LAW = auto()
    YA_EMAH = auto()
    LAFF = auto()
    SAM3NA = auto()
    TYPE_RKM = auto()
    TYPE_YA_AH_YA_LA = auto()
    BOOL_ESHTA = auto()
    BOOL_FAKS = auto()

    # Literals
    INT_LITERAL = auto()

    # Identifier
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    AND_AND = auto()
    OR_OR = auto()
    ARROW = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    # Special
    EOF = auto()
    
# 2️⃣ Token Class
@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int 
    
# 3️⃣ Lexer Error
class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"LexerError: {message} at line {line}, column {column}")
        self.line = line
        self.column = column