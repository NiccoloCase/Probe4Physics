"""Verify that retained experiment inputs match the research baseline."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'docs/release-inputs.json').read_text())
    problems = []
    for item in manifest['files']:
        path = root / item['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            problems.append(item['path'])
    if problems:
        raise SystemExit('Baseline input mismatch: ' + ', '.join(problems))
    print(f"Verified {len(manifest['files'])} unchanged experiment input files against {manifest['baseline_commit'][:7]}.")


if __name__ == '__main__':
    main()
