"""Offline CLI: analyze, verify and compare finite topology review bundles."""
import argparse
import json
import sys
from .io import compare_bundles, create_bundle, read_json, verify_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    analyze = commands.add_parser('analyze')
    analyze.add_argument('complex')
    analyze.add_argument('--requirements', required=True)
    analyze.add_argument('--output', required=True)
    verify = commands.add_parser('verify')
    verify.add_argument('bundle')
    compare = commands.add_parser('compare')
    compare.add_argument('baseline')
    compare.add_argument('scenario')
    args = parser.parse_args(argv)
    try:
        if args.command == 'analyze':
            result = create_bundle(args.output, read_json(args.complex), read_json(args.requirements))
        elif args.command == 'verify':
            result = verify_bundle(args.bundle)
        else:
            result = compare_bundles(args.baseline, args.scenario)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 1 if result.get('status') == 'FAIL' else 0
    except (OSError, ValueError, TypeError, OverflowError) as error:
        print(f'geometry-topology: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
