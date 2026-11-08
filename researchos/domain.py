"""Scoped synthetic domain adapter; no external execution."""
import itertools

def check():
    faces=list(itertools.combinations(range(4),3))
    edges={edge for face in faces for edge in itertools.combinations(face,2)}
    vertices={v for face in faces for v in face}
    characteristic=len(vertices)-len(edges)+len(faces)
    return {'domain':'geometry','statement':'The explicitly enumerated tetrahedron boundary has Euler characteristic 2.',
            'passed':characteristic==2 and len(edges)==6,'configuration':{'faces':[list(f) for f in faces]},
            'observed':{'vertices':len(vertices),'edges':len(edges),'faces':len(faces),'euler_characteristic':characteristic},
            'scope':'Finite combinatorial fixture only; Euler characteristic alone does not classify arbitrary spaces'}
