from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen = True)
class QuantaType:   #  Represents one semantic type in Quanta.

    name: str
    def __str__(self) -> str:
        return self.name


# ===== Built In language types =====
RAKM_TYPE = QuantaType("rakm")                 # int
FATAFET_TYPE = QuantaType("fatafet")           # float
KALAM_TYPE = QuantaType("kalam")               # string
YA_AH_YA_LA_TYPE = QuantaType("ya_ah_ya_la")   # bool

# Used when analysis cannot determine a real type.
UNKNOWN_TYPE = QuantaType("<unknown>")

# Optional helper for places where no value is returned.
VOID_TYPE = QuantaType("void")

# Maps source type names to internal semantic types.
TYPE_NAME_MAP = {
    "rakm": RAKM_TYPE,
    "fatafet": FATAFET_TYPE,
    "kalam": KALAM_TYPE,
    "ya_ah_ya_la": YA_AH_YA_LA_TYPE,
}