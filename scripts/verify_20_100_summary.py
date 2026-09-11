#!/usr/bin/env python3
"""Adversarial controls for status aggregation, using a real n=4 proof run."""
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import tempfile

import summarize_20_100 as reporter


ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT/'results/20.100-n4-runner-control'
expected = next(json.loads(line) for line in (ROOT/'results/20.100-n4-generator.log').read_text().splitlines()
                if 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION' in line)
aggregate = json.loads(Path(str(PREFIX)+'-shards-summary.json').read_text())
digest = aggregate['uncompressed_sha256']
checks = []


def record(name, condition):
    assert condition, name
    checks.append(name)


actual = reporter.inspect_shards(4, expected, digest, PREFIX)
record('actual_three_part_proof', actual['status'] == 'VERIFIED' and actual['relation_implications'] == 3953)
record('actual_single_checker', reporter.summarize_n(4)['relation_implications'] == 3953)

with tempfile.TemporaryDirectory(prefix='20-100-summary-') as directory:
    fixture = Path(directory)
    (fixture/'results').mkdir()
    (fixture/'scripts').mkdir()
    checker = fixture/'scripts/verify_20_100_shard.g'
    shutil.copyfile(ROOT/'scripts/verify_20_100_shard.g', checker)
    certificate = fixture/'results/20.100-n4-certificate.g.gz'
    shutil.copyfile(ROOT/'results/20.100-n4-certificate.g.gz', certificate)
    generator = fixture/'results/20.100-n4-generator.log'
    shutil.copyfile(ROOT/'results/20.100-n4-generator.log', generator)
    prefix = fixture/'results/20.100-n4'
    state_path = Path(str(prefix)+'-shards-state.json')
    summary_path = Path(str(prefix)+'-shards-summary.json')
    state = json.loads(Path(str(PREFIX)+'-shards-state.json').read_text())
    original_logs = {}
    for job in state['jobs']:
        original = Path(job['log']).read_text().splitlines()
        job['log'] = str(fixture/f"part{job['index']}.log")
        job['command'][-2:] = [str(checker), str(certificate)]
        # The current Python PID deliberately does not match the saved GAP command.
        job['pid'] = os.getpid()
        metadata = json.loads(original[0])
        metadata['command'] = job['command']
        original_logs[job['index']] = json.dumps(metadata)+'\n'+'\n'.join(original[1:])+'\n'
    reporter.root = fixture

    def reset():
        state_path.write_text(json.dumps(state))
        summary_path.write_text(json.dumps(aggregate))
        for job in state['jobs']:
            Path(job['log']).write_text(original_logs[job['index']])

    def inspect():
        return reporter.inspect_shards(4, expected, digest, prefix)

    def reject(name):
        try:
            inspect()
        except (AssertionError, ValueError, KeyError, FileNotFoundError):
            checks.append(name)
        else:
            raise AssertionError(f'accepted corrupt evidence: {name}')

    reset()
    record('fixture_replays_verified_counts', inspect()['status'] == 'VERIFIED')
    summary_path.unlink()
    record('all_parts_without_aggregate_not_verified', inspect()['status'] == 'CHECKED_PENDING_AGGREGATION')
    first = Path(state['jobs'][0]['log'])
    first.write_text(original_logs[0].splitlines()[0]+'\n')
    observed = inspect()
    record('partial_parts_not_verified', observed['status'] == 'VERIFICATION_STOPPED'
           and observed['completed_shards'] == 2)
    record('reused_pid_rejected', observed['verified_live_pids'] == [])
    summary_path.write_text(json.dumps(aggregate))
    reject('aggregate_with_missing_part_rejected')

    reset()
    first.write_text(first.read_text()+next(line for line in original_logs[0].splitlines()
                                         if line.startswith('PASS_SHARD'))+'\n')
    reject('duplicate_pass_rejected')
    reset()
    first.write_text(first.read_text().replace('index=0', 'index=1'))
    reject('wrong_partition_rejected')
    reset()
    first.write_text(first.read_text().replace(expected['compressed_sha256'], '0'*64))
    reject('stale_certificate_hash_rejected')
    reset()
    first.write_text(first.read_text()+'Error, deliberate fixture\n')
    reject('error_after_pass_rejected')
    reset()
    bad = deepcopy(aggregate)
    bad['totals']['relation_implications'] += 1
    summary_path.write_text(json.dumps(bad))
    reject('aggregate_count_tampering_rejected')
    reset()
    bad = deepcopy(aggregate)
    bad['uncompressed_sha256'] = '0'*64
    summary_path.write_text(json.dumps(bad))
    reject('uncompressed_hash_tampering_rejected')
    reset()
    checker.write_bytes(checker.read_bytes()+b'\n# changed after run\n')
    reject('changed_checker_rejected')
    shutil.copyfile(ROOT/'scripts/verify_20_100_shard.g', checker)

    reset()
    state_path.unlink()
    reject('aggregate_without_launch_state_rejected')
    summary_path.unlink()
    record('completed_certificate_without_checker_pending',
           reporter.summarize_n(4)['status'] == 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION')
    generator.write_text(json.dumps({'status': 'INCOMPLETE_BOUND_REACHED', 'n': 4,
                                    'prime_bound': 5, 'completed_nodes': 10})+'\n')
    record('bounded_stop_not_verified', reporter.summarize_n(4)['status'] == 'INCOMPLETE_BOUND_REACHED')
    generator.write_text(json.dumps({'states': 10})+'\n')
    record('unexplained_stop_not_verified',
           reporter.summarize_n(4)['status'] == 'GENERATION_STOPPED_WITHOUT_COMPLETION')
    generator.write_text(json.dumps({'status': 'COUNTEREXAMPLE', 'n': 4, 'prime_bound': 5})+'\n')
    record('counterexample_requires_verification',
           reporter.summarize_n(4)['status'] == 'COUNTEREXAMPLE_PENDING_VERIFICATION')

reporter.root = ROOT
summary = {'status': 'PASS', 'controls': checks, 'count': len(checks),
           'scope': 'Status evidence and corruption controls; no new mathematical certificate.'}
(ROOT/'results/20.100-summary-controls.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
