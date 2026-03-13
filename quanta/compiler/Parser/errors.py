class ParseError(Exception):    # Raised when parser finds invalid syntax.
    
    def __init__(self, message: str, line: int | None = None, column: int | None = None):
        self.message = message
        self.line = line
        self.column = column

        if line is not None and column is not None:
            super().__init__(f"ParseError: {message} at line {line}, column {column}")
        else:
            super().__init__(f"ParseError: {message}")