#!/usr/bin/env python3
"""Audit degree coverage, exact archives and actual proof runs; optional replay."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process(name,sentinel):
    base = ROOT/('results/21.99-'+name)
    record = json.loads(Path(str(base)+'-process.json').read_text())
    stdout,stderr = Path(str(base)+'.log'),Path(str(base)+'.stderr')
    assert record['actual_returncode'] == 0 and record['sentinel_seen']
    assert sha(stdout) == record['stdout_sha256'] and sha(stderr) == record['stderr_sha256']
    assert not stderr.read_bytes() and stdout.read_text().count(sentinel) == 1
    return record,stdout.read_text()


def archive(row):
    path = ROOT/row['path']
    assert sha(path) == row['sha256'] and path.stat().st_size == row['bytes']
    raw_hash = hashlib.sha256(); size = 0
    with gzip.open(path,'rb') as stream:
        while chunk := stream.read(1<<20):
            raw_hash.update(chunk); size += len(chunk)
    assert raw_hash.hexdigest() == row['raw_sha256'] and size == row['raw_bytes']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    args = parser.parse_args()
    packet = json.loads((ROOT/'results/21.99-words-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 0
    def bindings():
        assert len({x['path'] for x in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],path
    bindings()
    stages = [('words-census','PASS_2199_CENSUS'),('words-pilot','PASS_2199_WORD_PILOT'),
              ('words-pilot-python','PASS_2199_WORD_INDEPENDENT'),
              ('words-controller','PASS_2199_WORD_SHARD_RUNNER'),
              ('words-compression','PASS_2199_WORD_ARCHIVES'),
              ('words-extension-python','PASS_2199_WORD_INDEPENDENT'),
              ('words-archive-python','PASS_2199_WORD_ARCHIVE_INDEPENDENT'),
              ('muller-python','PASS_2199_MULLER')]
    for name,sentinel in stages:
        process(name,sentinel)
    census = json.loads((ROOT/'results/21.99-words-census.json').read_text())
    def non_prime_power(n):
        factors = []
        for p in range(2,n+1):
            if n % p == 0:
                factors.append(p)
                while n % p == 0:
                    n //= p
        return len(factors)>1
    assert [n for n,count in census] == [n for n in range(2,48) if non_prime_power(n)]
    assert sum(count for n,count in census) == 496284
    state = json.loads((ROOT/'results/21.99-words-shards-state.json').read_text())
    archives = json.loads((ROOT/'results/21.99-words-archives.json').read_text())['archives']
    assert len(state['jobs']) == len(archives) == 8
    for i,row in enumerate(archives):
        assert row['shard'] == i
        record,log = process(f'words-shard{i}','PASS_2199_WORD_SHARD ')
        assert record == state['jobs'][i]
        assert record['shard'] == i and record['shards'] == 8
        assert record['certificate_sha256'] == row['raw_sha256']
        assert record['certificate_bytes'] == row['raw_bytes']
        assert not (ROOT/f'results/21.99-words-shard{i}-unresolved.jsonl').read_bytes()
        done = [json.loads(x) for x in re.findall(r'^DEGREE_DONE (\[.*\])$',log,re.M)]
        expected = [[n,count,len(range(i+1,count+1,8)),0] for n,count in census]
        assert done == expected
        end = re.findall(r'^PASS_2199_WORD_SHARD (\[.*\])$',log,re.M)
        assert len(end) == 1 and json.loads(end[0]) == [i,8,sum(x[2] for x in expected),0]
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(archive,archives))
    raw = json.loads((ROOT/'results/21.99-words-extension-controls.json').read_text())
    zipped = json.loads((ROOT/'results/21.99-words-archive-controls.json').read_text())
    for key in ['counts','degrees','fixed_counts','max_random_steps']:
        assert raw[key] == zipped[key],key
    assert raw['counts']['groups'] == 496284 and raw['counts']['witnesses'] == 18404612
    assert dict(raw['degrees']) == dict(census)
    assert sum(n for fixed,n in raw['fixed_counts']) == 18404612
    assert all(fixed != 1 for fixed,n in raw['fixed_counts'])
    mutation_names = ['generator','forward_reference','target','fixed_count','missing_witness']
    assert raw['rejected_mutations'] == mutation_names
    assert zipped['rejected_mutations'] == [mutation_names]*8
    pilot = json.loads((ROOT/'results/21.99-words-pilot-controls.json').read_text())
    assert pilot['counts'] == dict(circuit_nodes=9248,groups=485,input_generators=1602,
                                  point_multiplications=117153,witnesses=4833)
    assert pilot['rejected_mutations'] == mutation_names
    muller = json.loads((ROOT/'results/21.99-muller-controls.json').read_text())
    assert muller['distinct_fixed_cosets'] == 2 and muller['subgroup_order'] == 52
    assert muller['field_associativity_triples'] == muller['field_distributivity_triples'] == 512
    probe = json.loads((ROOT/'results/21.99-factorization-probe.json').read_text())
    assert probe['actual_returncode'] == 0 and not probe['accepted']
    assert 'memory limit' in probe['combined_tool_output']
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='21.99-word-replay-') as directory:
            (Path(directory)/'results').mkdir()
            (Path(directory)/'scripts').symlink_to(ROOT/'scripts',target_is_directory=True)
            p = subprocess.run([str(ROOT/'bin/gap'),'-o','3g',str(ROOT/'scripts/pilot_21_99_words.g')],
                               cwd=directory,capture_output=True,timeout=60)
            assert p.returncode == 0 and not p.stderr
            assert p.stdout == (ROOT/'results/21.99-words-pilot.log').read_bytes()
            assert (Path(directory)/'results/21.99-words-pilot-certificate.jsonl').read_bytes() == (
                ROOT/'results/21.99-words-pilot-certificate.jsonl').read_bytes()
        for script,name in [('verify_21_99_archives.py','words-archive-python'),
                            ('check_21_99_muller.py','muller-python')]:
            p = subprocess.run(['python3','scripts/'+script],cwd=ROOT,capture_output=True,timeout=300)
            assert p.returncode == 0 and not p.stderr
            assert p.stdout == (ROOT/('results/21.99-'+name+'.log')).read_bytes()
    bindings()
    print('PASS_2199_WORD_PACKET files=%d groups=496284 witnesses=18404612 '
          'prime_power_degrees=theoretical degree_bound=47 replay=%s new_complete_candidates=0' %
          (len(packet['files']),str(args.replay).lower()))


if __name__ == '__main__':
    main()
