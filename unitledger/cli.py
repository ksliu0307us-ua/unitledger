from __future__ import annotations
import argparse,json,sys
from collections.abc import Sequence
from pathlib import Path
from . import __version__
from .checks import CheckFileError,load_cases,run_checks
from .conversion import convert_text
from .formatting import format_fraction
from .numeric import NumberError
from .units import CATEGORIES,UnitError,get_unit,list_units
def _precision(v):
 try:n=int(v)
 except ValueError as e:raise argparse.ArgumentTypeError("must be an integer") from e
 if not 1<=n<=100:raise argparse.ArgumentTypeError("must be from 1 to 100")
 return n
def _parser():
 p=argparse.ArgumentParser(prog="unitledger",description="Exact fixed-registry unit conversions and expectation checks.");p.add_argument("--version",action="version",version=f"%(prog)s {__version__}");s=p.add_subparsers(dest="command",required=True)
 c=s.add_parser("convert");c.add_argument("--value",required=True);c.add_argument("--from",dest="source",required=True);c.add_argument("--to",dest="target",required=True);c.add_argument("--precision",type=_precision,default=28);c.add_argument("--format",choices=("text","json"),default="text")
 u=s.add_parser("units");u.add_argument("--category",choices=CATEGORIES);u.add_argument("--format",choices=("text","json"),default="text")
 t=s.add_parser("table");t.add_argument("--value",action="append",required=True);t.add_argument("--from",dest="source",required=True);t.add_argument("--to",dest="targets",action="append",required=True);t.add_argument("--precision",type=_precision,default=28);t.add_argument("--format",choices=("text","json"),default="text")
 k=s.add_parser("check");k.add_argument("file",type=Path);k.add_argument("--precision",type=_precision,default=28);k.add_argument("--format",choices=("text","json"),default="text")
 return p
def main(argv:Sequence[str]|None=None)->int:
 a=_parser().parse_args(argv)
 try:
  if a.command=="units":
   values=[{"symbol":u.symbol,"name":u.name,"category":u.category,"base_unit":u.base_symbol,"scale_numerator":str(u.scale.numerator),"scale_denominator":str(u.scale.denominator)} for u in list_units(a.category)]
   if a.format=="json":print(json.dumps(values,ensure_ascii=False,indent=2))
   else:
    for u in values:print(f"{u['symbol']}\t{u['category']}\t{u['name']}\tbase={u['base_unit']} scale={u['scale_numerator']}/{u['scale_denominator']}")
   return 0
  if a.command=="convert":
   result=convert_text(a.value,a.source,a.target);display=format_fraction(result,a.precision);category=get_unit(a.source).category;data={"value":a.value,"from":a.source,"to":a.target,"category":category,"result":display,"precision":a.precision}
   print(json.dumps(data,ensure_ascii=False,indent=2) if a.format=="json" else f"{a.value} {a.source} = {display} {a.target}");return 0
  if a.command=="table":
   source=get_unit(a.source)
   for target in a.targets:
    if get_unit(target).category!=source.category:raise UnitError(f"incompatible destination unit: {target!r}")
   rows=[{"value":v,"conversions":[{"to":t,"result":format_fraction(convert_text(v,a.source,t),a.precision)} for t in a.targets]} for v in a.value]
   if a.format=="json":print(json.dumps({"from":a.source,"precision":a.precision,"rows":rows},ensure_ascii=False,indent=2))
   else:
    print("value\t"+"\t".join(a.targets))
    for r in rows:print(r["value"]+"\t"+"\t".join(x["result"] for x in r["conversions"]))
   return 0
  cases=load_cases(a.file);results=run_checks(cases);data=[{"id":r.case.id,"passed":r.passed,"actual":format_fraction(r.actual,a.precision),"expected":r.case.expected,"tolerance":r.case.tolerance,"difference":format_fraction(r.difference,a.precision)} for r in results]
  if a.format=="json":print(json.dumps({"passed":sum(x["passed"] for x in data),"failed":sum(not x["passed"] for x in data),"cases":data},indent=2))
  else:
   for r in data:print(f"{'PASS' if r['passed'] else 'FAIL'} {r['id']}: actual={r['actual']} expected={r['expected']} tolerance={r['tolerance']}")
  return 0 if all(r.passed for r in results) else 1
 except (NumberError,UnitError,CheckFileError,OSError,ValueError) as e:print(f"error: {e}",file=sys.stderr);return 2
