#!/usr/bin/env python3
"""Find and independently verify isomorphisms for the two power-map exceptions."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = 'results/6.47-vector-64-34-isomorphism'


def verify(data, controls, result):
    old, n = data['table'], data['n']
    assert result['original_id'] == [64, 34]
    operations = {r['function_index']: r['table'] for r in controls['associative_operations']}
    count = 0
    for record in result['operations']:
        assert record['function_index'] in [1, 2]
        perm = record['permutation']
        assert record['isomorphic'] and record['group_id'] == [64, 34]
        assert sorted(perm) == list(range(1, n+1))
        op = operations[record['function_index']]
        for a in range(n):
            for b in range(n):
                assert perm[op[a][b]-1] == old[perm[a]-1][perm[b]-1]
                count += 1
    assert [r['function_index'] for r in result['operations']] == [1, 2]
    return {'status': 'PASS_647_EXCEPTIONAL_ISOMORPHISMS', 'pairs_checked': count}


def main():
    data = json.loads((ROOT/'results/6.47-vector-64-34.json').read_text())
    controls = json.loads((ROOT/'results/6.47-vector-64-34-controls.json').read_text())
    tables = [r for r in controls['associative_operations'] if r['function_index'] in [1, 2]]
    lines = [f'old := {json.dumps(data["table"])};;',
             'gp := List([1..64],a->PermList(List([1..64],b->old[b][a])));;',
             'g := Group(gp);;',
             f'PrintTo("{STEM}.json","{{\\"original_id\\":",IdGroup(g),",\\"operations\\":[");']
    for index, record in enumerate(tables):
        if index:
            lines.append(f'AppendTo("{STEM}.json",",");')
        lines.extend([
            f'op := {json.dumps(record["table"])};;',
            'hp := List([1..64],a->PermList(List([1..64],b->op[b][a])));;',
            'h := Group(hp);; iso := IsomorphismGroups(h,g);;',
            'if iso=fail then p:=[]; else p:=List(hp,a->Position(gp,Image(iso,a))); fi;',
            f'AppendTo("{STEM}.json","{{\\"function_index\\":{record["function_index"]},\\"group_id\\":",IdGroup(h),",\\"isomorphic\\":",iso<>fail,",\\"permutation\\":",p,"}}");'])
    lines.extend([f'AppendTo("{STEM}.json","]}}\\n");',
                  'Print("PASS_647_EXCEPTIONAL_GAP\\n");', 'QUIT_GAP(0);'])
    source, logpath = ROOT/(STEM+'.g'), ROOT/(STEM+'.log')
    source.write_text('\n'.join(lines)+'\n')
    start = time.monotonic()
    with logpath.open('w') as stream:
        proc = subprocess.run(['bin/gap', STEM+'.g'], cwd=ROOT, stdout=stream,
                              stderr=subprocess.STDOUT, timeout=180)
    log = logpath.read_text()
    process = {'actual_gap_returncode': proc.returncode,
               'elapsed_seconds': time.monotonic()-start,
               'observed_utc': datetime.now(timezone.utc).isoformat(),
               'clean_log': not any(s in log for s in ['Error,', 'Syntax error', 'Syntax warning']),
               'sentinel': log.rstrip().endswith('PASS_647_EXCEPTIONAL_GAP'),
               'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in [source, logpath, ROOT/'scripts/check_6_47_exceptional_iso.py']}}
    (ROOT/(STEM+'-process.json')).write_text(json.dumps(process, indent=2)+'\n')
    assert proc.returncode == 0 and process['clean_log'] and process['sentinel']
    result = json.loads((ROOT/(STEM+'.json')).read_text())
    checked = verify(data, controls, result)
    (ROOT/(STEM+'-check.json')).write_text(json.dumps(checked, indent=2)+'\n')
    print(json.dumps(checked))


if __name__ == '__main__':
    main()
