#!/usr/bin/env python3
"""Audit the universal completion lemma and the full 19.61 proof packet."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import audit_19_62_rank_two as foundations
import check_19_61_square_completion_finite as finite
import prepare_19_61_square_completion as preparation
import verify_19_61_square_completion as verification

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet = json.loads((ROOT/'results/19.61-square-completion-packet.json').read_text())
    for path, digest in packet['sha256'].items():
        assert sha(ROOT/path) == digest, path
    for name, observation in [('19.62-rank-two-packet', '19.62-rank-two-audit-observation'),
                              ('19.62-derived-packet', '19.62-derived-audit-observation')]:
        path = ROOT/('results/'+name+'.json')
        prior = json.loads(path.read_text())
        for filename, digest in prior['sha256'].items():
            assert sha(ROOT/filename) == digest, filename
        obs = json.loads((ROOT/('results/'+observation+'.json')).read_text())
        assert obs['exit_code'] == 0 and obs['packet_sha256'] == sha(path)
    jobs = json.loads((ROOT/'results/19.61-square-completion-generation-summary.json').read_text())
    assert [v['type'] for v in jobs] == ['a2', 'b2', 'g2']
    for job, count in zip(jobs, [12, 48, 240]):
        label = job['type']; assert job['returncode'] == 0 and job['cases'] == count
        prefix = 'results/19.61-'+label+'-square-completion-'
        assert job['command'] == ['results/19.62-derive-types', prefix+'input.txt', '1', str(count), prefix+'certificate.jsonl']
        lines = (ROOT/(prefix+'generation.log')).read_text().splitlines()
        assert len(lines) == count+1
        assert lines[-1] == 'PASS_1962_MONOMIAL_INTERVAL 1 '+str(count)+' '+str(count)+' 0'
        for i, line in enumerate(lines[:-1], 1):
            fields = line.split()
            assert fields[:3] == ['TARGET', str(i), '1'] and len(fields) == 7
    foundations.run()
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp); Path('results').mkdir()
            for label in ['a2', 'b2', 'g2']:
                name = 'results/19.62-'+label+'-monomial-input.json'
                shutil.copyfile(ROOT/name, name)
            with contextlib.redirect_stdout(io.StringIO()):
                preparation.run()
            for label in ['a2', 'b2', 'g2']:
                for suffix in ['json', 'txt']:
                    name = 'results/19.61-'+label+'-square-completion-input.'+suffix
                    assert Path(name).read_bytes() == (ROOT/name).read_bytes()
    finally:
        os.chdir(ROOT)
    result = verification.run()
    assert result == json.loads((ROOT/'results/19.61-square-completion-verification.json').read_text())
    assert result['cases'] == 300 and result['nodes'] == 3191
    result = finite.run()
    assert result == json.loads((ROOT/'results/19.61-square-completion-finite.json').read_text())
    assert result['carpets'] == 193805
    print('PASS_1961_SQUARE_COMPLETION_PACKET', len(packet['sha256']),
          'targets=300 nodes=3191 finite_carpets=193805', flush=True)


if __name__ == '__main__':
    run()
