import copy
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from geometry_topology.analysis import build_report, parse_complex, rank
from geometry_topology.io import create_bundle, verify_bundle, compare_bundles, decode

POLICY = {'schema_version': 1, 'expected_betti': None, 'require_surface': False, 'require_orientable': False}


def complex_of(simplices, name='synthetic'):
    return {'schema_version': 1, 'name': name, 'simplices': simplices}


def analyze(simplices):
    return build_report(complex_of(simplices), POLICY)


def grid(twist=False):
    # Triangulated strip; identify the two ends, optionally reversing the width.
    def vertex(i, j):
        return f'{i % 5}-{1-j if twist and i == 5 else j}'
    faces = []
    for i in range(5):
        a, b, c, d = vertex(i, 0), vertex(i+1, 0), vertex(i+1, 1), vertex(i, 1)
        faces.extend([[a, b, c], [a, c, d]])
    return faces


class GeometryTests(unittest.TestCase):
    def test_point(self):
        self.assertEqual(analyze([['a']])['betti'], [1, 0, 0, 0])

    def test_circle(self):
        self.assertEqual(analyze([['a', 'b'], ['b', 'c'], ['c', 'a']])['betti'], [1, 1, 0, 0])

    def test_disk(self):
        r = analyze([['a', 'b', 'c']])
        self.assertEqual(r['betti'], [1, 0, 0, 0])
        self.assertEqual(r['surface']['classification'], {'family': 'orientable surface', 'genus': 0, 'boundary_components': 1})

    def test_sphere(self):
        r = analyze([list(f) for f in combinations('abcd', 3)])
        self.assertEqual(r['betti'], [1, 0, 1, 0])
        self.assertEqual(r['surface']['classification']['genus'], 0)

    def test_ball(self):
        r = analyze([list('abcd')])
        self.assertEqual(r['betti'], [1, 0, 0, 0])
        self.assertFalse(r['surface']['recognized'])

    def test_three_sphere(self):
        self.assertEqual(analyze([list(f) for f in combinations('abcde', 4)])['betti'], [1, 0, 0, 1])

    def test_annulus(self):
        r = analyze(grid())
        self.assertEqual(r['surface']['boundary_components'], 2)
        self.assertTrue(r['surface']['orientable'])
        self.assertEqual(r['betti'], [1, 1, 0, 0])

    def test_mobius(self):
        r = analyze(grid(True))
        self.assertEqual(r['surface']['classification'], {'family': 'nonorientable surface', 'crosscaps': 1, 'boundary_components': 1})
        self.assertEqual(r['betti'], [1, 1, 0, 0])

    def test_torus(self):
        def v(i, j):
            return f'{i % 4},{j % 4}'
        faces = []
        for i in range(4):
            for j in range(4):
                a,b,c,d = v(i,j),v(i+1,j),v(i+1,j+1),v(i,j+1)
                faces.extend([[a,b,c],[a,c,d]])
        r = analyze(faces)
        self.assertEqual(r['betti'], [1, 2, 1, 0])
        self.assertEqual(r['surface']['classification']['genus'], 1)

    def test_pinched_vertex_not_surface(self):
        self.assertFalse(analyze([list('abc'), list('ade')])['surface']['recognized'])

    def test_nonmanifold_edge(self):
        self.assertFalse(analyze([list('abc'),list('abd'),list('abe')])['surface']['recognized'])

    def test_dangling_edge(self):
        self.assertFalse(analyze([list('abc'),list('ad')])['surface']['recognized'])

    def test_disconnected(self):
        r = analyze([list('abc'),list('def')])
        self.assertEqual(r['betti'][0], 2)
        self.assertTrue(r['surface']['recognized'])
        self.assertIsNone(r['surface']['classification'])

    def test_permutation_invariance(self):
        a,b = analyze([list('abc'),list('acd')]),analyze([list('dca'),list('cba')])
        for key in ('betti','simplex_counts','surface','boundary_ranks'):
            self.assertEqual(a[key], b[key])

    def test_rank_exhaustive(self):
        for a in range(8):
            for b in range(8):
                for c in range(8):
                    span = {0}
                    for col in [a,b,c]:
                        span |= {x ^ col for x in list(span)}
                    self.assertEqual(1 << rank([a,b,c]), len(span))

    def test_all_graphs_four_vertices(self):
        edges = list(combinations('abcd',2))
        for mask in range(64):
            selected = [list(e) for i,e in enumerate(edges) if mask >> i & 1]
            r = analyze([[v] for v in 'abcd']+selected)
            # Independent union-find graph oracle.
            groups = [{v} for v in 'abcd']
            for a,b in selected:
                merged = set().union(*(g for g in groups if a in g or b in g))
                groups = [g for g in groups if a not in g and b not in g] + [merged]
            self.assertEqual(r['betti'],[len(groups),len(selected)-4+len(groups),0,0])

    def test_strict_input(self):
        for simplices in ([],[['a','a']],[[]],[list('abcde')],[[True]], [['x'*65]]):
            with self.subTest(simplices=simplices), self.assertRaises(ValueError):
                analyze(simplices)
        with self.assertRaises(ValueError):
            parse_complex({'schema_version':True,'name':'a','simplices':[['a']]})

    def test_limits(self):
        with self.assertRaises(ValueError):
            analyze([[str(i)] for i in range(129)])

    def test_fail_not_unknown(self):
        p = dict(POLICY,expected_betti=[1,1,0,0],require_surface=True)
        self.assertEqual(build_report(complex_of([['a']]),p)['status'],'FAIL')

    def test_requirements(self):
        for p in ({},dict(POLICY,expected_betti=[True,0,0,0]),dict(POLICY,require_surface='yes')):
            with self.assertRaises(ValueError):
                build_report(complex_of([['a']]),p)

    def test_strict_json(self):
        for raw in (b'{"a":1,"a":2}',b'NaN',b'1e400',b'\xff'):
            with self.assertRaises(ValueError):
                decode(raw)

    def test_bundle_and_compare(self):
        with tempfile.TemporaryDirectory() as root:
            a,b = Path(root)/'a',Path(root)/'b'
            create_bundle(a,complex_of([['a']]),POLICY)
            create_bundle(b,complex_of([list('abc')]),dict(POLICY,require_surface=True))
            self.assertEqual(verify_bundle(a)['status'],'PASS')
            self.assertTrue(compare_bundles(a,b)['acceptance_criteria_changed'])
            with self.assertRaises(FileExistsError):
                create_bundle(a,complex_of([['a']]),POLICY)

    def test_forged_report_rejected(self):
        import hashlib
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'a';create_bundle(p,complex_of([['a']]),POLICY)
            report=json.loads((p/'report.json').read_text());report['betti']=[999,0,0,0]
            data=json.dumps(report).encode();(p/'report.json').write_bytes(data)
            manifest=json.loads((p/'manifest.json').read_text())
            manifest['files']['report.json']={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
            (p/'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):verify_bundle(p)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'a';create_bundle(p,complex_of([['a']]),POLICY)
            (Path(root)/'link').symlink_to(p,target_is_directory=True)
            with self.assertRaises(ValueError):verify_bundle(Path(root)/'link')

    def test_html_escaped(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'a';create_bundle(p,complex_of([['a']],'<script>alert(1)</script>'),POLICY)
            html=(p/'review.html').read_text()
            self.assertNotIn('<script>',html)
            self.assertIn('&lt;script&gt;',html)

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root);(p/'input.json').write_text(json.dumps(complex_of([['a']])));(p/'p.json').write_text(json.dumps(dict(POLICY,require_surface=True)))
            r=subprocess.run([sys.executable,'-m','geometry_topology','analyze',str(p/'input.json'),'--requirements',str(p/'p.json'),'--output',str(p/'out')],capture_output=True)
            self.assertEqual(r.returncode,1,r.stderr)
            r=subprocess.run([sys.executable,'-m','geometry_topology','verify',str(p/'out')],capture_output=True)
            self.assertEqual(r.returncode,1,r.stderr)
            r=subprocess.run([sys.executable,'-m','geometry_topology','verify',str(p/'missing')],capture_output=True)
            self.assertEqual(r.returncode,2)


if __name__=='__main__':unittest.main()
