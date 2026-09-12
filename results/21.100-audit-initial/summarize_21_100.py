#!/usr/bin/env python3
"""Audit saved screen rows against completed, hash-bound process records."""
from collections import Counter
import hashlib
import json
from math import gcd
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process(base, sentinel):
    record = json.loads(Path(str(base)+'-process.json').read_text())
    out,err = Path(str(base)+'.log'),Path(str(base)+'.stderr')
    assert record['actual_returncode'] == 0 and record['sentinel_seen']
    assert sha(out) == record['stdout_sha256'] and sha(err) == record['stderr_sha256']
    assert not err.read_bytes() and 'Error' not in out.read_text()
    assert out.read_text().count(sentinel) == 1
    return out.read_text(),record


def prime_power(n,p):
    assert p >= 2 and all(p % k for k in range(2,p))
    while n > 1 and n % p == 0:
        n //= p
    return n == 1


def summarize():
    jobs = [('pilot',None,None)] + [(f'order{o}-shard{s}',o,s) for o in [256,2187] for s in range(4)]
    counts = Counter()
    by_order = {}
    actions_seen = set()
    state = json.loads((ROOT/'results/21.100-shards-state.json').read_text())
    assert len(state['jobs']) == 8
    for name,order,shard in jobs:
        base = ROOT/('results/21.100-'+name)
        sentinel = 'PASS_21100_PILOT ' if order is None else 'PASS_21100_SHARD '
        log,record = process(base,sentinel)
        if order is not None:
            assert record['order'] == order and record['shard'] == shard and record['shards'] == 4
            assert record in state['jobs']
        done = [json.loads(x) for x in re.findall(r'^ORDER_DONE (\[.*\])$',log,re.M)]
        assert [x[0] for x in done] == ([81,243,729] if order is None else [order])
        local = Counter()
        local_order = Counter()
        for line in Path(str(base)+'-rows.jsonl').read_text().splitlines():
            row = json.loads(line)
            if order is None:
                assert len(row) == 10
                row = row[:2]+[2,2]+row[2:]
            assert len(row) == 12
            o,i,p,a,j,aut,syl,c,n,never,cab,chars = row
            assert o in [x[0] for x in done]
            if order is not None:
                assert (i-1) % 4 == shard
            assert 1 <= i <= {81:15,243:67,729:504,256:56092,2187:9310}[o]
            assert 1 < a <= syl <= aut and aut % syl == 0 and syl % a == 0
            assert prime_power(syl,p) and prime_power(a,p) and (aut//syl) % p != 0 and gcd(o,a) == 1
            assert 1 <= cab <= c <= o and o % c == 0 and c % cab == 0
            key = (o,i,p,a,j)
            assert key not in actions_seen
            actions_seen.add(key)
            assert len(chars) == n and len({x[0] for x in chars}) == n
            assert all(len(x) == 5 and all(type(v) is int for v in x) for x in chars)
            assert all(x[0] > 0 and x[1] > 0 and x[2] > 0 and x[3] in [0,1]
                       and x[4] == int(x[2] == 1) and x[3] == x[4] for x in chars)
            assert sum(x[3] for x in chars) == never == cab
            stats = dict(actions=1,invariant_characters=n,
                         nonlinear_correspondents=sum(x[2] > 1 for x in chars),
                         nonabelian_fixed_subgroups=int(c != cab),count_hits=0,pointwise_hits=0)
            local.update(stats); local_order[o] += 1
            if o not in by_order:
                by_order[o] = dict(counts=Counter(),action_orders=Counter(),fixed_shapes=Counter())
            by_order[o]['counts'].update(stats)
            by_order[o]['action_orders'][a] += 1
            by_order[o]['fixed_shapes'][(c,cab)] += 1
        for o,bound,groups,actions,hits,pointwise in done:
            assert bound == {81:15,243:67,729:504,256:56092,2187:9310}[o]
            assert actions == local_order[o] and hits == pointwise == 0
            local['class_at_least_three_groups'] += groups
            by_order[o]['counts']['class_at_least_three_groups'] += groups
        summary = [local['class_at_least_three_groups'],local['actions'],0,0]
        assert json.loads(re.findall(r'^'+sentinel+r'(\[.*\])$',log,re.M)[0]) == summary
        counts.update(local)
    expected = dict(class_at_least_three_groups=32262,actions=15623,invariant_characters=313685,
                    nonlinear_correspondents=66172,nonabelian_fixed_subgroups=5856,count_hits=0,pointwise_hits=0)
    assert dict(counts) == expected
    return dict(status='PASS_SAVED_SCREEN_ROWS',counts=dict(sorted(counts.items())),
                orders=[dict(order=o,counts=dict(sorted(r['counts'].items())),
                             action_orders=sorted(r['action_orders'].items()),
                             fixed_shapes=[[a,b,n] for (a,b),n in sorted(r['fixed_shapes'].items())])
                        for o,r in sorted(by_order.items())],
                scope='GAP-based bounded screen; independent certificates cover selected actions only.',
                new_complete_candidates_added=0)


def main():
    result = summarize()
    (ROOT/'results/21.100-screen-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_21100_SAVED_SCREEN',json.dumps(result['counts'],sort_keys=True))


if __name__ == '__main__':
    main()
