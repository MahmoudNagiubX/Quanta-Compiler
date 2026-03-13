from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .type import QuantaType, UNKNOWN_TYPE

@dataclass
class Symbol:   # Base symbol stored inside scopes.
    name: str
    type: QuantaType
    line: int
    column: int

@dataclass
class VariableSymbol(Symbol):
    """ Symbol for local/global variables """
    pass

@dataclass
class ParameterSymbol(Symbol):
    """ Symbol for function parameters """
    pass

@dataclass
class FunctionSymbol(Symbol):   # Symbol for functions
    parameters: List[ParameterSymbol] = field(default_factory=list)

    def __init__(
        self,
        name: str,
        line: int,
        column: int,
        parameters: List[ParameterSymbol] | None = None,
        type: QuantaType = UNKNOWN_TYPE,
    ):
        super().__init__(name=name, type=type, line=line, column=column)
        self.parameters = parameters or []