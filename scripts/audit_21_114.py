#!/usr/bin/env python3
"""Audit the bounded screen and independently replay the central-product inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process(name, sentinel):
    base = ROOT/('results/21.114-'+name)
    rec = json.loads(Path(str(base)+'-process.json').read_text())
    out, err = Path(str(base)+'.log'), Path(str(base)+'.stderr')
    assert rec['actual_returncode'] == 0 and rec['sentinel_seen']
    assert sha(out) == rec['stdout_sha256'] and sha(err) == rec['stderr_sha256']
    assert not err.read_bytes() and out.read_text().count(sentinel) == 1
    return out.read_text()


def summarize():
    log = process('pilot', 'PASS_21114_PILOT')
    rows = []
    witnesses = []
    for match in re.finditer(r'ROW114\s*(\[[^\]]*\])(?:\s*WITNESS\s*(\[[^\]]*\]))?', log):
        row = json.loads(match[1])
        rows.append(row)
        if not row[5]:
            witness = json.loads(match[2])
            assert witness[1] > row[4] and witness[0] >= witness[1]
            witnesses.append(witness)
        else:
            assert match[2] is None
    orders = {64:267, 81:15, 128:2328, 243:67, 729:504}
    assert len(rows) == 1901 and len({tuple(r[:2]) for r in rows}) == len(rows)
    assert all(1 <= r[1] <= orders[r[0]] and r[2] >= 3 for r in rows)
    weak = [r for r in rows if r[5]]
    assert len(weak) == 177 and all(r[3] == 2 for r in weak)
    assert sum(r[6] for r in rows) == 13209
    assert len(re.findall(r'ORDER_DONE\s+', log)) == 5
    assert re.search(r'PASS_21114_PILOT total=3181 eligible=1901 weak=177 checks=13209', log)
    covers = process('covers', 'PASS_21114_COVERS')
    cover_rows = [json.loads(m[1]) for m in re.finditer(
        r'COVER_ROW\s*(\[\s*\d+,\s*\d+,\s*\d+,\s*\[[^\]]*\],\s*\d+,\s*\d+\s*\])', covers)]
    assert [r[:2] for r in cover_rows] == [r[:2] for r in weak]
    hits = [r for r in cover_rows if r[4] >= 3]
    assert [r[:2] for r in hits] == [[128,854],[128,860]]
    expected = 'CoverInputs114 := '+str([r[:2] for r in weak])+';;\n'
    assert (ROOT/'results/21.114-cover-input.g').read_text() == expected
    process('central-export', 'PASS_21114_CENTRAL_EXPORT')
    process('independent', 'PASS_21114_INDEPENDENT')
    native = process('native', 'PASS_21114_NATIVE_CENTRAL')
    native_rows = [json.loads(m[1]) for m in re.finditer(r'NATIVE_ROW\s*(\[[^\]]*\])',native)]
    assert native_rows == [[854,8192,256,3,5],[860,8192,256,3,5]]
    proof = json.loads((ROOT/'results/21.114-independent-summary.json').read_text())
    assert proof['status'] == 'PASS' and proof['stats']['quotient_subgroups'] == 776
    assert len(proof['rejected_corruptions']) == 5
    assert all(c['source_maximum_subgroup_abelianization'] == 64 for c in proof['cases'])
    return {'catalogue_groups':3181, 'eligible_groups':len(rows), 'weak_groups':len(weak),
            'subgroup_abelianization_checks':13209, 'covers':len(cover_rows),
            'cover_hits':hits, 'independent_stats':proof['stats'],
            'by_order':[[n,count,sum(r[0]==n for r in rows),sum(r[0]==n for r in weak)]
                        for n,count in orders.items()]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--summary-only',action='store_true')
    args = parser.parse_args()
    summary = summarize()
    if args.summary_only:
        print(json.dumps(summary,indent=2))
        return
    packet = json.loads((ROOT/'results/21.114-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 0
    def bindings():
        assert len({row['path'] for row in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT/row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],path
    bindings()
    assert summary == packet['summary']
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='21.114-replay-') as directory:
            temporary = Path(directory)
            (temporary/'results').mkdir()
            p = subprocess.run([str(ROOT/'bin/gap'),'-o','3g',str(ROOT/'scripts/build_21_114_central.g')],
                               cwd=temporary,capture_output=True,timeout=120)
            assert p.returncode == 0 and not p.stderr
            assert p.stdout == (ROOT/'results/21.114-central-export.log').read_bytes()
            for ident in [854,860]:
                for suffix in ['-p.json','-q.json','-map.json']:
                    relative = f'results/21.114-central-{ident}'+suffix
                    assert (temporary/relative).read_bytes() == (ROOT/relative).read_bytes(),relative
        p = subprocess.run(['python3','scripts/verify_21_114_central.py'],cwd=ROOT,
                           capture_output=True,timeout=120)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/'results/21.114-independent.log').read_bytes()
        p = subprocess.run([str(ROOT/'bin/gap'),'-o','3g','scripts/native_21_114_central.g'],cwd=ROOT,
                           capture_output=True,timeout=120)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/'results/21.114-native.log').read_bytes()
    bindings()
    print(f'PASS_21114_PACKET files={len(packet["files"])} replay={str(args.replay).lower()} '
          'order=8192 derived_length=3 quotient_subgroups=776 new_complete_candidates=0')


if __name__ == '__main__':
    main()
