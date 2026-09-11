#!/usr/bin/env python3
"""Audit complete search coverage and replay every noncentral involution."""
from pathlib import Path
import ast
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'results/16.14-through256.log').read_text()
assert 'Error' not in text and 'HIT_16_14' not in text
expected = {2: 1, 4: 2, 8: 5, 16: 14, 32: 51, 64: 267,
            128: 2328, 256: 56092}
starts = [(int(a), int(b)) for a, b in re.findall(
    r'ORDER_START order=(\d+) groups=(\d+)', text)]
assert starts == list(expected.items())
done = [[int(x) for x in row] for row in re.findall(
    r'ORDER_DONE order=(\d+) rank_excluded=(\d+) involution_excluded=(\d+) hits=(\d+)', text)]
assert [row[0] for row in done] == list(expected)
rows = []
for order, ident, d, z, vector in re.findall(
        r'INVOLUTION_EXCLUSION id=\[ (\d+), (\d+) \] d=(\d+) zrank=(\d+) witness=(\[[^\n]+\])', text):
    n, i, rank, central_rank = map(int, (order, ident, d, z))
    vector = ast.literal_eval(vector)
    assert n in expected and 1 <= i <= expected[n]
    assert rank > 2*central_rank and all(x in (0, 1) for x in vector)
    rows.append([n, i, rank, central_rank, vector])
assert len({(r[0], r[1]) for r in rows}) == len(rows)
for n, rank, involution, hits in done:
    assert rank+involution+hits == expected[n] and hits == 0
    assert sum(row[0] == n for row in rows) == involution
summary = re.findall(r'DONE checked=(\d+) rank_excluded=(\d+) involution_excluded=(\d+) hits=(\d+) elapsed_ms=(\d+) PASS', text)
assert len(summary) == 1
checked, rank, involution, hits, elapsed = map(int, summary[0])
assert (checked, rank, involution, hits) == (58760, 55177, 3583, 0)
assert rank == sum(row[1] for row in done) and involution == len(rows)

# Numeric JSON arrays are valid GAP lists. Reconstruct every element as an
# ordered product of pc generators, then check noncentrality by commutation
# with generators, without using centre membership for that predicate.
program = 'WITNESS_ROWS:=' + json.dumps(rows) + ';;\n' + r'''
SizeScreen([1000000,1000000]);;
(function()
local row,g,pc,x,zcount,checked;
checked:=0;
for row in WITNESS_ROWS do
  g:=SmallGroup(row[1],row[2]); pc:=Pcgs(g);
  if Length(pc)<>Length(row[5]) then Error("pc length"); fi;
  x:=Product([1..Length(pc)],j->pc[j]^row[5][j]);
  if x=One(g) or x^2<>One(g) then Error("not an involution"); fi;
  if ForAll(GeneratorsOfGroup(g),y->x*y=y*x) then Error("witness central"); fi;
  if Length(AbelianInvariants(g))<>row[3] then Error("generator rank"); fi;
  zcount:=Number(Elements(Centre(g)),y->y^2=One(g));
  if zcount<>2^row[4] then Error("central rank"); fi;
  checked:=checked+1;
od;
Print("DONE checked=",checked," WITNESSES PASS\n");
end)();
QUIT;
'''
proc = subprocess.run([str(ROOT / 'bin/gap')], input=program, text=True,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT)
(ROOT / 'results/16.14-witness-verification.log').write_text(proc.stdout)
assert proc.returncode == 0 and 'Error' not in proc.stdout
assert proc.stdout.strip().endswith('DONE checked=3583 WITNESSES PASS')
small = (ROOT / 'results/16.14-small-verification.log').read_text()
assert 'Error' not in small and 'ALL CHECKS PASS' in small
assert 'checked=340' in small
result = dict(problem='16.14', status='PASS', complete_orders=list(expected),
              groups_checked=checked, rank_bound_satisfied=rank,
              noncentral_involution_certificates=involution, hits=hits,
              independent_small_groups=340,
              scope='Bounded search through order 256 only; no general resolution.')
(ROOT / 'results/16.14-summary.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
