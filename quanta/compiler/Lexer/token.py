from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):  # Token kinds produced by the lexer.
    
    """ This is the contract between lexer and parser.
        Every token used by the lexer must be defined here. """

    # ===== Keywords / language types =====
    RAKM = auto()            # integer type
    FATAFET = auto()         # float type
    KALAM = auto()           # string type
    YA_AH_YA_LA = auto()     # boolean type

    # ===== Boolean values =====
    ESHTA = auto()           # true
    FAKES = auto()           # false

    # ===== Function / return =====
    WASFA = auto()           # function keyword
    YA = auto()              # legacy function keyword
    RAGA3 = auto()           # return

    # ===== Control flow =====
    LAW = auto()             # if
    TB_LAW = auto()          # else if
    AY_HAGA = auto()         # else
    AW = auto()              # logical OR
    WA = auto()              # logical AND
    KHALIK = auto()          # while
    LEF = auto()             # for
    EKHTAR = auto()          # switch
    LAW_KAN = auto()         # case

    # ===== Builtins / helpers =====
    ETBA3 = auto()           # print
    OLY = auto()             # input
    TABOOR = auto()          # array

    # ===== Single-character tokens =====
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    COMMA = auto()           # ,
    SEMICOLON = auto()       # ;
    COLON = auto()           # :

    # ===== Operators =====
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    SLASH = auto()           # /
    EQUAL = auto()           # =
    EQUAL_EQUAL = auto()     # ==
    BANG = auto()            # !
    BANG_EQUAL = auto()      # !=
    LESS = auto()            # <
    LESS_EQUAL = auto()      # <=
    GREATER = auto()         # >
    GREATER_EQUAL = auto()   # >=

    # ===== Literals =====
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()

    # ===== End of file =====
    EOF = auto()

@dataclass(frozen = True) # Represents one token in source code.
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

class LexerError(Exception):    # Error raised when lexer finds invalid source text.
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError: {message} at line {line}, column {column}")
        self.line = line
        self.column = column