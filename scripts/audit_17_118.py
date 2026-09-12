#!/usr/bin/env python3
"""Audit 17.118 source/evidence bindings and rerun independent finite controls.

This is an evidence audit, not an automatic proof of the universal theorem.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_bindings(packet):
    assert packet['new_complete_candidates_added'] == 0
    assert packet['full_problem_solved'] is False
    for item in packet['files']:
        path = ROOT / item['path']
        assert path.stat().st_size == item['bytes'], path
        assert sha(path) == item['sha256'], path


def main():
    packet = json.loads((ROOT / 'results/17.118-packet.json').read_text())
    verify_bindings(packet)
    for item in json.loads((ROOT / 'results/17.118-source-downloads.json').read_text()):
        path = ROOT / item['path']
        assert item['status'] == 200
        assert item['bytes'] == path.stat().st_size
        assert item['sha256'] == sha(path)
    for name, sentinel in [('pilot', 'PASS_17118_PILOT'),
                           ('algebra', 'PASS_17118_ALGEBRA'),
                           ('model', 'PASS_17118_MODEL'),
                           ('matrices', 'PASS_17118_MATRICES')]:
        base = ROOT / ('results/17.118-'+name)
        record = json.loads(Path(str(base)+'-process.json').read_text())
        out, err = Path(str(base)+'.log'), Path(str(base)+'.stderr')
        assert record['actual_returncode'] == 0
        assert record['stdout_sha256'] == sha(out)
        assert record['stderr_sha256'] == sha(err)
        assert not err.read_bytes()
        assert out.read_text().count(sentinel) == 1
        assert all(t not in out.read_text() for t in ['Error', 'Syntax warning',
                                                     'Assertion failure'])
    controls = json.loads((ROOT/'results/17.118-algebra-controls.json').read_text())
    assert [row['p'] for row in controls] == [2, 3, 5]
    assert sum(row['linear_vectors'] for row in controls) == 3156
    assert sum(row['associativity_triples'] for row in controls) == 1800
    assert [row['characteristic_exponent_p_index'] for row in controls] == [4,27,3125]
    pilot = ' '.join((ROOT/'results/17.118-pilot.log').read_text().split())
    for phrase in ['order=6561 class=3 exponent=9 derived_order=243',
                   'abelian=[ 3, 3, 3 ]', 'lower_orders=[ 6561, 243, 9, 1 ]',
                   'hyperplane_orders=[ 2187, 2187, 2187 ] exponents=[ 3, 3, 3 ]',
                   'cycle_bijective=true', 'noncubes=1944 root_count=4617']:
        assert phrase in pilot, phrase
    for name, command in [
        ('algebra', ['python3','scripts/check_17_118.py']),
        ('model', ['python3','scripts/verify_17_118_model.py']),
        ('matrices', ['bin/gap','-o','512m','scripts/check_17_118_matrices.g'])]:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=300)
        assert process.returncode == 0 and not process.stderr, name
        assert process.stdout == (ROOT/('results/17.118-'+name+'.log')).read_bytes(), name
    # The producer deterministically rewrites its two output files; these too
    # must still match the pre-replay bindings.
    verify_bindings(packet)
    print('PASS_17118_PACKET files=%d linear_vectors=3156 '
          'group_elements=6561 generator_edges=19683 mutations=5 '
          'matrix_model_isomorphic=true new_complete_candidates=0' % len(packet['files']))


if __name__ == '__main__':
    main()
