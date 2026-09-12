#!/usr/bin/env python3
"""Hash audit and full isolated replay of the Z/9 congruence calculation."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import check_19_61_g2_z9 as controls
import kernels_19_61_g2_z9 as kernels
import matrices_19_61_mod9 as matrices
import prepare_19_61_g2_z9 as prepare
import search_19_61_g2_z9 as search

ROOT=Path(__file__).resolve().parents[1]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet=json.loads((ROOT/'results/19.61-g2z9-summary.json').read_text())
    for path,h in packet['sha256'].items():assert sha(ROOT/path)==h,path
    for name in ['results/19.61-g2z9-launch-manifest.json','results/19.61-g2-summary.json']:
        prior=json.loads((ROOT/name).read_text())
        for path,h in prior['sha256'].items():assert sha(ROOT/path)==h,path
    obs=json.loads((ROOT/'results/19.61-g2z9-process-observations.json').read_text())
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in obs['successful_processes'])
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir();Path('scripts').mkdir()
            for name in ['results/19.61-g2-integral.grows','results/19.61-g2-summary.json',
                         'results/19.61-g2p3-input.g','results/19.61-g2p3-orders.grows',
                         'results/19.61-matrices-mod9.so','scripts/matrices_19_61_mod9.c']:
                shutil.copyfile(ROOT/name,name)
            assert matrices.controls()==json.loads((ROOT/'results/19.61-mod9-native-controls.json').read_text())
            for task,name in [(prepare.run,'input'),(kernels.run,'unit-kernels'),(search.run,'search')]:
                with contextlib.redirect_stdout(io.StringIO()):task()
                path=Path('results/19.61-g2z9-'+name+'.json')
                actual=json.loads(path.read_text());expected=json.loads((ROOT/path).read_text())
                actual.pop('elapsed_seconds');expected.pop('elapsed_seconds');assert actual==expected,name
                # Restore the matched original's bytes so dependent hashes compare exactly.
                shutil.copyfile(ROOT/path,path)
                print('PASS_1961_Z9_REPLAY',name,flush=True)
            actual=json.loads(json.dumps(controls.run()))
            assert actual==json.loads((ROOT/'results/19.61-g2z9-controls.json').read_text())
            result=json.loads(Path('results/19.61-g2z9-search.json').read_text())
            assert result['carpets']==20047 and result['expanded']==0 and result['failures']==[]
            assert len(result['rows'])==20047
    finally:os.chdir(ROOT)
    print('PASS_1961_Z9_PACKET',len(packet['sha256']),'carpets=20047 expanded=0 controls=219',flush=True)


if __name__=='__main__':run()
