#!/usr/bin/env python3
"""Audit disjoint ID coverage, completion provenance and independent controls."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def read_log(name):
    value = (ROOT/name).read_text()
    assert not re.search(r'Error|Syntax|Assertion', value), name
    return value


def prime_divisors(n):
    result = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            result.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        result.append(n)
    return result


state = json.loads((ROOT/'state/14.67-search.json').read_text())
assert state['status']=='EXITED_PENDING_AUDIT' and state['returncode']==0
assert [state['first_order'], state['last_order']]==[2, 511]
assert state['command']==[str(ROOT/'bin/gap'), str(ROOT/'scripts/search_14_67.g')]
assert state['output']==str(ROOT/'results/14.67-search.log')
for path, sha in state['source_sha256'].items():
    assert digest(path)==sha, f'Source changed since launch: {path}'

catalogue_log = read_log('results/14.67-catalogue.log')
catalogue_rows = [tuple(map(int, row)) for row in re.findall(
    r'^CATALOGUE order=(\d+) groups=(\d+)$', catalogue_log, re.M)]
assert [n for n,_ in catalogue_rows]==list(range(2, 512))
catalogue = dict(catalogue_rows)
assert catalogue_log.splitlines()[-1]==f'CATALOGUE_DONE orders=510 groups={sum(catalogue.values())}'

search = read_log('results/14.67-search.log')
header = json.loads(search.splitlines()[0])
assert header['command']==state['command']
assert header['source_sha256']==state['source_sha256']
assert 'PARAMETERS start=2 end=511 gap=4.16.1' in search
orders = [tuple(map(int, row)) for row in re.findall(
    r'^ORDER_START order=(\d+) groups=(\d+)$', search, re.M)]
assert orders==catalogue_rows
power_rows = [tuple(map(int, row)) for row in re.findall(
    r'^PRIME_POWER_SKIPPED order=(\d+) groups=(\d+) reason=nontrivial_centre$', search, re.M)]
assert power_rows==[(n,c) for n,c in catalogue_rows if len(prime_divisors(n))==1]
power_orders = {n for n,_ in power_rows}
skipped = [tuple(map(int, row)) for row in re.findall(
    r'^CENTRE_SKIPPED id=\[ (\d+), (\d+) \]$', search, re.M)]
checked = [tuple(map(int, row)) for row in re.findall(
    r'^CHECKED id=\[ (\d+), (\d+) \] minimum_class=(\d+) eligible_classes=(\d+) overgroups=(\d+)$',
    search, re.M)]
assert len(skipped)==search.count('CENTRE_SKIPPED id=')
assert len(checked)==search.count('CHECKED id=')
checked_ids = [(r[0],r[1]) for r in checked]
assert len(set(skipped+checked_ids))==len(skipped)+len(checked_ids)
assert set(skipped+checked_ids)=={(n,i) for n,c in catalogue_rows if n not in power_orders
                                 for i in range(1,c+1)}
assert all(size>1 and n%size==0 and classes>0 and overgroups>=2*classes
           for n,i,size,classes,overgroups in checked)
done_orders = [tuple(map(int, row)) for row in re.findall(
    r'^ORDER_DONE order=(\d+) enumerated=(\d+) centre_skipped=(\d+) runtime_ms=\d+$', search, re.M)]
assert done_orders==[(n,c,sum(x==n for x,i in skipped))
                     for n,c in catalogue_rows if n not in power_orders]
assert search.count('HIT_14_67')==0, 'A hit requires a separate witness audit'
names = ['catalogue','prime_power_skipped','enumerated','centre_skipped',
         'checked','eligible_classes','overgroups','hits']
pattern = '^DONE '+' '.join(key+r'=(\d+)' for key in names)+r' runtime_ms=\d+$'
matches = re.findall(pattern, search, re.M)
assert len(matches)==1 and search.splitlines()[-1].startswith('DONE ')
counts = dict(zip(names, map(int,matches[0])))
assert list(counts.values())==[
    sum(catalogue.values()), sum(c for n,c in power_rows), len(skipped)+len(checked),
    len(skipped), len(checked), sum(r[3] for r in checked), sum(r[4] for r in checked), 0]

control = read_log('results/14.67-controls.log')
control_names = ['groups','element_classes','literal_subgroup_cases','positive','negative','eligible_failures']
matches = re.findall('^PASS '+' '.join(key+r'=(\d+)' for key in control_names)+
                     r' runtime_ms=\d+$', control, re.M)
assert len(matches)==1 and control.splitlines()[-1].startswith('PASS ')
controls = dict(zip(control_names, map(int,matches[0])))
assert controls==dict(groups=147, element_classes=1966, literal_subgroup_cases=67289,
                     positive=1321, negative=645, eligible_failures=0)
assert controls['groups']==sum(catalogue[n] for n in range(2,33))+4
assert controls['positive']+controls['negative']==controls['element_classes']
assert [int(i) for i in re.findall(r'^CONTROL group_number=(\d+) ',control,re.M)]==list(range(1,148))

prime_rows = [r for r in checked if prime_divisors(r[2])==[r[2]]]
sources = ['scripts/lib_14_67.g','scripts/search_14_67.g','scripts/verify_14_67.g',
           'scripts/run_14_67.py','scripts/catalogue_14_67.g','scripts/summarize_14_67.py',
           'results/14.67-search.log','results/14.67-controls.log','results/14.67-catalogue.log',
           'results/14.67-runner.log','state/14.67-search.json','bin/gap',
           'research/14.67-search-plan.md','research/14.67-prime-class.md',
           'research/14.67-review.md',
           'references/cache/notebook-page79.png']
result = dict(status='COMPLETE_BOUNDED_SEARCH', observed_utc=datetime.now(timezone.utc).isoformat(),
              first_order=2,last_order=511,gap_version='4.16.1',search=counts,
              independent_controls=controls,
              prime_class_groups=len(prime_rows),
              prime_class_eligible_classes=sum(r[3] for r in prime_rows),
              composite_class_groups=len(checked)-len(prime_rows),
              sha256={p:digest(p) for p in sources},
              limitation='All groups through511 satisfy the assertion, with nontrivial-centre cases covered theoretically. General question and novelty unresolved. A separate all-group prime-class-size proof is retained as a partial theorem.')
(ROOT/'results/14.67-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='sha256'},indent=2))
