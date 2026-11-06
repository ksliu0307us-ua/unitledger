from __future__ import annotations
from fractions import Fraction
from .numeric import parse_number
from .units import UnitError,get_unit
def convert_fraction(value:Fraction,source:str,target:str)->Fraction:
 a=get_unit(source);b=get_unit(target)
 if a.category!=b.category:raise UnitError(f"incompatible unit categories: {a.category} and {b.category}")
 return value*a.scale/b.scale
def convert_text(value:str,source:str,target:str)->Fraction:return convert_fraction(parse_number(value),source,target)
