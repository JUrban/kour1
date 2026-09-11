#!/usr/bin/env python3
"""Validate completed certificate counts and identify live jobs by command+stdout."""
from datetime import datetime, timezone
from pathlib import Path
import gzip
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def recorded_job_is_live(job):
    """A saved PID is evidence only if its current command and stdout agree."""
    entry = Path('/proc')/str(job['pid'])
    try:
        command = (entry/'cmdline').read_bytes().rstrip(b'\0').split(b'\0')
        return (command == [part.encode() for part in job['command']]
                and (entry/'fd/1').resolve() == Path(job['log']).resolve())
    except (OSError, FileNotFoundError, PermissionError):
        return False


def inspect_shards(n, expected, uncompressed_digest, prefix):
    """Replay aggregation evidence; no individual PASS_SHARD is a proof."""
    state_path = Path(str(prefix)+'-shards-state.json')
    summary_path = Path(str(prefix)+'-shards-summary.json')
    if not state_path.exists():
        assert not summary_path.exists(), 'aggregate without launch provenance'
        return None
    state = json.loads(state_path.read_text())
    jobs = state['jobs']
    assert 1 <= len(jobs) <= 10
    assert [job['index'] for job in jobs] == list(range(len(jobs)))
    certificate = root/f'results/20.100-n{n}-certificate.g.gz'
    digest = expected['compressed_sha256']
    assert state['certificate_sha256'] == digest
    checker = root/'scripts/verify_20_100_shard.g'
    checker_digest = sha256(checker)
    rows, live, stopped = [], [], []
    pattern = (r'PASS_SHARD n=\s*(\d+) index=\s*(\d+) shards=\s*(\d+) total_nodes=\s*(\d+) '
               r'checked_nodes=\s*(\d+) leaves=\s*(\d+) edges=\s*(\d+) relation_implications=\s*(\d+)')
    keys = ['n', 'index', 'shards', 'total_nodes', 'checked_nodes',
            'leaves', 'edges', 'relation_implications']
    for job in jobs:
        log = Path(job['log']).read_text()
        assert 'Error' not in log and 'Assertion failure' not in log
        metadata = json.loads(log.splitlines()[0])
        assert metadata['certificate_sha256'] == digest
        assert metadata['checker_sha256'] == checker_digest
        assert metadata['command'] == job['command']
        command = job['command']
        assert command[-2:] == [str(checker), str(certificate)]
        assert command[-4:-2] == ['-c', f"ProofShardIndex:={job['index']};ProofShardCount:={len(jobs)};"]
        matches = re.findall(pattern, ' '.join(log.split()))
        assert log.count('PASS_SHARD') <= 1, 'duplicate or trailing partial completion marker'
        assert len(matches) <= 1, 'duplicate completion marker'
        if matches:
            values = list(map(int, matches[0]))
            assert values[:4] == [n, job['index'], len(jobs), expected['states']]
            assert values[4] == (expected['states']+len(jobs)-1-job['index'])//len(jobs)
            rows.append(dict(zip(keys, values)))
        elif recorded_job_is_live(job):
            live.append(job['pid'])
        else:
            stopped.append(job['index'])
    item = {'verifier_mode': 'sharded', 'shard_count': len(jobs),
            'completed_shards': len(rows), 'verified_live_pids': live}
    if summary_path.exists():
        aggregate = json.loads(summary_path.read_text())
        assert len(rows) == len(jobs), 'aggregate claims incomplete coverage'
        totals = {key: sum(row[key] for row in rows)
                  for key in ['checked_nodes', 'leaves', 'edges', 'relation_implications']}
        assert [totals['checked_nodes'], totals['leaves'], totals['edges']] == [
            expected['states'], expected['leaves'], expected['edges']]
        assert aggregate['status'] == 'VERIFIED'
        assert aggregate['n'] == n and aggregate['prime_bound'] == n+1
        assert aggregate['certificate_sha256'] == digest
        assert aggregate['uncompressed_sha256'] == uncompressed_digest
        assert aggregate['checker_sha256'] == checker_digest
        assert aggregate['shards'] == rows and aggregate['totals'] == totals
        item.update(status='VERIFIED', relation_implications=totals['relation_implications'],
                    aggregate_path=str(summary_path))
    elif stopped:
        item.update(status='VERIFICATION_STOPPED', stopped_shards=stopped)
    elif len(rows) == len(jobs):
        item['status'] = 'CHECKED_PENDING_AGGREGATION'
    else:
        item['status'] = 'VERIFYING'
    return item


def live_job(argument, logfile):
    matches = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            command = (entry/'cmdline').read_bytes().split(b'\0')
            if argument.encode() not in command:
                continue
            if not str((entry/'fd/1').resolve()) == str(logfile.resolve()):
                continue
            matches.append(int(entry.name))
        except (OSError, FileNotFoundError, PermissionError):
            pass
    return matches


def summarize_n(n):
    generator_path = root/f'results/20.100-n{n}-generator.log'
    verifier_path = root/f'results/20.100-n{n}-verifier.log'
    certificate = root/f'results/20.100-n{n}-certificate.g.gz'
    generated = []
    for line in generator_path.read_text().splitlines():
        try:
            generated.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    completed = next((row for row in reversed(generated)
                      if row.get('status') == 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION'), None)
    item = {'n': n}
    if completed:
        assert completed['n'] == n and completed['prime_bound'] == n+1
        assert sha256(certificate) == completed['compressed_sha256']
        count, digest, final = 0, hashlib.sha256(), b''
        with gzip.open(certificate, 'rb') as stream:
            first = next(stream)
            assert first == f'StartProof({n},{n+1});\n'.encode()
            digest.update(first)
            for line in stream:
                digest.update(line)
                count += line.startswith(b'CheckNode(')
                final = line
        assert count == completed['states']
        assert final == f'FinishProof({count});\n'.encode()
        item.update({key: completed[key] for key in ['states', 'leaves', 'edges']})
        item['uncompressed_sha256'] = digest.hexdigest()
        shards = inspect_shards(n, completed, digest.hexdigest(),
                                root/f'results/20.100-n{n}')
        if shards is not None:
            item.update(shards)
            return item
        log = verifier_path.read_text() if verifier_path.exists() else ''
        assert 'Error,' not in log and 'Assertion failure' not in log
        matches = re.findall(r'PASS n=(\d+) nodes=(\d+) leaves=(\d+) edges=(\d+) relation_implications=\s*(\d+)', log)
        assert len(matches) <= 1
        if matches:
            assert list(map(int, matches[0][:4])) == [n, count, completed['leaves'], completed['edges']]
            item['relation_implications'] = int(matches[0][4])
            item['status'] = 'VERIFIED'
        else:
            pids = live_job(f'results/20.100-n{n}-certificate.g.gz', verifier_path)
            item.update(status='VERIFYING' if pids else 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION',
                        verified_live_pids=pids)
    else:
        pids = live_job(f'results/20.100-n{n}-certificate.g.gz', generator_path)
        last_status = generated[-1].get('status') if generated else None
        if pids:
            item.update(status='GENERATING', verified_live_pids=pids)
        elif last_status in {'INCOMPLETE_BOUND_REACHED', 'COUNTEREXAMPLE'}:
            assert generated[-1]['n'] == n and generated[-1]['prime_bound'] == n+1
            item['status'] = ('COUNTEREXAMPLE_PENDING_VERIFICATION'
                              if last_status == 'COUNTEREXAMPLE' else last_status)
        else:
            item['status'] = 'GENERATION_STOPPED_WITHOUT_COMPLETION'
        if generated:
            item['last_progress'] = generated[-1]
    return item

def main():
    results = [summarize_n(n) for n in [4, 5, 6, 7]]
    summary = {'observed_utc': datetime.now(timezone.utc).isoformat(), 'results': results,
               'all_log_checks_pass': True}
    (root/'results/20.100-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
