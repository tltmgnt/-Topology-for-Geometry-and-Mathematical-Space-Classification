"""Exact finite simplicial homology and bounded combinatorial surface recognition."""
import hashlib
from itertools import combinations
import json


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2) + '\n').encode()


def rank(columns):
    """Rank over GF(2), represented by integer bit columns."""
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def components(vertices, edges):
    neighbors = {v: set() for v in vertices}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    result, unseen = [], set(vertices)
    while unseen:
        pending, part = [min(unseen)], set()
        while pending:
            node = pending.pop()
            if node in part:
                continue
            part.add(node)
            pending.extend(neighbors[node] - part)
        unseen -= part
        result.append(sorted(part))
    return result


def parse_complex(value):
    if not isinstance(value, dict) or set(value) != {'schema_version', 'name', 'simplices'} or type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError('expected schema_version 1, name, simplices')
    if not isinstance(value['name'], str) or not 1 <= len(value['name']) <= 200:
        raise ValueError('bounded nonempty name required')
    items = value['simplices']
    if not isinstance(items, list) or not 1 <= len(items) <= 512:
        raise ValueError('require 1..512 generating simplices')
    cells = set()
    for item in items:
        if not isinstance(item, list) or not 1 <= len(item) <= 4:
            raise ValueError('simplex must have 1..4 vertices (dimension <=3)')
        if any(not isinstance(v, str) or not 1 <= len(v) <= 64 for v in item) or len(set(item)) != len(item):
            raise ValueError('distinct bounded vertex identifiers required')
        ordered = tuple(sorted(item))
        # Redundant generating faces are permitted and collapse to one simplex.
        for size in range(1, len(ordered) + 1):
            cells.update(combinations(ordered, size))
        if len(cells) > 4096:
            raise ValueError('closure exceeds 4096 simplices')
    levels = [sorted(cell for cell in cells if len(cell) == d + 1) for d in range(4)]
    if len(levels[0]) > 128:
        raise ValueError('at most 128 vertices')
    return levels


def boundary(levels, dimension):
    if dimension == 0:
        return [0] * len(levels[0])
    index = {cell: i for i, cell in enumerate(levels[dimension - 1])}
    return [sum(1 << index[face] for face in combinations(cell, dimension)) for cell in levels[dimension]]


def surface_info(levels):
    vertices, edges, triangles, tetrahedra = levels
    if not triangles or tetrahedra:
        return {'recognized': False, 'reason': 'requires a pure two-dimensional complex'}
    incidence = {edge: [] for edge in edges}
    for i, triangle in enumerate(triangles):
        for edge in combinations(triangle, 2):
            incidence[edge].append(i)
    if any(len(items) not in (1, 2) for items in incidence.values()):
        return {'recognized': False, 'reason': 'edge incidence is not one or two'}
    boundary_edges = [edge for edge, items in incidence.items() if len(items) == 1]
    boundary_vertices = {v for edge in boundary_edges for v in edge}
    for vertex, in vertices:
        link_edges = [tuple(v for v in triangle if v != vertex) for triangle in triangles if vertex in triangle]
        link_vertices = {v for edge in link_edges for v in edge}
        if not link_vertices or len(components(link_vertices, link_edges)) != 1:
            return {'recognized': False, 'reason': 'vertex link is empty or disconnected'}
        degrees = [sum(v in edge for edge in link_edges) for v in link_vertices]
        expected = sorted([1, 1] + [2] * (len(link_vertices) - 2)) if vertex in boundary_vertices else [2] * len(link_vertices)
        if sorted(degrees) != expected:
            return {'recognized': False, 'reason': 'vertex link is not a path or cycle'}
    # Adjacent sorted triangles must induce opposite orientations on shared edges.
    neighbors = {i: [] for i in range(len(triangles))}
    for edge, items in incidence.items():
        if len(items) == 2:
            a, b = items
            omitted_a = next(j for j, v in enumerate(triangles[a]) if v not in edge)
            omitted_b = next(j for j, v in enumerate(triangles[b]) if v not in edge)
            parity = 1 ^ (omitted_a % 2) ^ (omitted_b % 2)
            neighbors[a].append((b, parity))
            neighbors[b].append((a, parity))
    labels, orientable = {}, True
    for root in neighbors:
        if root in labels:
            continue
        labels[root] = 0
        pending = [root]
        while pending:
            node = pending.pop()
            for neighbor, parity in neighbors[node]:
                expected = labels[node] ^ parity
                if neighbor in labels:
                    orientable &= labels[neighbor] == expected
                else:
                    labels[neighbor] = expected
                    pending.append(neighbor)
    parts = components([v[0] for v in vertices], edges)
    boundary_count = len(components(boundary_vertices, boundary_edges))
    result = {'recognized': True, 'connected': len(parts) == 1, 'orientable': bool(orientable), 'boundary_components': boundary_count}
    if len(parts) == 1:
        euler = len(vertices) - len(edges) + len(triangles)
        defect = 2 - boundary_count - euler
        result['classification'] = {'family': 'orientable surface' if orientable else 'nonorientable surface',
                                    'genus' if orientable else 'crosscaps': defect // 2 if orientable else defect,
                                    'boundary_components': boundary_count}
    else:
        result['classification'] = None
        result['reason'] = 'global genus omitted for disconnected surfaces'
    return result


def validate_requirements(value):
    if not isinstance(value, dict) or set(value) != {'schema_version', 'expected_betti', 'require_surface', 'require_orientable'}:
        raise ValueError('requirements must specify schema_version, expected_betti, require_surface, require_orientable')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError('unsupported requirements version')
    expected = value['expected_betti']
    if expected is not None and (not isinstance(expected, list) or len(expected) != 4 or any(type(v) is not int or v < 0 for v in expected)):
        raise ValueError('expected_betti must be null or four nonnegative integers')
    if any(type(value[k]) is not bool for k in ('require_surface', 'require_orientable')):
        raise ValueError('boolean requirements required')
    return value


def build_report(value, requirements):
    levels = parse_complex(value)
    requirements = validate_requirements(requirements)
    matrices = [boundary(levels, d) for d in range(4)]
    for dimension in range(2, 4):
        for column in matrices[dimension]:
            composed = 0
            while column:
                bit = column & -column
                composed ^= matrices[dimension - 1][bit.bit_length() - 1]
                column ^= bit
            if composed:
                raise ValueError('boundary composition invariant violated')
    ranks = [rank(matrix) for matrix in matrices] + [0]
    betti = [len(levels[d]) - ranks[d] - ranks[d + 1] for d in range(4)]
    euler = sum((-1)**d * len(levels[d]) for d in range(4))
    if euler != sum((-1)**d * betti[d] for d in range(4)):
        raise ValueError('Euler-Poincare invariant violated')
    surface, gaps = surface_info(levels), []
    if requirements['expected_betti'] is not None and betti != requirements['expected_betti']:
        gaps.append('BETTI_MISMATCH')
    if requirements['require_surface'] and not surface['recognized']:
        gaps.append('NOT_RECOGNIZED_SURFACE')
    if requirements['require_orientable'] and not (surface['recognized'] and surface['orientable']):
        gaps.append('ORIENTABILITY_NOT_ESTABLISHED')
    return {'schema_version': 1, 'engine_version': '0.1.0', 'name': value['name'],
            'input_sha256': hashlib.sha256(canonical(value)).hexdigest(),
            'requirements_sha256': hashlib.sha256(canonical(requirements)).hexdigest(), 'requirements': requirements,
            'status': 'FAIL' if gaps else 'PASS', 'gaps': gaps, 'field': 'GF(2)',
            'simplex_counts': [len(level) for level in levels], 'boundary_ranks': ranks[:4],
            'betti': betti, 'euler_characteristic': euler, 'boundary_squared_zero': True,
            'surface': surface, 'execution_authorized': False,
            'assurance_scope': 'Exact combinatorial checks on the supplied finite complex; no physical-space, general homeomorphism, or truth certification'}
