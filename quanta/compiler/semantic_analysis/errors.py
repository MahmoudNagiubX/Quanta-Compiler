'''
Defines semantic errors produced during semantic analysis.
'''

from dataclasses import dataclass

''' Represents a semantic error detected during analysis.

      Example errors:
      - undeclared variable
      - type mismatch
      - invalid return type
       - duplicate declaration
'''
@dataclass
class SemanticError:        
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"SemanticError: {self.message} at line {self.line}, column {self.column}"