from __future__ import annotations

class InterpreterRuntimeError(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value: object | None) -> None:
        self.value = value
