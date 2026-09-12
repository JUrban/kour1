#!/usr/bin/env python3
"""Bounded positive certificates, rejected first run, and exact dual replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    packet = json.loads((ROOT/'results/20.112-chain-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 0
    def bindings():
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],path
    bindings()
    old = json.loads((ROOT/'results/20.112-screen-audit.json').read_text())
    assert old['total_groups'] == 8339 and old['counterexamples'] == 0
    for path, digest in old['sha256'].items():
        assert sha(ROOT/path) == digest
    for name in ['gap','python']:
        base = ROOT/('results/20.112-chain-'+name)
        record = json.loads(Path(str(base)+'-process.json').read_text())
        out, err = Path(str(base)+'.log'), Path(str(base)+'.stderr')
        assert record['actual_returncode'] == 0 and record['sentinel_seen']
        assert sha(out) == record['stdout_sha256'] and sha(err) == record['stderr_sha256']
        assert not err.read_bytes() and 'Error' not in out.read_text()
    failed = ROOT/'results/20.112-chain-initial'
    initial = json.loads((failed/'20.112-chain-gap-process.json').read_text())
    assert initial['actual_returncode'] == 0 and initial['sentinel_seen']
    assert sha(failed/'20.112-chain-gap.log') == initial['stdout_sha256']
    assert sha(failed/'20.112-chain-gap.stderr') == initial['stderr_sha256']
    assert (failed/'20.112-chain-gap.stderr').read_text().count('Syntax warning:') == 6
    assert json.loads((failed/'wrapper-observation.json').read_text())['actual_wrapper_returncode'] == 1
    control = json.loads((ROOT/'results/20.112-chain-controls.json').read_text())
    assert control['groups'] == 15 and control['original_retained_cases'] == 12
    assert control['distinct_quotient_models'] == 3 and control['new_complete_candidates_added'] == 0
    assert control['controls'] == dict(central_steps=157,chain_edges=61,maximal_cosets=227,
        nilpotent_factors=137,permutation_edges=37152,sylow_chains=30,table_entries=25380864)
    assert control['rejected_mutations'] == ['cayley','normalizer','core','tower','missing_edge']
    with tempfile.TemporaryDirectory(prefix='20.112-replay-') as directory:
        (Path(directory)/'results').mkdir()
        p = subprocess.run([str(ROOT/'bin/gap'),'-o','2g',str(ROOT/'scripts/check_20_112_chains.g')],
                           cwd=directory,capture_output=True,timeout=120)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/'results/20.112-chain-gap.log').read_bytes()
        assert (Path(directory)/'results/20.112-chain-certificate.json').read_bytes() == (
            ROOT/'results/20.112-chain-certificate.json').read_bytes()
    p = subprocess.run(['python3','scripts/verify_20_112_chains.py'],cwd=ROOT,
                       capture_output=True,timeout=120)
    assert p.returncode == 0 and not p.stderr
    assert p.stdout == (ROOT/'results/20.112-chain-python.log').read_bytes()
    bindings()
    print('PASS_20112_PACKET files=%d models=15 chains=30 maximal_steps=61 '
          'table_entries=25380864 mutations=5 rejected_run_preserved=true new_complete_candidates=0'
          % len(packet['files']))


if __name__ == '__main__':
    main()
