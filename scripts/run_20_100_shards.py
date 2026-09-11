#!/usr/bin/env python3
"""Run every proof-checker shard, then require complete, consistent coverage."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    parser.add_argument('--shards', type=int, default=6)
    parser.add_argument('--workspace-gib', type=int, default=8)
    parser.add_argument('--output-prefix')
    args = parser.parse_args()
    assert 1 <= args.shards <= 10
    assert 1 <= args.workspace_gib <= 32
    assert args.shards*args.workspace_gib <= 84  # <=90.2 GB; allow process overhead below100GB.
    n = args.n
    certificate = ROOT/f'results/20.100-n{n}-certificate.g.gz'
    prefix = Path(args.output_prefix) if args.output_prefix else ROOT/f'results/20.100-n{n}'
    prefix = prefix.resolve()
    generator_log = ROOT/f'results/20.100-n{n}-generator.log'
    print(json.dumps({'status': 'CHECKING_CERTIFICATE_INTEGRITY', 'n': n,
                      'shards': args.shards, 'workspace_gib_each': args.workspace_gib}), flush=True)
    completed = [json.loads(line) for line in generator_log.read_text().splitlines()
                 if line.startswith('{') and 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION' in line]
    assert len(completed) == 1
    expected = completed[0]
    assert expected['n'] == n and expected['prime_bound'] == n+1
    digest = sha256(certificate)
    assert digest == expected['compressed_sha256']
    node_count, uncompressed = 0, hashlib.sha256()
    with gzip.open(certificate, 'rb') as stream:
        first = next(stream)
        assert first == f'StartProof({n},{n+1});\n'.encode()
        uncompressed.update(first)
        for line in stream:
            uncompressed.update(line)
            node_count += line.startswith(b'CheckNode(')
        assert line == f'FinishProof({node_count});\n'.encode()
    assert node_count == expected['states']
    integrity_path = Path(str(prefix)+'-integrity.json')
    assert not integrity_path.exists(), 'preserve any previous integrity report'
    integrity = {'status': 'INTEGRITY_CHECKED_PENDING_MATHEMATICAL_VERIFICATION',
                 'observed_utc': datetime.now(timezone.utc).isoformat(),
                 'n': n, 'prime_bound': n+1, 'states': node_count,
                 'leaves': expected['leaves'], 'edges': expected['edges'],
                 'certificate_sha256': digest, 'uncompressed_sha256': uncompressed.hexdigest(),
                 'shards': args.shards, 'workspace_gib_each': args.workspace_gib}
    integrity_path.write_text(json.dumps(integrity, indent=2)+'\n')
    print(json.dumps(integrity), flush=True)
    processes, handles, jobs = [], [], []
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    checker = ROOT/'scripts/verify_20_100_shard.g'
    checker_digest = sha256(checker)
    state_path = Path(str(prefix)+'-shards-state.json')
    summary_path = Path(str(prefix)+'-shards-summary.json')
    assert not summary_path.exists(), 'preserve any previous completed summary'
    for index in range(args.shards):
        log = Path(f'{prefix}-shard{index}-verifier.log')
        assert not log.exists(), 'preserve previous checker logs; choose another output prefix'
    try:
        for index in range(args.shards):
            log = Path(f'{prefix}-shard{index}-verifier.log')
            handle = log.open('w')
            command = [str(ROOT/'gap-4.16.1/gap'), '-l', str(ROOT/'gap-4.16.1'),
                       '-q', '-b', '-T', '-m', '128m', '-o', f'{args.workspace_gib}g', '-c',
                       f'ProofShardIndex:={index};ProofShardCount:={args.shards};',
                       str(checker), str(certificate)]
            handle.write(json.dumps({'certificate_sha256': digest, 'checker_sha256': checker_digest,
                                     'command': command})+'\n')
            handle.flush()
            process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                       stdout=handle, stderr=subprocess.STDOUT, env=env)
            processes.append(process)
            handles.append(handle)
            jobs.append({'index': index, 'pid': process.pid, 'log': str(log), 'command': command})
        state = {'started_utc': datetime.now(timezone.utc).isoformat(),
                 'jobs': jobs, 'certificate_sha256': digest,
                 'uncompressed_sha256': uncompressed.hexdigest(),
                 'workspace_gib_each': args.workspace_gib,
                 'runner_sha256': sha256(Path(__file__)),
                 'controller_pid': os.getpid(), 'status': 'VERIFYING'}
        state_path.write_text(json.dumps(state, indent=2)+'\n')
        print(json.dumps({'status': 'VERIFYING_SHARDS', 'n': n, 'jobs': jobs}), flush=True)
        for process, job in zip(processes, jobs):
            job['returncode'] = process.wait()
            state_path.write_text(json.dumps(state, indent=2)+'\n')
            assert job['returncode'] == 0
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            process.wait()
        for handle in handles:
            handle.close()
    assert sha256(certificate) == digest and sha256(checker) == checker_digest
    rows = []
    pattern = (r'PASS_SHARD n=\s*(\d+) index=\s*(\d+) shards=\s*(\d+) total_nodes=\s*(\d+) '
               r'checked_nodes=\s*(\d+) leaves=\s*(\d+) edges=\s*(\d+) relation_implications=\s*(\d+)')
    for job in jobs:
        log = Path(job['log']).read_text()
        assert 'Error' not in log and 'Assertion failure' not in log
        metadata = json.loads(log.splitlines()[0])
        assert metadata['certificate_sha256'] == digest and metadata['checker_sha256'] == checker_digest
        matches = re.findall(pattern, ' '.join(log.split()))
        assert log.count('PASS_SHARD') == 1
        assert len(matches) == 1
        values = list(map(int, matches[0]))
        assert values[:4] == [n, job['index'], args.shards, node_count]
        assert values[4] == (node_count+args.shards-1-job['index'])//args.shards
        rows.append(dict(zip(['n', 'index', 'shards', 'total_nodes', 'checked_nodes',
                              'leaves', 'edges', 'relation_implications'], values)))
    totals = {key: sum(row[key] for row in rows)
              for key in ['checked_nodes', 'leaves', 'edges', 'relation_implications']}
    assert [totals['checked_nodes'], totals['leaves'], totals['edges']] == [
        expected['states'], expected['leaves'], expected['edges']]
    summary = {'status': 'VERIFIED', 'n': n, 'prime_bound': n+1,
               'certificate_sha256': digest, 'uncompressed_sha256': uncompressed.hexdigest(),
               'checker_sha256': checker_digest, 'shards': rows, 'totals': totals,
               'completed_utc': datetime.now(timezone.utc).isoformat()}
    summary_path.write_text(json.dumps(summary, indent=2)+'\n')
    state['status'] = 'VERIFIED'
    state['completed_utc'] = summary['completed_utc']
    state_path.write_text(json.dumps(state, indent=2)+'\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
