#!/usr/bin/env python3
"""Compile and record a complete literal-data audit; this does not replay GAP mathematics."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    out = ROOT/'results/20.100-data-summary.json'
    assert not out.exists(), 'preserve the recorded audit; replay in a temporary output workspace'
    started = datetime.now(timezone.utc).isoformat()
    begin = time.monotonic()
    source = ROOT/'scripts/check_20_100_data.cpp'
    with tempfile.TemporaryDirectory(prefix='20.100-data-') as directory:
        binary = Path(directory)/'checker'
        command = ['g++', '-O2', '-Wall', '-Wextra', '-Werror', '-std=c++17', str(source),
                   '-lz', '-lcrypto', '-o', str(binary)]
        p = subprocess.run(command, capture_output=True)
        assert p.returncode == 0 and not p.stdout and not p.stderr
        compile_record = {'command': command, 'actual_returncode': p.returncode,
                          'binary_sha256': sha(binary)}
        raw = gzip.decompress((ROOT/'results/20.100-n4-certificate.g.gz').read_bytes())
        bad = {
            'extra_statement': raw.replace(b'StartProof(4,5);', b'StartProof(4,5);ProofN:=2;'),
            'checker_redefinition': raw.replace(b'CheckNode(1,', b'CheckNode:=function()end;CheckNode(1,'),
            'skipped_identifier': raw.replace(b'CheckNode(1,', b'CheckNode(2,'),
            'wrong_prime_bound': raw.replace(b'StartProof(4,5)', b'StartProof(4,4)'),
            'wrong_root': raw.replace(b'FinishProof(227)', b'FinishProof(226)'),
            'trailing_statement': raw+b'QUIT;\n',
            'missing_footer': raw[:raw.rfind(b'FinishProof(')],
            'zero_denominator': raw.replace(b'[1,', b'[1/0,', 1),
            'invalid_list': raw.replace(b'[[', b'[,', 1),
            'scalar_overflow': raw.replace(b'[1,', b'[18446744073709551616,', 1),
            'missing_final_newline': raw[:-1],
        }
        controls = []
        for name, content in bad.items():
            path = Path(directory)/(name+'.g.gz')
            path.write_bytes(gzip.compress(content, mtime=0))
            p = subprocess.run([str(binary), '4', str(path)], capture_output=True)
            assert p.returncode == 1 and not p.stdout and b'invalid certificate data' in p.stderr, name
            controls.append({'name': name, 'actual_returncode': p.returncode,
                             'input_sha256': sha(path)})
        rows = []
        for n in range(4, 8):
            path = ROOT/f'results/20.100-n{n}-certificate.g.gz'
            command = [str(binary), str(n), str(path)]
            stamp = datetime.now(timezone.utc).isoformat()
            clock = time.monotonic()
            p = subprocess.run(command, capture_output=True)
            assert p.returncode == 0 and not p.stderr
            row = json.loads(p.stdout)
            assert row['status'] == 'PASS_DATA_ONLY' and row['n'] == n
            row.update(command=command, actual_returncode=p.returncode,
                       started_utc=stamp, elapsed_seconds=time.monotonic()-clock,
                       compressed_sha256=sha(path), stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),
                       stderr_sha256=hashlib.sha256(p.stderr).hexdigest())
            rows.append(row)
            print(json.dumps(row), flush=True)
    result = {'status': 'PASS_DATA_ONLY', 'started_utc': started,
              'ended_utc': datetime.now(timezone.utc).isoformat(),
              'elapsed_seconds': time.monotonic()-begin, 'source_sha256': sha(source),
              'runner_sha256': sha(Path(__file__)), 'compile': compile_record,
              'rejected_controls': controls, 'certificates': rows,
              'scope': 'Full gzip integrity and strict literal syntax, consecutive node identifiers, '
                       'unique header/footer, and node/leaf/edge counts. Mathematical proof remains '
                       'the separate GAP localized Smith-normal-form verification.'}
    out.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS_20_100_DATA_AUDIT certificates=4 rejected_controls=11', flush=True)


if __name__ == '__main__':
    main()
