'''
Collects semantic errors produced during analysis.

'''
from dataclasses import dataclass, field
from typing import List
from .errors import SemanticError

@dataclass
class SemanticResult:
    """
    Result of semantic analysis.

    Stores a list of semantic errors.
    """
    errors: List[SemanticError] = field(default_factory=list)

    def add_error(self, message: str, line: int, column: int) -> None:  # Add a semantic error to the result.
        self.errors.append(SemanticError(message, line, column))

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0   # Returns True if no semantic errors occurred.