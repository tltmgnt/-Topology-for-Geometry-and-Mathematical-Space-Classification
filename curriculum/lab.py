"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")




def run():
    from itertools import combinations
    from geometry_topology.analysis import build_report
    policy = {"schema_version":1,"expected_betti":None,"require_surface":False,"require_orientable":False}
    def report(faces):
        return build_report({"schema_version":1,"name":"synthetic lesson","simplices":faces},policy)
    ring = report([list("ab"),list("bc"),list("ca")])
    disk = report([list("abc")])
    sphere = report([list(face) for face in combinations("abcd",3)])
    check("unfilled triangle is a circle", ring["betti"], [1,1,0,0])
    check("filled triangle has no H1 hole", disk["betti"], [1,0,0,0])
    check("tetrahedron boundary has H2", sphere["betti"], [1,0,1,0])
    check("disk boundary component", disk["surface"]["classification"]["boundary_components"], 1)
    check("sphere genus", sphere["surface"]["classification"]["genus"], 0)
    check("shared edge in three faces is nonmanifold", report([list("abc"),list("abd"),list("abe")])["surface"]["recognized"], False)
    rejects("empty generator rejected", lambda: report([[]]))

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
