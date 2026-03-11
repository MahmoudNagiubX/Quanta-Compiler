'''
This module defines the type system used by the Quanta language.

A type represents the kind of value an expression or variable can hold.
Examples: num, flag.

'''

from dataclasses import dataclass

@dataclass(frozen=True)
class QuantaType:
    name: str

    def __str__(self) -> str:      
                                #Return the human-readable name of the type.
        return self.name

# Integer type
NUM_TYPE = QuantaType("num")

# Boolean type
FLAG_TYPE = QuantaType("flag")

# This prevents cascading errors.
UNKNOWN_TYPE = QuantaType("<unknown>")

# Maps type names from source code to internal type objects.
TYPE_NAME_MAP = {
    "num": NUM_TYPE,
    "flag": FLAG_TYPE,
    "<unknown>": UNKNOWN_TYPE
}