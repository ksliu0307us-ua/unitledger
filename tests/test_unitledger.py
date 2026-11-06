import json,os,subprocess,sys,tempfile,unittest
from decimal import getcontext
from fractions import Fraction
from pathlib import Path
from unitledger.checks import CheckFileError,load_cases,run_checks
from unitledger.conversion import convert_fraction,convert_text
from unitledger.formatting import format_fraction
from unitledger.numeric import parse_number
from unitledger.units import UnitError,get_unit,list_units

class ConversionTests(unittest.TestCase):
 def test_categories_known_and_identity(self):
  known=[("1","m","cm",100),("1","kg","g",1000),("1","h","s",3600),("1","B","bit",8)]
  for value,a,b,expected in known:self.assertEqual(convert_text(value,a,b),expected)
  for symbol in ("mm","kg","us","GiB"):self.assertEqual(convert_text("-2.5",symbol,symbol),Fraction(-5,2))
 def test_exact_roundtrip_and_chain(self):
  v=Fraction(7,3);feet=convert_fraction(v,"m","ft");self.assertEqual(convert_fraction(feet,"ft","m"),v);self.assertEqual(convert_fraction(convert_fraction(v,"m","cm"),"cm","mm"),convert_fraction(v,"m","mm"))
 def test_nonterminating_precision_half_even(self):
  self.assertTrue(format_fraction(convert_text("1","m","ft"),12).startswith("3.280839"));self.assertEqual(format_fraction(Fraction(125,100),2),"1.2");self.assertEqual(format_fraction(Fraction(135,100),2),"1.4")
 def test_negative_zero_small_large(self):
  self.assertEqual(format_fraction(Fraction(0),5),"0");self.assertEqual(format_fraction(parse_number("-0"),5),"0");self.assertEqual(convert_text("1e-20","m","mm"),Fraction(1,10**17));self.assertEqual(convert_text("1e20","kB","B"),10**23)
 def test_decimal_context_preserved(self):
  before=getcontext().copy();format_fraction(Fraction(1,3),100);after=getcontext();self.assertEqual((after.prec,after.rounding,after.Emin,after.Emax,after.capitals,after.clamp,dict(after.flags),dict(after.traps)),(before.prec,before.rounding,before.Emin,before.Emax,before.capitals,before.clamp,dict(before.flags),dict(before.traps)))
 def test_case_bits_prefixes(self):
  self.assertEqual(convert_text("1","B","bit"),8);self.assertEqual(convert_text("1","kB","B"),1000);self.assertEqual(convert_text("1","KiB","B"),1024)
  for s in ("kb","KIB","meter","M"):
   with self.assertRaises(UnitError):get_unit(s)
 def test_cross_category(self):
  with self.assertRaises(UnitError):convert_text("1","m","kg")
 def test_invalid_numbers(self):
  for x in ("NaN","Infinity","-inf","1,000","1_000","","."):
   with self.assertRaises(ValueError):parse_number(x)

class CheckTests(unittest.TestCase):
 def write(self,data):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)/"c.json";p.write_text(json.dumps(data),encoding="utf-8");return p
 def tearDown(self):
  if hasattr(self,"tmp"):self.tmp.cleanup()
 def test_tolerance_boundary(self):
  p=self.write({"schema_version":1,"cases":[{"id":"edge","value":"1","from":"m","to":"cm","expected":"99","tolerance":"1"},{"id":"fail","value":"1","from":"m","to":"cm","expected":"98.999","tolerance":"1"}]});r=run_checks(load_cases(p));self.assertTrue(r[0].passed);self.assertFalse(r[1].passed)
 def test_independent_of_display_rounding(self):
  p=self.write({"schema_version":1,"cases":[{"id":"rounded","value":"1","from":"m","to":"ft","expected":"3.28"}]});self.assertFalse(run_checks(load_cases(p))[0].passed);self.assertEqual(format_fraction(convert_text("1","m","ft"),3),"3.28")
 def test_malformed_duplicate_ids_negative_tolerance_and_duplicate_json(self):
  bad=[{"schema_version":1,"cases":[{"id":"x","value":"1","from":"m","to":"cm","expected":"100"},{"id":"x","value":"1","from":"m","to":"cm","expected":"100"}]},{"schema_version":1,"cases":[{"id":"x","value":"1","from":"m","to":"cm","expected":"100","tolerance":"-1"}]},{"schema_version":1,"cases":[{"id":"x","value":1,"from":"m","to":"cm","expected":"100"}]}]
  for data in bad:
   p=self.write(data)
   with self.assertRaises(CheckFileError):load_cases(p)
   self.tmp.cleanup();del self.tmp
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)/"d";p.write_text('{"schema_version":1,"schema_version":1,"cases":[]}')
  with self.assertRaises(CheckFileError):load_cases(p)

class CliTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.file=self.root/"c.json";self.file.write_text(json.dumps({"schema_version":1,"cases":[{"id":"ok","value":"1","from":"MiB","to":"B","expected":"1048576"}]}));env=os.environ.copy();src=Path(__file__).resolve().parents[1];env["PYTHONPATH"]=str(src)+((os.pathsep+env["PYTHONPATH"]) if env.get("PYTHONPATH") else "");self.env=env
 def tearDown(self):self.tmp.cleanup()
 def run_cli(self,*a):return subprocess.run([sys.executable,"-m","unitledger",*map(str,a)],cwd=self.root,env=self.env,text=True,capture_output=True)
 def test_commands_order_json_exit_and_readonly(self):
  self.assertEqual(self.run_cli("convert","--value","1","--from","MiB","--to","B","--format","json").returncode,0);self.assertEqual(self.run_cli("units","--format","json").returncode,0);table=json.loads(self.run_cli("table","--value","1","--value","2.5","--from","m","--to","cm","--to","mm","--format","json").stdout);self.assertEqual([r["value"] for r in table["rows"]],["1","2.5"]);self.assertEqual([x["to"] for x in table["rows"][0]["conversions"]],["cm","mm"]);before=self.file.read_bytes();self.assertEqual(self.run_cli("check",self.file,"--format","json").returncode,0);self.assertEqual(self.file.read_bytes(),before);self.assertEqual(self.run_cli("convert","--value","1","--from","m","--to","kg").returncode,2)

if __name__=="__main__":unittest.main()
