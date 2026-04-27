from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

class IRInstruction:
    def __str__(self) -> str:
        raise NotImplementedError

@dataclass
class Assign(IRInstruction):
    target: str
    value: str

    def __str__(self) -> str:
        return f"{self.target} = {self.value}"

@dataclass
class BinaryOp(IRInstruction):
    target: str
    left: str
    operator: str
    right: str

    def __str__(self) -> str:
        return f"{self.target} = {self.left} {self.operator} {self.right}"

@dataclass
class Print(IRInstruction):
    value: str

    def __str__(self) -> str:
        return f"PRINT {self.value}"

@dataclass
class Label(IRInstruction):
    name: str

    def __str__(self) -> str:
        return f"label {self.name}"

@dataclass
class Goto(IRInstruction):
    label: str

    def __str__(self) -> str:
        return f"goto {self.label}"

@dataclass
class IfGoto(IRInstruction):
    condition: str
    label: str

    def __str__(self) -> str:
        return f"if {self.condition} goto {self.label}"

@dataclass
class Call(IRInstruction):
    target: str | None
    function_name: str
    arguments: list[str]

    def __str__(self) -> str:
        args = ", ".join(self.arguments)
        if self.target is None:
            return f"call {self.function_name}({args})"
        return f"{self.target} = call {self.function_name}({args})"

@dataclass
class Return(IRInstruction):
    value: str | None = None

    def __str__(self) -> str:
        if self.value is None:
            return "return"
        return f"return {self.value}"
