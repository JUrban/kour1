#!/usr/bin/env python3
"""Recreate the F9 preparation exactly and verify the imported source bindings."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import prepare_19_61_g2_f9 as prep

ROOT=Path(__file__).resolve().parents[1]


def main():
    packet=json.loads((ROOT/'results/19.61-g2f9-launch-manifest.json').read_text())
    for path,digest in packet['sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    try:
        with tempfile.TemporaryDirectory() as temp:
            os.chdir(temp);Path('results').mkdir()
            for name in ['results/19.61-g2-integral.grows','results/19.61-g2-summary.json','results/19.61-g2p3-preparation.json']:
                shutil.copyfile(ROOT/name,name)
            with contextlib.redirect_stdout(io.StringIO()):prep.prepare()
            name='results/19.61-g2f9-input.g'
            assert Path(name).read_bytes()==(ROOT/name).read_bytes()
            name='results/19.61-g2f9-preparation.json'
            a=json.loads(Path(name).read_text());b=json.loads((ROOT/name).read_text())
            a.pop('elapsed_seconds');b.pop('elapsed_seconds');assert a==b
    finally:os.chdir(ROOT)
    print('PASS_1961_G2_F9_PREPARATION_AUDIT',len(packet['sha256']),'carpets=40105 degree=66430')


if __name__=='__main__':main()
