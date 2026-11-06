from __future__ import annotations
from fractions import Fraction as F
from .models import Unit
_DATA=[
 Unit("mm","millimetre","length","m",F(1,1000)),Unit("cm","centimetre","length","m",F(1,100)),Unit("m","metre","length","m",F(1)),Unit("km","kilometre","length","m",F(1000)),Unit("in","international inch","length","m",F(127,5000)),Unit("ft","international foot","length","m",F(381,1250)),
 Unit("mg","milligram","mass","kg",F(1,1000000)),Unit("g","gram","mass","kg",F(1,1000)),Unit("kg","kilogram","mass","kg",F(1)),
 Unit("us","microsecond","duration","s",F(1,1000000)),Unit("ms","millisecond","duration","s",F(1,1000)),Unit("s","second","duration","s",F(1)),Unit("min","minute","duration","s",F(60)),Unit("h","hour","duration","s",F(3600)),Unit("d","fixed 86400-second day","duration","s",F(86400)),
 Unit("bit","bit","data_size","B",F(1,8)),Unit("B","byte","data_size","B",F(1)),Unit("kB","decimal kilobyte","data_size","B",F(1000)),Unit("MB","decimal megabyte","data_size","B",F(1000000)),Unit("GB","decimal gigabyte","data_size","B",F(1000000000)),Unit("KiB","binary kibibyte","data_size","B",F(1024)),Unit("MiB","binary mebibyte","data_size","B",F(1048576)),Unit("GiB","binary gibibyte","data_size","B",F(1073741824)),
]
UNITS={u.symbol:u for u in _DATA};CATEGORIES=("length","mass","duration","data_size")
class UnitError(ValueError):pass
def get_unit(symbol:str)->Unit:
 try:return UNITS[symbol]
 except KeyError:raise UnitError(f"unsupported unit symbol: {symbol!r}") from None
def list_units(category:str|None=None)->tuple[Unit,...]:
 if category is not None and category not in CATEGORIES:raise UnitError(f"unsupported category: {category!r}")
 return tuple(u for u in _DATA if category is None or u.category==category)
