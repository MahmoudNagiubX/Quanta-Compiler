from __future__ import annotations
from .ir_instruction import Assign, BinaryOp, IRInstruction, Call, IfGoto, Print, Return

class IROptimizer:
    def optimize(self, instructions: list[IRInstruction]) -> list[IRInstruction]:
        folded = self._constant_fold(instructions)
        return self._dead_code_eliminate(folded)

    def _constant_fold(self, instructions: list[IRInstruction]) -> list[IRInstruction]:
        optimized: list[IRInstruction] = []
        constants: dict[str, int | float] = {}

        for instr in instructions:
            if isinstance(instr, BinaryOp):
                folded = self._fold_binary(instr, constants)
                optimized.append(folded)
                if isinstance(folded, Assign) and self._is_temp(folded.target):
                    const_value = self._resolve_constant(folded.value, constants)
                    if const_value is not None:
                        constants[folded.target] = const_value
                else:
                    if self._is_temp(instr.target):
                        constants.pop(instr.target, None)
                continue

            if isinstance(instr, Assign):
                const_value = self._resolve_constant(instr.value, constants)
                if self._is_temp(instr.target) and const_value is not None:
                    constants[instr.target] = const_value
                elif self._is_temp(instr.target):
                    constants.pop(instr.target, None)
                optimized.append(instr)
                continue

            optimized.append(instr)

        return optimized

    def _dead_code_eliminate(self, instructions: list[IRInstruction]) -> list[IRInstruction]:
        used_vars: set[str] = set()
        optimized: list[IRInstruction] = []

        for instr in reversed(instructions):
            if isinstance(instr, (Assign, BinaryOp)):
                if instr.target in used_vars:
                    optimized.append(instr)
                    used_vars.update(self._read_operands(instr))
                else:
                    continue
            else:
                optimized.append(instr)
                used_vars.update(self._read_operands(instr))

        return list(reversed(optimized))

    def _read_operands(self, instr: IRInstruction) -> set[str]:
        reads: set[str] = set()

        if isinstance(instr, Assign):
            self._add_operand(reads, instr.value)
        elif isinstance(instr, BinaryOp):
            self._add_operand(reads, instr.left)
            self._add_operand(reads, instr.right)
        elif isinstance(instr, Print):
            self._add_operand(reads, instr.value)
        elif isinstance(instr, IfGoto):
            self._add_operand(reads, instr.condition)
        elif isinstance(instr, Call):
            for arg in instr.arguments:
                self._add_operand(reads, arg)
        elif isinstance(instr, Return):
            if instr.value is not None:
                self._add_operand(reads, instr.value)

        return reads

    def _add_operand(self, reads: set[str], operand: str) -> None:
        if self._is_constant(operand):
            return
        reads.add(operand)

    def _fold_binary(self, instr: BinaryOp, constants: dict[str, int | float]) -> IRInstruction:
        left_value = self._resolve_constant(instr.left, constants)
        right_value = self._resolve_constant(instr.right, constants)

        if left_value is None or right_value is None:
            return instr

        result = self._evaluate(instr.operator, left_value, right_value)
        if result is None:
            return instr

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return Assign(instr.target, str(result))

    def _resolve_constant(self, operand: str, constants: dict[str, int | float]) -> int | float | None:
        if operand in constants:
            return constants[operand]
        return self._parse_constant(operand)

    def _parse_constant(self, operand: str) -> int | float | None:
        try:
            if "." in operand:
                return float(operand)
            return int(operand)
        except ValueError:
            return None

    def _is_constant(self, operand: str) -> bool:
        return self._parse_constant(operand) is not None

    def _evaluate(self, operator: str, left: int | float, right: int | float) -> int | float | None:
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == 0:
                return None
            return left / right
        return None

    def _is_temp(self, name: str) -> bool:
        return name.startswith("t") and name[1:].isdigit()
