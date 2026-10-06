import ast,re
from dataclasses import dataclass,field
@dataclass
class State:
 java:str;rules:list=field(default_factory=list);python_code:str="";errors:list=field(default_factory=list);attempts:int=0;status:str="new"
def extract(java):
 out=[]
 for m in re.finditer(r"if\s*\((\w+)\s*(>=|<=|>|<|==)\s*([0-9.]+)\)\s*return\s+([^;]+);",java):out.append({"kind":"branch","var":m.group(1),"cmp":m.group(2),"boundary":m.group(3),"expr":m.group(4)})
 rs=re.findall(r"return\s+([^;]+);",java)
 if rs:out.append({"kind":"return","expr":rs[-1]})
 return out
def translate(s):
 b=next((x for x in s.rules if x["kind"]=="branch"),None);f=next((x for x in reversed(s.rules) if x["kind"]=="return"),{"expr":"x"})
 cv=lambda e:re.sub(r"([0-9]+\.[0-9]+)",r'Decimal("\1")',e)
 x=["from decimal import Decimal","","def business_rule(x):","    x=Decimal(str(x))"]
 if b:x += [f'    if x {b["cmp"]} Decimal("{b["boundary"]}"):',f'        return {cv(b["expr"])}']
 x += [f'    return {cv(f["expr"])}'];s.python_code="\n".join(x);return s
def check(s):
 t=ast.parse(s.python_code);expected=sum(x["kind"]=="branch" for x in s.rules)
 if sum(isinstance(n,ast.Compare) for n in ast.walk(t))!=expected:s.errors.append("boundary mismatch")
 if "Decimal" not in s.python_code:s.errors.append("precision guard")
 return s
def reflect(s):
 s.attempts+=1;s.status="repair" if s.errors and s.attempts<2 else ("done" if not s.errors else "needs_review");return s
def graph_spec():return ["extract","translate","ast_check","generate_tests","docker_validate","reflect"]
