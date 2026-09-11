#!/usr/bin/env python3
"""Integrity and completion audit; not a formal verification of the proof."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def main():
    summary=json.loads((ROOT/'results/15.92-summary.json').read_text())
    for name,digest in summary['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    controls=json.loads((ROOT/'results/15.92-cycle-controls.json').read_text())
    assert controls['status']=='PASS' and len(controls['rows'])==150
    assert controls['table_count']==13 and controls['divisor_count']==240
    assert {(r['h'],r['d'],r['chain_length']) for r in controls['rows']}=={
        (h,d,k) for h in range(7,13) for d in (0,1,2,3,10) for k in (1,2,3,10,101)}
    for r in controls['rows']:
        assert r['moved_points']==r['p'] and r['p'] in (11,13)
        assert r['word_exponent']*r['p']==360360
    arithmetic=(ROOT/'results/15.92-cycle-controls.log').read_text()
    assert arithmetic.strip()=='15_92_CYCLE_CONTROLS_DONE 150 240'
    process=json.loads((ROOT/'results/15.92-cycle-process.json').read_text())
    assert process['returncode']==0
    gap=(ROOT/'results/15.92-r7-diagrams.log').read_text()
    assert '15_92_GAP_DIAGRAMS_DONE' in gap
    assert not any(s in gap for s in ('Error','Syntax warning','brk>','#I'))
    rows=re.findall(r'ALTERNATING_CONTROL (\d+) (\d+)',gap)
    assert rows==[(str(n),'11') for n in (78,120,162,246,456)]
    process=json.loads((ROOT/'results/15.92-r7-diagram-process.json').read_text())
    assert process['returncode']==0
    assert process['log_sha256']==hashlib.sha256((ROOT/'results/15.92-r7-diagrams.log').read_bytes()).hexdigest()
    assert process['input_sha256']==hashlib.sha256((ROOT/'results/15.92-r7-diagrams.g').read_bytes()).hexdigest()
    outer=json.loads((ROOT/'results/15.92-r7-outer-process.json').read_text())
    assert outer['actual_returncode']==0
    assert '15_92_DIAGRAM_RECONSTRUCTION_DONE' in (ROOT/'results/15.92-r7-diagram-runner.log').read_text()
    initial=json.loads((ROOT/'results/15.92-r7-outer-process-initial.json').read_text())
    assert initial['actual_returncode']==1
    assert 'Error, relations' in (ROOT/'results/15.92-r7-diagrams-initial.log').read_text()
    assert '15_92_GAP_DIAGRAMS_DONE' not in (ROOT/'results/15.92-r7-diagrams-initial.log').read_text()
    stopped=json.loads((ROOT/'results/15.92-r7-diagram-process-order-stopped.json').read_text())
    assert stopped['returncode']==-15
    stopped_outer=json.loads((ROOT/'results/15.92-r7-outer-process-order-stopped.json').read_text())
    assert stopped_outer['actual_returncode']==1
    stopped_log=(ROOT/'results/15.92-r7-diagrams-order-stopped.log').read_text()
    assert '15_92_GAP_DIAGRAMS_DONE' not in stopped_log
    assert re.findall(r'ALTERNATING_CONTROL (\d+) (\d+)',stopped_log)==[
        (str(n),'11') for n in (78,120,162,246)]
    primitive=json.loads((ROOT/'results/15.92-r7-degree456-primitive-process.json').read_text())
    assert primitive['actual_returncode']==0
    primitive_log=(ROOT/'results/15.92-r7-degree456-primitive.log').read_text()
    assert '15_92_PRIMITIVE_CONTROL_DONE 456 11' in primitive_log
    assert not any(s in primitive_log for s in ('Error','Syntax warning','brk>'))
    assert primitive['log_sha256']==hashlib.sha256((ROOT/'results/15.92-r7-degree456-primitive.log').read_bytes()).hexdigest()
    assert primitive['input_sha256']==hashlib.sha256((ROOT/'results/15.92-r7-degree456-primitive.g').read_bytes()).hexdigest()
    print('15_92_AUDIT_PASS',len(summary['sha256']),'hashes;',len(rows),'GAP groups;150 cycle cases')


if __name__=='__main__':
    main()
