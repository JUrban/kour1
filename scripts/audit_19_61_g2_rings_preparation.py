#!/usr/bin/env python3
"""Recreate all finite-ring inputs and repeat the exact enumeration controls."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import carpet_horn_19_61 as horn
import prepare_19_61_g2_rings as prep

ROOT=Path(__file__).resolve().parents[1]


def main():
    manifest=json.loads((ROOT/'results/19.61-g2-rings-launch-manifest.json').read_text())
    for path,digest in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    replay=horn.controls();old=json.loads((ROOT/'results/19.61-horn-controls.json').read_text())
    for data in [replay,old]:
        for row in data['rings']:row.pop('elapsed_seconds')
    assert replay==old
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir()
            for name in ['results/19.61-g2-integral.grows','results/19.61-g2-summary.json']:
                shutil.copyfile(ROOT/name,name)
            for label in ['f4','dual','split','z4']:
                with contextlib.redirect_stdout(io.StringIO()):prep.prepare(label)
                name=f'results/19.61-g2{label}-input.g'
                assert Path(name).read_bytes()==(ROOT/name).read_bytes()
                name=f'results/19.61-g2{label}-preparation.json'
                a=json.loads(Path(name).read_text());b=json.loads((ROOT/name).read_text())
                a.pop('elapsed_seconds');b.pop('elapsed_seconds');assert a==b
                print('PASS_1961_G2_RING_REPLAY',label,flush=True)
    finally:os.chdir(ROOT)
    print('PASS_1961_G2_RINGS_PREPARATION_AUDIT',len(manifest['sha256']),'carpets=135700')


if __name__=='__main__':main()
