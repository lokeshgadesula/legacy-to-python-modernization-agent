from modernizer.core import *
J="public double price(double x){ if (x >= 100) return x * 0.90; return x; }"
def test_extract():assert extract(J)[0]["boundary"]=="100"
def test_compile():s=State(J,extract(J));translate(s);compile(s.python_code,"x","exec")
def test_precision():s=State(J,extract(J));translate(s);check(s);assert not s.errors and 'Decimal("0.90")' in s.python_code
def test_graph():assert graph_spec()==["extract","translate","ast_check","generate_tests","docker_validate","reflect"]
def test_reflect():s=State(J,errors=["x"]);reflect(s);assert s.status=="repair"
