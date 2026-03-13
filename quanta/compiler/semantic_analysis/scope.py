from __future__ import annotations
from typing import Dict, Optional
from .symbols import Symbol

class Scope: # Lexical scope used during semantic analysis.
    """
    Example:
        global scope
          -> function scope
              -> block scope"""

    def __init__(self, name: str, parent: Optional["Scope"] = None) -> None:
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> bool:   # Add symbol to current scope only.
            # Returns False if symbol already exists in this scope.
        if symbol.name in self.symbols:
            return False

        self.symbols[symbol.name] = symbol
        return True

    def lookup_local(self, name: str) -> Optional[Symbol]: # Search only in current scope
        return self.symbols.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:    # Search current scope, then parent scopes.
        scope: Optional[Scope] = self

        while scope is not None:
            symbol = scope.lookup_local(name)
            if symbol is not None:
                return symbol
            scope = scope.parent
        return None