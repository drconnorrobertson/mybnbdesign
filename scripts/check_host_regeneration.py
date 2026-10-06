"""Check committed host-library output and deterministic regeneration in a copy."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from check_jsonld import check

SOURCE = Path(__file__).resolve().parents[1]

def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for pattern in ('*.html', '*.xml', 'worksheet.txt') for p in root.rglob(pattern)
            if not any(part.startswith('.') for part in p.relative_to(root).parts)}

def compare(before, after):
    return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))

def run(root):
    before = snapshot(root)
    with tempfile.TemporaryDirectory(prefix='bnb-host-regeneration-') as temporary:
        copy = Path(temporary) / 'site'
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        def build():
            for script in ('build_host_library.py', 'rebuild_discovery.py'):
                subprocess.run([sys.executable, str(SOURCE / 'scripts' / script),
                                '--output-root', str(copy)], check=True,
                               stdout=subprocess.DEVNULL)
        build()
        first = snapshot(copy)
        first_jsonld = check(copy)
        build()
        second = snapshot(copy)
        second_jsonld = check(copy)
        result = {'uncommitted_generated_changes': compare(before, first),
                  'nondeterministic_changes': compare(first, second),
                  'generated_files_checked': len(second),
                  'jsonld_errors': first_jsonld['errors'] + second_jsonld['errors']}
        print(json.dumps(result, indent=2))
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=SOURCE)
    args = parser.parse_args()
    result = run(args.root.resolve())
    raise SystemExit(bool(result['uncommitted_generated_changes'] or result['nondeterministic_changes'] or result['jsonld_errors']))
