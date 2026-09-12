#!/usr/bin/env python3
"""Bind exact evidence, reconcile saved screens, and replay independent controls."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from summarize_21_100 import process, summarize

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    packet = json.loads((ROOT/'results/21.100-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 0
    def bindings():
        assert len({x['path'] for x in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],path
    bindings()
    assert summarize() == json.loads((ROOT/'results/21.100-screen-summary.json').read_text())
    for name,sentinel in [('conlon-probe','PASS_21100_CONLON_DUPLICATES'),
                          ('independent-gap','PASS_21100_EXPORT'),
                          ('independent-python','PASS_21100_INDEPENDENT')]:
        process(ROOT/('results/21.100-'+name),sentinel)
    failed = ROOT/'results/21.100-independent-initial'
    for name,rc in [('gap',0),('python',1)]:
        base = failed/('21.100-independent-'+name)
        record = json.loads(Path(str(base)+'-process.json').read_text())
        assert record['actual_returncode'] == rc and not record['sentinel_seen']
        assert sha(Path(str(base)+'.log')) == record['stdout_sha256']
        assert sha(Path(str(base)+'.stderr')) == record['stderr_sha256']
        assert Path(str(base)+'.stderr').read_bytes()
    assert 'Conlon completeness' in (failed/'21.100-independent-gap.stderr').read_text()
    try:
        json.loads((failed/'21.100-independent-certificate.json').read_text())
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError('initial certificate was not truncated')
    assert [x['actual_wrapper_returncode'] for x in json.loads(
        (failed/'wrapper-observations.json').read_text())] == [1,1]
    failed_audit = ROOT/'results/21.100-audit-initial'
    initial = json.loads((failed_audit/'21.100-audit-process.json').read_text())
    assert initial['actual_returncode'] == 1 and not initial['sentinel_seen']
    assert sha(failed_audit/'21.100-audit.log') == initial['stdout_sha256']
    assert sha(failed_audit/'21.100-audit.stderr') == initial['stderr_sha256']
    assert json.loads((failed_audit/'wrapper-observation.json').read_text())['actual_wrapper_returncode'] == 1
    seven = ROOT/'results/21.100-independent-seven'
    for name,sentinel in [('gap','PASS_21100_EXPORT'),('python','PASS_21100_INDEPENDENT')]:
        process(seven/('21.100-independent-'+name),sentinel)
    old = json.loads((seven/'21.100-independent-controls.json').read_text())
    assert old['counts']['groups'] == 7 and old['counts']['certified_irreducibles'] == 812
    control = json.loads((ROOT/'results/21.100-independent-controls.json').read_text())
    assert control['counts']['groups'] == 13 and control['new_complete_candidates_added'] == 0
    assert control['rejected_mutations'] == ['cayley','automorphism','linear_map','missing_character','inducing_subgroup']
    screens = []
    for line in (ROOT/'results/21.100-pilot-rows.jsonl').read_text().splitlines():
        r = json.loads(line); screens.append(r[:2]+[2,2]+r[2:])
    for o in [256,2187]:
        for s in range(4):
            screens.extend(json.loads(line) for line in (ROOT/f'results/21.100-order{o}-shard{s}-rows.jsonl').read_text().splitlines())
    for row in control['groups']:
        signature = Counter((x['degree'],x['correspondent_degree'],int(x['nonvanishing']))
                            for x in row['characters'])
        matches = [r for r in screens if r[:2] == row['catalogue_id'] and r[3] == row['action_order']
                   and r[7] == row['fixed_order'] and r[10] == row['fixed_abelianization']]
        assert any(Counter(tuple(x[1:4]) for x in r[-1]) == signature for r in matches)
    with tempfile.TemporaryDirectory(prefix='21.100-replay-') as directory:
        (Path(directory)/'results').mkdir()
        p = subprocess.run([str(ROOT/'bin/gap'),'-o','2g',str(ROOT/'scripts/export_21_100_controls.g')],
                           cwd=directory,capture_output=True,timeout=240)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/'results/21.100-independent-gap.log').read_bytes()
        assert (Path(directory)/'results/21.100-independent-certificate.json').read_bytes() == (
            ROOT/'results/21.100-independent-certificate.json').read_bytes()
    p = subprocess.run(['python3','scripts/verify_21_100_controls.py'],cwd=ROOT,
                       capture_output=True,timeout=240)
    assert p.returncode == 0 and not p.stderr
    assert p.stdout == (ROOT/'results/21.100-independent-python.log').read_bytes()
    p = subprocess.run(['bin/gap','-o','2g','scripts/probe_21_100_conlon.g'],cwd=ROOT,
                       capture_output=True,timeout=60)
    assert p.returncode == 0 and not p.stderr
    assert p.stdout == (ROOT/'results/21.100-conlon-probe.log').read_bytes()
    bindings()
    print('PASS_21100_PACKET files=%d actions=15623 characters=313685 nonlinear=66172 '
          'independent_models=13 mutations=5 rejected_runs_preserved=true new_complete_candidates=0'
          % len(packet['files']))


if __name__ == '__main__':
    main()
