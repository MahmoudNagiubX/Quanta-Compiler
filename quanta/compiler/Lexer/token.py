from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # --- Keywords / types
    RAKM = auto()            # int
    FATAFET = auto()         # float
    KALAM = auto()           # string
    YA_AH_YA_LA = auto()     # ya_ah_ya_la
    ESHTA = auto()           # true
    FAKES = auto()           # false (fakes)
    WASFA = auto()           # function
    RAGA3 = auto()           # return
    LAW = auto()             # if (also supports lw)
    TB_LAW = auto()          # else-if prefix: tb law
    AY_HAGA = auto()         # else default case: ay haga
    AW = auto()              # logical OR (context decides)
    WA = auto()              # logical AND
    KHALIK = auto()          # while (also supports tol lma)
    LEF = auto()             # for
    ETBA3 = auto()           # print
    OLY = auto()             # input

    # Optional (spec mentions switch/arrays; parser/runtime can add later)
    EKHTAR = auto()          # switch
    LAW_KAN = auto()         # case
    TABOOR = auto()          # arrays

    
    
    # --- Single-character tokens
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()

    # --- One or two character tokens
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # --- Literals
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()

    
    
# 2️⃣ Token Class
@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError: {message} at line {line}, column {column}")
        self.line = line
        self.column = column