from __future__ import annotations
from decimal import Decimal,ROUND_HALF_EVEN,localcontext
from fractions import Fraction
from .numeric import validate_precision
def format_fraction(value:Fraction,precision:int=28)->str:
 validate_precision(precision)
 if value==0:return "0"
 with localcontext() as c:
  c.prec=max(precision+25,125);d=Decimal(value.numerator)/Decimal(value.denominator);adjusted=d.adjusted()
 with localcontext() as c:
  c.prec=max(precision+10,adjusted+precision+10 if adjusted>=0 else precision+10);q=Decimal(1).scaleb(adjusted-precision+1);rounded=d.quantize(q,rounding=ROUND_HALF_EVEN);text=format(rounded,"f")
 if "." in text:text=text.rstrip("0").rstrip(".")
 return "0" if Decimal(text)==0 else text
