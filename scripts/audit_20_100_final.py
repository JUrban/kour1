#!/usr/bin/env python3
"""Audit the completed n=7 proof receipts and immutable packet bindings."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT/'results/20.100-n7'
KEYS = ['n', 'index', 'shards', 'total_nodes', 'checked_nodes', 'leaves',
        'edges', 'relation_implications']
TOTALS = dict(checked_nodes=42891332, leaves=5435268, edges=786577344,
              relation_implications=5447182055)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read(suffix):
    return json.loads(Path(str(PREFIX)+suffix).read_text())


def parse_workers(state, aggregate, logs, certificate_hash, checker_hash, runner_hash):
    assert state['status'] == aggregate['status'] == 'VERIFIED'
    assert state['runner_sha256'] == runner_hash
    assert state['certificate_sha256'] == aggregate['certificate_sha256'] == certificate_hash
    assert aggregate['checker_sha256'] == checker_hash
    assert state['uncompressed_sha256'] == aggregate['uncompressed_sha256']
    assert state['completed_utc'] == aggregate['completed_utc']
    assert aggregate['n'] == 7 and aggregate['prime_bound'] == 8
    jobs = state['jobs']
    assert len(jobs) == len(logs) == 6 and [j['index'] for j in jobs] == list(range(6))
    assert state['workspace_gib_each'] == 14
    recorded_root = Path(jobs[0]['command'][0]).parent.parent
    assert recorded_root.is_absolute()
    rows, cpu = [], []
    for job, log in zip(jobs, logs):
        index = job['index']
        assert job.get('returncode') == 0, 'missing or nonzero actual worker exit'
        lines = log.splitlines()
        meta = json.loads(lines[0])
        command = [str(recorded_root/'gap-4.16.1/gap'), '-l', str(recorded_root/'gap-4.16.1'),
                   '-q', '-b', '-T', '-m', '128m', '-o', '14g', '-c',
                   f'ProofShardIndex:={index};ProofShardCount:=6;',
                   str(recorded_root/'scripts/verify_20_100_shard.g'),
                   str(recorded_root/'results/20.100-n7-certificate.g.gz')]
        assert meta['command'] == job['command'] == command
        assert meta['certificate_sha256'] == certificate_hash
        assert meta['checker_sha256'] == checker_hash
        assert job['log'] == str(recorded_root/f'results/20.100-n7-shard{index}-verifier.log')
        # Consume every token: a trailing warning/error cannot be hidden by a PASS.
        body = ' '.join(' '.join(lines[1:]).split())
        header = 'START n=7 prime_bound=8 '
        assert body.startswith(header)
        pos, checked, last_edges, last_cpu = len(header), 0, 0, 0
        progress = re.compile(r'CHECK_SHARD index=\s*(\d+) nodes=\s*(\d+) last_id=\s*(\d+) '
                              r'edges=\s*(\d+) cpu_ms=\s*(\d+) ')
        while (match := progress.match(body, pos)):
            i, count, identifier, edges, runtime = map(int, match.groups())
            assert i == index and count == checked+10000
            assert identifier == (count-1)*6+index+1
            assert edges >= last_edges and runtime >= last_cpu
            pos, checked, last_edges, last_cpu = match.end(), count, edges, runtime
        terminal = re.fullmatch(
            r'PASS_SHARD n=\s*(\d+) index=\s*(\d+) shards=\s*(\d+) total_nodes=\s*(\d+) '
            r'checked_nodes=\s*(\d+) leaves=\s*(\d+) edges=\s*(\d+) '
            r'relation_implications=\s*(\d+) cpu_ms=\s*(\d+)', body[pos:])
        assert terminal, 'missing completion or unexpected log content'
        values = list(map(int, terminal.groups()))
        assert values[:4] == [7, index, 6, TOTALS['checked_nodes']]
        assert values[4] == (TOTALS['checked_nodes']+5-index)//6
        assert checked == values[4]//10000*10000
        assert values[6] >= last_edges and values[8] >= last_cpu
        assert values[6] == (values[4]-values[5])*21
        rows.append(dict(zip(KEYS, values[:8])))
        cpu.append(values[8])
    totals = {k: sum(row[k] for row in rows) for k in TOTALS}
    assert aggregate['shards'] == rows and aggregate['totals'] == totals == TOTALS
    return dict(totals=totals, worker_actual_exits=[0]*6, worker_cpu_ms=cpu)


def process(prefix, marker=None):
    base = ROOT/('results/'+prefix)
    rec = json.loads(Path(str(base)+'-process.json').read_text())
    stdout, stderr = Path(str(base)+'.log'), Path(str(base)+'.stderr')
    assert rec['actual_returncode'] == 0
    assert sha(stdout) == rec['stdout_sha256'] and sha(stderr) == rec['stderr_sha256']
    assert not stderr.read_bytes()
    if marker:
        assert rec['sentinel_seen'] and stdout.read_text().count(marker) == 1
    return stdout.read_text()


def summarize():
    state, aggregate = read('-shards-state.json'), read('-shards-summary.json')
    logs = [Path(str(PREFIX)+f'-shard{i}-verifier.log').read_text() for i in range(6)]
    hashes = [sha(Path(str(PREFIX)+'-certificate.g.gz')),
              sha(ROOT/'scripts/verify_20_100_shard.g'), sha(ROOT/'scripts/run_20_100_shards.py')]
    result = parse_workers(state, aggregate, logs, *hashes)
    controls = []
    def reject(name, change):
        s, a, l = copy.deepcopy(state), copy.deepcopy(aggregate), list(logs)
        change(s, a, l)
        try:
            parse_workers(s, a, l, *hashes)
        except (AssertionError, KeyError, IndexError, ValueError):
            controls.append(name)
        else:
            raise AssertionError('accepted corruption: '+name)
    reject('nonzero_worker_exit', lambda s,a,l: s['jobs'][4].update(returncode=143))
    reject('missing_worker_exit', lambda s,a,l: s['jobs'][4].pop('returncode'))
    reject('missing_worker', lambda s,a,l: s['jobs'].pop())
    reject('duplicate_part', lambda s,a,l: s['jobs'][4].update(index=3))
    reject('wrong_aggregate_count', lambda s,a,l: a['totals'].update(relation_implications=1))
    reject('wrong_command_partition', lambda s,a,l: s['jobs'][4]['command'].__setitem__(-3, 'ProofShardIndex:=3;ProofShardCount:=6;'))
    reject('trailing_warning', lambda s,a,l: l.__setitem__(0,l[0]+'Syntax warning: test\n'))
    reject('wrong_progress_identifier', lambda s,a,l: l.__setitem__(0,l[0].replace('last_id=59995','last_id=59996',1)))
    reject('stale_certificate', lambda s,a,l: s.update(certificate_sha256='0'*64))
    report = json.loads(process('20.100-n7-final-report'))
    assert report['results'] == json.loads((ROOT/'results/20.100-summary.json').read_text())['results']
    assert [x['n'] for x in report['results']] == [4,5,6,7]
    assert all(x['status'] == 'VERIFIED' for x in report['results'])
    assert report['results'][-1]['relation_implications'] == TOTALS['relation_implications']
    process('20.100-data-audit', 'PASS_20_100_DATA_AUDIT')
    data = json.loads((ROOT/'results/20.100-data-summary.json').read_text())
    assert data['status'] == 'PASS_DATA_ONLY' and len(data['rejected_controls']) == 11
    assert data['source_sha256'] == sha(ROOT/'scripts/check_20_100_data.cpp')
    assert data['runner_sha256'] == sha(ROOT/'scripts/run_20_100_data.py')
    assert data['compile']['actual_returncode'] == 0
    assert [x['n'] for x in data['certificates']] == [4,5,6,7]
    for row, prior in zip(data['certificates'], report['results']):
        assert row['status'] == 'PASS_DATA_ONLY' and row['actual_returncode'] == 0
        assert row['stderr_sha256'] == hashlib.sha256(b'').hexdigest()
        assert row['nodes'] == prior['states'] and row['leaves'] == prior['leaves']
        assert row['edges'] == prior['edges'] and row['uncompressed_sha256'] == prior['uncompressed_sha256']
        assert row['compressed_sha256'] == sha(ROOT/f'results/20.100-n{row["n"]}-certificate.g.gz')
    assert data['certificates'][-1]['uncompressed_sha256'] == aggregate['uncompressed_sha256']
    result.update(rejected_aggregation_controls=controls, rejected_data_controls=11,
                  certificate_uncompressed_bytes=data['certificates'][-1]['uncompressed_bytes'],
                  mathematical_scope='20.100 holds for every eligible group at n=7; arbitrary n unresolved',
                  new_complete_candidates_added=0, outside_reviews=0)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--summary-only', action='store_true')
    args = parser.parse_args()
    summary = summarize()
    if args.summary_only:
        print(json.dumps(summary, indent=2))
        return
    packet = json.loads((ROOT/'results/20.100-final-packet.json').read_text())
    assert packet['summary'] == summary
    assert len({row['path'] for row in packet['files']}) == len(packet['files'])
    for row in packet['files']:
        path = ROOT/row['path']
        assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], path
    print(f'PASS_20_100_FINAL_PACKET files={len(packet["files"])} n=7 nodes=42891332 '
          'relation_implications=5447182055 worker_exits=0,0,0,0,0,0 rejected_controls=20')


if __name__ == '__main__':
    main()
