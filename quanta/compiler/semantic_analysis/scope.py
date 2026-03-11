'''
Implements lexical scopes used during semantic analysis.
global
 └── function scope
      └── block scope
'''


from __future__ import annotations
from typing import Dict, Optional
from .symbols import Symbol


class Scope:
    def __init__(self, name: str, parent: Optional["Scope"] = None) -> None:
        self.name = name             # Create a new scope.
        self.parent = parent                      
        self.symbols: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:          # Add a symbol to the current scope.
            return False                         # Returns False if the symbol already exists in this scope.
        self.symbols[symbol.name] = symbol
        return True

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)             # Search for a symbol only in this scope.

    def lookup(self, name: str) -> Optional[Symbol]:
        scope: Optional[Scope] = self
        while scope is not None:                  # Search for a symbol starting from this scope
                                                  # and walking up through parent scopes.
            symbol = scope.lookup_local(name)
            if symbol is not None:
                return symbol
            scope = scope.parent
        return None