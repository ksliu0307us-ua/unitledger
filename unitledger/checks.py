from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .conversion import convert_text
from .numeric import parse_number
from .units import get_unit,UnitError
@dataclass(frozen=True,slots=True)
class CheckCase:
 id:str;value:str;source:str;target:str;expected:str;tolerance:str
@dataclass(frozen=True,slots=True)
class CheckResult:
 case:CheckCase;passed:bool;actual:object;difference:object
class CheckFileError(Exception):pass
class _Duplicate(ValueError):pass
def _strict(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise _Duplicate(f"duplicate JSON key {k!r}")
  d[k]=v
 return d
def load_cases(path:Path)->tuple[CheckCase,...]:
 try:text=path.read_text(encoding="utf-8")
 except (OSError,UnicodeError) as e:raise CheckFileError(f"cannot read check file {path}: {e}") from e
 try:data=json.loads(text,object_pairs_hook=_strict)
 except (_Duplicate,json.JSONDecodeError) as e:raise CheckFileError(f"invalid check JSON: {e}") from e
 if not isinstance(data,dict) or set(data)!={"schema_version","cases"}:raise CheckFileError("check file must contain only schema_version and cases")
 if data["schema_version"]!=1 or isinstance(data["schema_version"],bool):raise CheckFileError("unsupported schema_version")
 if not isinstance(data["cases"],list):raise CheckFileError("cases must be an array")
 out=[];ids=set();required={"id","value","from","to","expected"};allowed=required|{"tolerance"}
 for i,raw in enumerate(data["cases"]):
  if not isinstance(raw,dict) or not required<=set(raw) or set(raw)-allowed:raise CheckFileError(f"cases[{i}] has missing, unknown, or invalid fields")
  if not all(isinstance(raw[k],str) for k in required) or ("tolerance" in raw and not isinstance(raw["tolerance"],str)):raise CheckFileError(f"cases[{i}] values must be strings")
  if not raw["id"] or raw["id"] in ids:raise CheckFileError(f"duplicate or empty case ID: {raw['id']!r}")
  ids.add(raw["id"]);tol=raw.get("tolerance","0")
  try:
   parse_number(raw["value"]);expected=parse_number(raw["expected"]);tolerance=parse_number(tol);actual=convert_text(raw["value"],raw["from"],raw["to"])
  except (ValueError,UnitError) as e:raise CheckFileError(f"cases[{i}] {e}") from e
  if tolerance<0:raise CheckFileError(f"cases[{i}] tolerance must be nonnegative")
  out.append(CheckCase(raw["id"],raw["value"],raw["from"],raw["to"],raw["expected"],tol))
 return tuple(out)
def run_checks(cases):
 return tuple(CheckResult(c,abs((a:=convert_text(c.value,c.source,c.target))-parse_number(c.expected))<=parse_number(c.tolerance),a,abs(a-parse_number(c.expected))) for c in cases)
