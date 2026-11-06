from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
@dataclass(frozen=True,slots=True)
class Unit:
 symbol:str
 name:str
 category:str
 base_symbol:str
 scale:Fraction
