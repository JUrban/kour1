#!/usr/bin/env python3
"""Verify archived evidence, not the unsolved mathematical assertion."""
import hashlib
import json
import subprocess
from pathlib import Path


def main():
    manifest = json.loads(Path('results/11.18-manifest.json').read_text())
    for name, digest in manifest['sha256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    records = []
    for name in ('exploration-summary', 'ace-summary', 'matrix-status'):
        data = json.loads(Path(f'results/11.18-{name}.json').read_text())
        records.extend(data if isinstance(data, list) else [data])
    assert len(records) == 9
    for record in records:
        assert record['returncode'] == 0
        assert record['complete'] and record['clean_log']
        assert not record['timeout']
        for name, digest in record['sha256'].items():
            assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    subprocess.run(['python3', 'scripts/replay_11_18_permutations.py'], check=True)
    print(f"PASS: {len(manifest['sha256'])} retained hashes, 9 final process records; no resolution claimed")


if __name__ == '__main__':
    main()
