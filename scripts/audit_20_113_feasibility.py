#!/usr/bin/env python3
"""Check the preserved failure evidence; never interpret progress as completion."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize():
    stem = ROOT / 'results/20.113-pq-probe'
    rec = json.loads(Path(str(stem) + '-process.json').read_text())
    out, err = Path(str(stem) + '.log'), Path(str(stem) + '.stderr')
    assert rec['actual_returncode'] == 1 and rec['bounded_stop']
    assert rec['sentinel_seen'] is False and rec['accepted_complete_probe'] is False
    assert rec['timeout_seconds'] == 180 and rec['address_space_limit_bytes'] == 8*1024**3
    assert rec['stdout_sha256'] == sha(out) and rec['stderr_sha256'] == sha(err)
    assert not err.read_bytes()
    text = out.read_text()
    assert 'PASS_20_113_PQ_PROBE' not in text and 'PROBE_20113_RESULT' not in text
    rows = [[int(a), int(b)] for a, b in re.findall(r'class (\d+) has order 7\^(\d+)', text)]
    assert rows == [[i, n] for i, n in enumerate([4, 9, 25, 70, 214, 654, 1978, 6238], 1)]
    download = json.loads((ROOT / 'results/20.113-source-download.json').read_text())
    source = ROOT / 'references/cache/vaughan-lee-schur-II-2111.11098v3.pdf'
    assert source.stat().st_size == download['bytes'] and sha(source) == download['sha256']
    return dict(progress_only_rows=rows, accepted_complete_probe=False,
                actual_probe_returncode=1, new_complete_candidates_added=0)


if __name__ == '__main__':
    summary = summarize()
    packet = json.loads((ROOT / 'results/20.113-feasibility-packet.json').read_text())
    assert packet['summary'] == summary
    assert len({row['path'] for row in packet['files']}) == len(packet['files'])
    for row in packet['files']:
        path = ROOT / row['path']
        assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], path
    print(json.dumps(dict(status='PASS_FAILURE_EVIDENCE', files=len(packet['files']),
                          summary=summary), sort_keys=True))
    print('PASS_20_113_FAILURE_EVIDENCE')
