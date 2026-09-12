#!/usr/bin/env python3
"""Replay the short rank-two proof, its root models and readable appendix."""
import ast
import collections
import contextlib
import hashlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
import check_19_62_g2_integer_constants as constants
import prepare_19_62_types as old_preparation
import prepare_19_62_rank_two as preparation
import render_19_62_rank_two as rendering
import verify_19_62_rank_two as verification

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def integral_model(label):
    name = 'results/19.61-g2-integral.grows' if label == 'g2' else 'results/19.62-'+label+'-integral.grows'
    roots, powers, adj, cartan = ast.literal_eval((ROOT/name).read_text())
    expected = {'a2': [[2, -1], [-1, 2]], 'b2': [[2, -2], [-1, 2]],
                'g2': [[2, -1], [-3, 2]]}[label]
    assert cartan == expected
    known = set(map(tuple, cartan)); pending = list(known)
    for v in pending:
        for i, simple in enumerate(cartan):
            w = tuple(x-v[i]*y for x, y in zip(v, simple))
            if w not in known:
                known.add(w); pending.append(w); assert len(known) <= 12
    assert known == set(map(tuple, roots)) and len(known) == len(roots)
    nr = len(roots); dimension = nr+2
    assert len(adj) == dimension and len(powers) == nr
    assert all(type(v) is int for a in adj for row in a for v in row)
    brackets = {(i, j): [(k, adj[i][k][j]) for k in range(dimension) if adj[i][k][j]]
                for i in range(dimension) for j in range(dimension)}
    for i in range(dimension):
        for j in range(dimension):
            assert all(adj[i][k][j] == -adj[j][k][i] for k in range(dimension))
            for k in range(dimension):
                value = collections.defaultdict(int)
                for a, b, c in [(i, j, k), (j, k, i), (k, i, j)]:
                    for h, v in brackets[a, b]:
                        for z, w in brackets[h, c]:
                            value[z] += v*w
                assert not any(value.values())
    for r in range(nr):
        for i in range(2):
            assert [adj[nr+i][k][r] for k in range(dimension)] == [roots[r][i]*int(k == r) for k in range(dimension)]
        actual = {(i, i): 1 for i in range(dimension)}
        for degree, power in enumerate(powers[r]):
            assert {(i, j): math.factorial(degree)*v for i, row in enumerate(power) for j, v in enumerate(row) if v} == actual
            out = collections.defaultdict(int)
            for (i, h), v in actual.items():
                for j, w in enumerate(adj[r][h]):
                    if w:
                        out[i, j] += v*w
            actual = {k: v for k, v in out.items() if v}
        assert not actual
    print('PASS_1962_RANK_TWO_INTEGRAL_MODEL', label, nr, dimension**3, flush=True)


def run():
    packet = json.loads((ROOT/'results/19.62-rank-two-packet.json').read_text())
    for path, digest in packet['sha256'].items():
        assert sha(ROOT/path) == digest, path
    prior_path = ROOT/'results/19.62-all-types-packet.json'
    prior = json.loads(prior_path.read_text())
    for path, digest in prior['sha256'].items():
        assert sha(ROOT/path) == digest, path
    observation = json.loads((ROOT/'results/19.62-all-types-audit-observation.json').read_text())
    assert observation['exit_code'] == 0 and observation['packet_sha256'] == sha(prior_path)
    assert observation['audit_log_sha256'] == sha(ROOT/'results/19.62-all-types-audit.log')
    jobs = json.loads((ROOT/'results/19.62-rank-two-generation-summary.json').read_text())
    assert [v['type'] for v in jobs] == ['a2', 'b2', 'g2']
    for job, expected in zip(jobs, [6, 20, 78]):
        label = job['type']; assert job['returncode'] == 0
        prefix = 'results/19.62-'+label+'-rank-two-'
        assert job['command'] == ['results/19.62-derive-types', prefix+'input.txt', '1', str(expected), prefix+'certificate.jsonl']
        lines = (ROOT/(prefix+'generation.log')).read_text().splitlines()
        assert len(lines) == expected+1
        assert lines[-1] == 'PASS_1962_MONOMIAL_INTERVAL 1 '+str(expected)+' '+str(expected)+' 0'
        for i, line in enumerate(lines[:-1], 1):
            fields = line.split()
            assert fields[:3] == ['TARGET', str(i), '1'] and len(fields) == 7
        integral_model(label)
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp); Path('results').mkdir(); Path('research').mkdir()
            for label in ['a2', 'b2']:
                name = 'results/19.62-'+label+'-integral.grows'
                shutil.copyfile(ROOT/name, name)
                with contextlib.redirect_stdout(io.StringIO()):
                    old_preparation.prepare(label)
                for suffix in ['json', 'txt']:
                    name = 'results/19.62-'+label+'-monomial-input.'+suffix
                    assert Path(name).read_bytes() == (ROOT/name).read_bytes()
            name = 'results/19.62-g2-monomial-input.json'
            shutil.copyfile(ROOT/name, name)
            with contextlib.redirect_stdout(io.StringIO()):
                preparation.run()
            for label in ['a2', 'b2', 'g2']:
                prefix = 'results/19.62-'+label+'-rank-two-'
                for suffix in ['input.json', 'input.txt']:
                    name = prefix+suffix
                    assert Path(name).read_bytes() == (ROOT/name).read_bytes()
                name = prefix+'certificate.jsonl'; shutil.copyfile(ROOT/name, name)
            with contextlib.redirect_stdout(io.StringIO()):
                rendered = rendering.run()
            assert rendered == json.loads((ROOT/'results/19.62-rank-two-short-summary.json').read_text())
            for label in ['a2', 'b2', 'g2']:
                name = 'results/19.62-'+label+'-rank-two-short-certificate.jsonl'
                assert Path(name).read_bytes() == (ROOT/name).read_bytes()
            name = 'research/19.62-rank-two-derivations.md'
            assert Path(name).read_bytes() == (ROOT/name).read_bytes()
    finally:
        os.chdir(ROOT)
    assert constants.run() == json.loads((ROOT/'results/19.62-g2-integer-constants.json').read_text())
    result = verification.run()
    assert result == json.loads((ROOT/'results/19.62-rank-two-verification.json').read_text())
    assert result['cases'] == 104 and result['derivation_nodes'] == 763
    assert sum(v['short_nodes'] for v in result['types']) == 655
    assert sum(v['representatives'] for v in result['types']) == 19
    print('PASS_1962_RANK_TWO_PACKET', len(packet['sha256']), 'targets=104 short_nodes=655 representatives=19', flush=True)


if __name__ == '__main__':
    run()
