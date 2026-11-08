"""Scoped adapter for the existing domain analyzer, not external validation."""
from geometry_topology import build_report
DATA={'schema_version': 1, 'name': 'Synthetic tetrahedron boundary (2-sphere)', 'simplices': [['a', 'b', 'c'], ['a', 'b', 'd'], ['a', 'c', 'd'], ['b', 'c', 'd']]}
REQUIREMENTS={'schema_version': 1, 'expected_betti': [1, 0, 1, 0], 'require_surface': True, 'require_orientable': True}

def check():
    report=build_report(DATA,REQUIREMENTS)
    passed=report['status']=='PASS' and report['betti']==[1,0,1,0] and report['euler_characteristic']==2
    observed=report
    return {'domain':'geometry','statement':'The supplied tetrahedron-boundary fixture has Betti [1,0,1,0], Euler characteristic 2, and passes its finite-complex requirements.','passed':passed,
            'configuration':{'input':DATA,'requirements':REQUIREMENTS},'observed':observed,
            'scope':'Synthetic software/model requirements only; no independent scientific certification or execution authority'}
