#!/usr/bin/env python3
"""Audit the extension packet and recompute exact controls without rerunning GAP."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,re,subprocess,sys
from check_15_65_classical import all_series,direct_product_series,finite_formula,analytic_controls
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check_hashes(record):
    for name,digest in record.items(): assert sha(ROOT/name)==digest,name
packet=json.loads((ROOT/'results/15.65-classical-summary.json').read_text())
assert packet['candidate_number']==31 and packet['outer_python_exit']==0
assert packet['novelty']=='pending' and packet['outside_reviews']==0
check_hashes(packet['sha256'])
subprocess.run([sys.executable,str(ROOT/'scripts/audit_15_65.py')],check=True,cwd=ROOT)
r=json.loads((ROOT/'results/15.65-classical-controls.json').read_text())
assert r['status']=='PASS' and r['actual_gap_exit']==0
check_hashes(r['hashes'])
p=json.loads((ROOT/'results/15.65-classical-gap-process.json').read_text())
assert p['actual_exit']==0
check_hashes(p['hashes'])
log=(ROOT/'results/15.65-classical-gap.log').read_text()
assert log.rstrip().endswith('CLASSICAL_CONTROLS_DONE')
assert not re.search(r'Error|Syntax warning|Syntax error|Traceback|#I',log)
pattern=r'^CLASSICAL_CONTROL (U|Sp) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)$'
rows=re.findall(pattern,log,re.M)
assert len(rows)==23 and len(r['finite_cases'])==23
expected={('U',2,n) for n in range(1,5)}|{('U',q,n) for q in (3,4) for n in range(1,4)}|{('U',q,n) for q in (5,7) for n in (1,2)}
expected|={('Sp',2,n) for n in range(1,4)}|{('Sp',q,n) for q in (3,4) for n in (1,2)}|{('Sp',q,1) for q in (5,7)}
assert {(row[0],int(row[1]),int(row[2])) for row in rows}==expected
for row,case in zip(rows,r['finite_cases']):
    family=row[0]; q,n,order,c,ss,rs,classes=map(int,row[1:])
    assert (family,q,n,order,classes)==tuple(case[k] for k in ('family','q','n','order','classes'))
    for mode,count in [('C',c),('SS',ss),('RS',rs)]:
        assert count==case['values'][mode]['count']
        assert Q(count,order)==Q(case['values'][mode]['proportion'])==finite_formula(family,q,n,mode)
assert r['class_checks']==sum(int(row[-1]) for row in rows)==563
assert r['finite_formula_checks']==69
assert r['series_degree']==40
series=all_series(40)
assert {k:list(map(str,v)) for k,v in series.items()}==r['series']
for mode in ('C','SS','RS'):
    for family,e in [('U',0),('Sp',1),('Sp',2)]:
        key=f'U_{mode}' if family=='U' else f'Sp{e}_{mode}'
        assert series[key][:13]==direct_product_series(family,mode,e,12)
assert r['published_coefficients_checked']==160 and r['published_coefficients_matched']==159
assert r['independent_binomial_checks']==117
assert r['published_discrepancies']==[dict(row='Sp2_SS',degree=9,computed='-193',published='-195')]
assert r['orthogonal_table_identity_coefficient']=='-193'
assert analytic_controls()==r['analytic_controls']
assert (ROOT/'results/15.65-classical-controls-runner.log').read_text().strip()=='15_65_CLASSICAL_CONTROLS_DONE 23 563 160'
# Initial GAP files were relocated verbatim after the process exited.
initial=json.loads((ROOT/'results/15.65-classical-gap-process-initial.json').read_text())
assert initial['actual_exit']==0
for name,digest in initial['hashes'].items():
    path=ROOT/name; relocated=path.with_name(path.stem+'-initial'+path.suffix)
    assert sha(relocated)==digest,name
initial_log=(ROOT/'results/15.65-classical-gap-initial.log').read_text()
assert initial_log.rstrip().endswith('CLASSICAL_CONTROLS_DONE')
assert not re.search(r'Error|Syntax warning|Syntax error|Traceback',initial_log)
assert re.findall(pattern,initial_log,re.M)==rows
failed=json.loads((ROOT/'results/15.65-classical-table-mismatch-process.json').read_text())
assert failed['actual_exit']==1
check_hashes(failed['hashes'])
assert 'AssertionError' in (ROOT/'results/15.65-classical-controls-table-mismatch.log').read_text()
print('PASS_15_65_CLASSICAL_PACKET',len(packet['sha256']),'hashes; 23 groups; 563 classes; one documented table discrepancy')
