"""Bounded strict JSON input and exclusively created replay-verifiable bundles."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
from .analysis import build_report, canonical
from .render import render_html

MAX_BYTES = 4 * 1024 * 1024
FILES = {'complex.json', 'requirements.json', 'report.json', 'review.html', 'manifest.json'}


def read_bytes(path, limit=MAX_BYTES, no_symlink=False):
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0)
    if no_symlink:
        flags |= getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise ValueError('bounded regular file required')
        value = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
        if len(value) > limit or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError('input too large or changed during read')
        return value


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _constant(_value):
    raise ValueError('nonfinite JSON number')


def decode(raw):
    try:
        value = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, RecursionError) as error:
        raise ValueError('invalid UTF8 or JSON nesting') from error
    pending = [(value, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > 64:
            raise ValueError('JSON nesting limit exceeded')
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError('nonfinite JSON number')
        if isinstance(item, dict):
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)
    return value


def read_json(path):
    return decode(read_bytes(path))


def bundle_contents(complex_value, requirements):
    report = build_report(complex_value, requirements)
    files = {'complex.json': canonical(complex_value), 'requirements.json': canonical(requirements),
             'report.json': canonical(report), 'review.html': render_html(complex_value, report).encode()}
    if any(len(value) > MAX_BYTES for value in files.values()):
        raise ValueError('output exceeds bundle limits')
    manifest = {'schema_version': 1, 'files': {name: {'sha256': hashlib.sha256(value).hexdigest(),
                                                  'bytes': len(value)} for name, value in sorted(files.items())}}
    files['manifest.json'] = canonical(manifest)
    return files, report


def create_bundle(destination, complex_value, requirements):
    files, report = bundle_contents(complex_value, requirements)
    path = Path(destination)
    # Exclusive directory creation prevents overwriting inputs or prior runs.
    path.mkdir(mode=0o700)
    try:
        for name, value in files.items():
            with (path / name).open('xb') as stream:
                stream.write(value)
    except (OSError, ValueError):
        shutil.rmtree(path)
        raise
    return report


def verify_bundle(destination):
    path = Path(destination)
    if path.is_symlink() or not path.is_dir() or {p.name for p in path.iterdir()} != FILES:
        raise ValueError('exact bundle directory required')
    actual = {}
    for name in sorted(FILES):
        item = path / name
        if item.is_symlink():
            raise ValueError('bundle symlinks forbidden')
        actual[name] = read_bytes(item, no_symlink=True)
    expected, report = bundle_contents(decode(actual['complex.json']), decode(actual['requirements.json']))
    if actual != expected:
        raise ValueError('bundle differs from recomputed analysis')
    return report


def compare_bundles(baseline, scenario):
    left, right = verify_bundle(baseline), verify_bundle(scenario)
    return {'schema_version': 1, 'baseline_input_sha256': left['input_sha256'],
            'scenario_input_sha256': right['input_sha256'],
            'acceptance_criteria_changed': left['requirements'] != right['requirements'],
            'baseline_status': left['status'], 'scenario_status': right['status'],
            'betti_change': [b - a for a, b in zip(left['betti'], right['betti'])],
            'new_gaps': sorted(set(right['gaps']) - set(left['gaps'])),
            'resolved_gaps': sorted(set(left['gaps']) - set(right['gaps'])),
            'execution_authorized': False,
            'limitation': 'Descriptive comparison; input and criteria changes are recorded, not a causal explanation'}
