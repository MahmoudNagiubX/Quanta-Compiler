from dataclasses import dataclass

@dataclass
class SemanticError:    # Represents one semantic error found during analysis.
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"SemanticError: {self.message} at line {self.line}, column {self.column}"