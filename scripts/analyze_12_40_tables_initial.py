#!/usr/bin/env python3
"""Independently recompute all p-parts and check exact table-row coverage."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def primes(n):
    factors = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        factors.append(n)
    return factors


def part(n,p):
    answer = 1
    while n % p == 0:
        n //= p
        answer *= p
    return answer


def run():
    catalog = json.loads((ROOT/'results/12.40-table-catalog.json').read_text())
    assert len(catalog['names']) == len(set(catalog['names'])) == catalog['table_count']
    by_name, excess = {}, []
    available = missing = degrees_checked = 0
    for line in (ROOT/'results/12.40-table-degrees.txt').read_text().splitlines():
        name,order,p,values = line.split('|')
        order,p = int(order),int(p)
        entry = by_name.setdefault(name,{'order':order,'primes':[]})
        assert entry['order'] == order and p not in entry['primes']
        entry['primes'].append(p)
        assert p in primes(order)
        if values == 'MISSING':
            missing += 1
            continue
        available += 1
        degrees = ast.literal_eval(values)
        assert isinstance(degrees,list) and degrees
        assert all(type(d) is int and d > 0 for d in degrees)
        degrees_checked += len(degrees)
        order_part = part(order,p)
        large = [{'index':i+1,'degree':d,'degree_part':part(d,p)}
                 for i,d in enumerate(degrees) if part(d,p)>order_part]
        if large:
            excess.append({'name':name,'prime':p,'order':order,
                           'order_part':order_part,'degrees':large})
    # The catalogue may contain a trivial group with no tested primes.
    assert set(by_name) <= set(catalog['names'])
    unrepresented = set(catalog['names'])-set(by_name)
    assert not unrepresented, ('catalogue entries without any row',unrepresented)
    for name,entry in by_name.items():
        assert sorted(entry['primes']) == primes(entry['order']),name
    assert available == catalog['available'] and missing == catalog['missing']
    expected = ['EXCESS '+e['name']+' p='+str(e['prime'])+
                ' order_p='+str(e['order_part'])+
                ' max_degree_p='+str(max(d['degree_part'] for d in e['degrees']))
                for e in excess]
    actual = [s for s in (ROOT/'results/12.40-table-screen.log').read_text().splitlines()
              if s.startswith('EXCESS ')]
    assert actual == expected
    return {'status':'PASS','table_names':catalog['table_count'],
            'available_tables':available,'missing_tables':missing,
            'degrees_checked':degrees_checked,'excess':excess,
            'scope':'Installed table names can describe isomorphic groups; '
                    'unavailable tables and groups outside the library are not covered.'}


if __name__ == '__main__':
    data = run()
    (ROOT/'results/12.40-table-analysis.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS_1240_TABLE_ANALYSIS',data['table_names'],data['available_tables'],
          data['missing_tables'],data['degrees_checked'],len(data['excess']))
