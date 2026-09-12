#!/usr/bin/env python3
"""Bind the 20.122 proof, successful computations, and explicitly stopped pilot."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ORDERS = [24,36,48,54,60,72,96,108,120,144,162]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt(name,command,marker,accepted=True):
    stem = ROOT/('results/20.122-'+name)
    rec = json.loads(Path(str(stem)+'-process.json').read_text())
    out,err = Path(str(stem)+'.log'),Path(str(stem)+'.stderr')
    assert rec['command'] == command
    assert sha(out) == rec['stdout_sha256'] and sha(err) == rec['stderr_sha256']
    observed = rec['actual_returncode'] == 0 and not err.read_bytes() and out.read_bytes().count(marker)==1
    observed = observed and not rec.get('bounded_stop',False)
    assert bool(observed) == accepted
    if 'accepted' in rec: assert rec['accepted'] == accepted
    if 'sentinel_seen' in rec: assert rec['sentinel_seen'] == (marker in out.read_bytes())
    return rec,out.read_text()


def summarize():
    _,out = receipt('native',['bin/gap','-o','2g','scripts/verify_20_122_native.g'],
                    b'PASS_20_122_NATIVE pairs=2304')
    m = re.fullmatch(r'\s*NATIVE_20122\s*(\[.*\])\s*PASS_20_122_NATIVE pairs=2304\s*',out,re.S)
    assert m and json.loads(m[1]) == [48,[16,8,8],3,3,[2,2,2,2,2,4],16,8]
    _,out = receipt('independent',['python3','scripts/verify_20_122_permutations.py'],
                    b'PASS_20_122_PERMUTATIONS rejected_corruptions=5')
    independent = json.loads((ROOT/'results/20.122-permutations-summary.json').read_text())
    assert json.loads(out.splitlines()[0]) == independent
    assert independent['status'] == 'PASS'
    assert independent['all_subgroups'] == 98 and independent['conjugating_pairs'] == 2304
    assert independent['Min_order'] == 16 and independent['min_order'] == independent['fitting_order'] == 8
    statement = json.loads((ROOT/'results/20.122-statement.json').read_text())
    assert statement['id'] == '20.122' and statement['pdf_page'] == 165
    assert not statement['starred_heading'] and not statement['contains_editorial_star']
    assert 'minimal by inclusion' in statement['text'] and 'minimal order' in statement['text']

    totals = {}; hits = 0; hit_groups = set(); rows = []
    for n in ORDERS:
        export,_ = receipt(f'order{n}-export',['bin/gap','-o','2g',f'results/20.122-order{n}-input.g'],
                            f'PASS_20_122_EXPORT order={n} '.encode())
        command = ['python3','scripts/screen_20_122.py',f'results/20.122-order{n}-models.json',
                   f'results/20.122-order{n}-summary.json']
        screen,out = receipt(f'order{n}-screen',command,f'PASS_20_122_SCREEN order={n} '.encode())
        d = json.loads((ROOT/command[3]).read_text())
        assert d['status'] == 'COMPLETE_SUPPLIED_FAMILIES' and d['order'] == n
        assert json.loads(out.splitlines()[0]) == {k:v for k,v in d.items() if k != 'group_rows'}
        models = json.loads((ROOT/command[2]).read_text())
        assert [g['id'] for g in models['groups']] == list(range(1,models['catalogue_count']+1))
        assert models['catalogue_count'] == d['stats']['catalogue_groups']
        assert not any(h['outside_minimum_order'] for h in d['hits'])
        hits += len(d['hits']); hit_groups |= {(n,h['id']) for h in d['hits']}
        for k,v in d['stats'].items(): totals[k] = totals.get(k,0)+v
        rows.append([n,d['stats']['catalogue_groups'],d['stats']['total_families'],len(d['hits'])])
    assert totals['catalogue_groups'] == 734 and totals['total_families'] == 19715203
    assert hits == 641 and len(hit_groups) == 15
    failed,_ = receipt('order192-export',['bin/gap','-o','2g','results/20.122-order192-input.g'],
                       b'PASS_20_122_EXPORT order=192 ',False)
    assert failed['actual_returncode'] == 1 and failed['bounded_stop'] and failed['timeout_seconds'] == 180
    assert not (ROOT/'results/20.122-order192-summary.json').exists()
    receipt('diagnose-grouped-option-failed',['bin/gap','-o2g','results/20.122-diagnose.g'],
            b'PASS_20_122_DIAGNOSE',False)
    receipt('diagnose',['bin/gap','-o','2g','results/20.122-diagnose.g'],b'PASS_20_122_DIAGNOSE')
    controller = json.loads((ROOT/'results/20.122-pilot-processes.json').read_text())
    assert controller['orders'] == ORDERS[1:]+[192]
    assert [r['order'] for r in controller['rows'] if r['complete']] == ORDERS[1:]
    assert controller['max_workers'] == 4 and controller['per_process_address_limit'] == 8*1024**3
    for row in controller['rows']:
        n = row['order']
        assert row['export'] == json.loads((ROOT/f'results/20.122-order{n}-export-process.json').read_text())
        if row['complete']:
            assert row['screen'] == json.loads((ROOT/f'results/20.122-order{n}-screen-process.json').read_text())
            d = json.loads((ROOT/f'results/20.122-order{n}-summary.json').read_text())
            assert row['stats'] == d['stats'] and row['hits'] == d['hits']
    return dict(independent=independent,pilot_rows=rows,pilot_totals=totals,
                inclusion_failure_families=hits,inclusion_failure_groups=sorted(map(list,hit_groups)),
                minimum_order_failure_families=0,excluded_incomplete_orders=[192])


def main():
    p = argparse.ArgumentParser(); p.add_argument('--summary-only',action='store_true')
    p.add_argument('--replay',action='store_true'); args = p.parse_args()
    summary = summarize()
    if args.summary_only:
        print(json.dumps(summary,indent=2)); return
    packet = json.loads((ROOT/'results/20.122-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 1
    assert packet['outside_reviews'] == 0 and packet['priority_established'] is False
    assert packet['summary'] == summary

    def bindings():
        assert len({x['path'] for x in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], path

    bindings()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='20.122-replay-') as directory:
            temporary = Path(directory); (temporary/'results').mkdir()
            native = subprocess.run([str(ROOT/'bin/gap'),'-o','2g',str(ROOT/'scripts/verify_20_122_native.g')],
                                    cwd=temporary,capture_output=True,timeout=60)
            assert native.returncode == 0 and not native.stderr
            assert native.stdout == (ROOT/'results/20.122-native.log').read_bytes()
            assert (temporary/'results/20.122-native-model.json').read_bytes() == (ROOT/'results/20.122-native-model.json').read_bytes()
            independent = subprocess.run(['python3',str(ROOT/'scripts/verify_20_122_permutations.py')],
                                         cwd=ROOT,capture_output=True,timeout=60)
            assert independent.returncode == 0 and not independent.stderr
            assert independent.stdout == (ROOT/'results/20.122-independent.log').read_bytes()
            for n in ORDERS:
                output = temporary/f'order{n}-summary.json'
                screen = subprocess.run(['python3',str(ROOT/'scripts/screen_20_122.py'),
                    str(ROOT/f'results/20.122-order{n}-models.json'),str(output)],capture_output=True,timeout=180)
                assert screen.returncode == 0 and not screen.stderr
                assert screen.stdout == (ROOT/f'results/20.122-order{n}-screen.log').read_bytes()
                assert output.read_bytes() == (ROOT/f'results/20.122-order{n}-summary.json').read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS',files=len(packet['files']),replay=args.replay,
                          group_order=48,pilot_families=summary['pilot_totals']['total_families']),sort_keys=True))
    print('PASS_20_122_PACKET')


if __name__ == '__main__': main()
