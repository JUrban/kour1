#!/usr/bin/env python3
"""Replay the bounded controls for the omitted-pair structural lemma."""
import hashlib
import json
from pathlib import Path
import check_15_46_omitted_pairs as checker


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet = json.loads(Path('results/15.46-omitted-pairs-packet.json').read_text())
    for path, digest in packet['sha256'].items():
        assert sha(path) == digest, path
    for stem in ['19.61-square-completion', '19.62-rank-two']:
        path = Path('results/'+stem+'-packet.json')
        prior = json.loads(path.read_text())
        for source, digest in prior['sha256'].items():
            assert sha(source) == digest, source
        obs = json.loads(Path('results/'+stem+'-audit-observation.json').read_text())
        assert obs['exit_code'] == 0 and obs['packet_sha256'] == sha(path)
        assert obs['audit_log_sha256'] == sha('results/'+stem+'-audit.log')
    result = checker.run()
    assert result == json.loads(Path('results/15.46-omitted-pairs-controls.json').read_text())
    assert result['controls'] == 1127612
    print('PASS_1546_OMITTED_PAIR_PACKET', len(packet['sha256']), 'controls=1127612 general_problem_open', flush=True)


if __name__ == '__main__':
    run()
