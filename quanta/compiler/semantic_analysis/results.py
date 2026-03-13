from dataclasses import dataclass, field
from typing import List
from .errors import SemanticError

@dataclass
class SemanticResult:   # Final result of semantic analysis.
        # Stores all semantic errors.
    errors: List[SemanticError] = field(default_factory=list)

    def add_error(self, message: str, line: int, column: int) -> None:
        self.errors.append(SemanticError(message, line, column))

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0