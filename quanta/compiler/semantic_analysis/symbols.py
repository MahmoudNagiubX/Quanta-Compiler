'''
Symbols represent named entities in the program such as:

- variables
- function parameters
- functions
'''

from dataclasses import dataclass, field
from typing import List

from types import QuantaType


@dataclass
class Symbol:        # Base class for all symbols stored in scopes.
    name: str
    type: QuantaType
    line: int
    column: int


@dataclass
class VariableSymbol(Symbol):  # Represents a variable declaration.
    pass


@dataclass
class ParameterSymbol(Symbol):   # Represents a function parameter.
    pass


@dataclass
class FunctionSymbol(Symbol):    # Represents a function definition.
    parameters: List[ParameterSymbol] = field(default_factory=list)
