from __future__ import annotations
import re
from decimal import Decimal,InvalidOperation
from fractions import Fraction
_NUMBER=re.compile(r"\A[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
class NumberError(ValueError):pass
def parse_number(text:str)->Fraction:
 if not isinstance(text,str) or not _NUMBER.fullmatch(text):raise NumberError(f"invalid decimal number: {text!r}")
 try:value=Decimal(text)
 except InvalidOperation as e:raise NumberError(f"invalid decimal number: {text!r}") from e
 if not value.is_finite():raise NumberError("NaN and infinity are not supported")
 return Fraction(value)
def validate_precision(value:int)->int:
 if not isinstance(value,int) or isinstance(value,bool) or not 1<=value<=100:raise NumberError("precision must be an integer from 1 to 100")
 return value
