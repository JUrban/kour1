#!/usr/bin/env python3
"""Audit the class-two refinement, retained setup errors, and corrected scope."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process(name, command, sentinel):
    stem = ROOT / ('results/16.14-class2-'+name)
    rec = json.loads(Path(str(stem)+'-process.json').read_text())
    out, err = Path(str(stem)+'.log'), Path(str(stem)+'.stderr')
    assert rec['command'] == command and rec['actual_returncode'] == 0
    assert rec['sentinel_seen'] is True and not err.read_bytes()
    assert sha(out) == rec['stdout_sha256'] and sha(err) == rec['stderr_sha256']
    assert out.read_text().count(sentinel) == 1
    return out.read_text()


def summarize():
    native = process('native', ['bin/gap','-o','2g','scripts/verify_16_14_class2.g'],
                     'PASS_16_14_CLASS2_NATIVE models=10')
    match = re.fullmatch(r'\s*NATIVE_1614_CLASS2_ROWS\s*(\[.*\])\s*'
                         r'PASS_16_14_CLASS2_NATIVE models=10\s*',native,flags=re.S)
    assert match is not None
    rows = json.loads(match[1])
    independent = process('independent', ['python3','scripts/verify_16_14_class2.py'],
                          'PASS_16_14_CLASS2_INDEPENDENT models=10 rejected_corruptions=5')
    lines = independent.splitlines()
    assert len(lines) == 2 and lines[1] == 'PASS_16_14_CLASS2_INDEPENDENT models=10 rejected_corruptions=5'
    summary = json.loads((ROOT/'results/16.14-class2-summary.json').read_text())
    assert json.loads(lines[0]) == summary and summary['status'] == 'PASS'
    assert 'prior consequence' in summary['scope']
    assert [c['row'] for c in summary['cases']] == rows and len(rows) == 10
    assert summary['stats'] == dict(table_entries=84097,associativity_generator_cases=291200,
                                    representative_checks=401,polarization_triples=4483)
    assert sum(row[2] for row in summary['quadratic_controls']) == 1086606
    assert len(summary['rejected_corruptions']) == 5 and summary['rejected_cubic_control']
    for stage in ['initial','second-initial','third-initial','fourth-initial','independent-initial']:
        name = 'independent' if stage == 'independent-initial' else 'native'
        base = ROOT/f'results/16.14-class2-{stage}/16.14-class2-{name}'
        rec = json.loads(Path(str(base)+'-process.json').read_text())
        out, err = Path(str(base)+'.log'), Path(str(base)+'.stderr')
        assert rec['actual_returncode'] == (1 if name == 'independent' else 0)
        assert rec['sentinel_seen'] is False and err.read_bytes()
        assert sha(out) == rec['stdout_sha256'] and sha(err) == rec['stderr_sha256']
    statement = json.loads((ROOT/'results/16.14-class2-statement.json').read_text())
    assert statement['id'] == '16.14' and statement['pdf_page'] == 98
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    args = parser.parse_args()
    summary = summarize()
    packet = json.loads((ROOT/'results/16.14-class2-packet.json').read_text())
    assert packet['summary'] == summary and packet['new_complete_candidates_added'] == 0
    assert packet['original_problem_status'] == 'prior affirmative consequence'

    def bindings():
        assert len({row['path'] for row in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],path

    bindings()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='16.14-class2-replay-') as directory:
            tmp = Path(directory); (tmp/'results').mkdir()
            p = subprocess.run([str(ROOT/'bin/gap'),'-o','2g',
                                str(ROOT/'scripts/verify_16_14_class2.g')],
                               cwd=tmp,capture_output=True,timeout=60)
            assert p.returncode == 0 and not p.stderr
            assert p.stdout == (ROOT/'results/16.14-class2-native.log').read_bytes()
            for i in range(1,11):
                name = f'results/16.14-class2-model-{i}.json'
                assert (tmp/name).read_bytes() == (ROOT/name).read_bytes()
        p = subprocess.run(['python3',str(ROOT/'scripts/verify_16_14_class2.py')],
                           cwd=ROOT,capture_output=True,timeout=60)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/'results/16.14-class2-independent.log').read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,
                          original_problem_status=packet['original_problem_status'],
                          stats=summary['stats']),sort_keys=True))
    print('PASS_16_14_CLASS2_PACKET')


if __name__ == '__main__':
    main()
