#!/usr/bin/env python3
"""Source bindings, rejected GAP control, and independent polynomial replay."""
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def polynomial(node, t):
    """Return (value, degree bound) with a deliberately restricted AST."""
    if isinstance(node, ast.Constant):
        assert type(node.value) is int
        return Fraction(node.value), 0
    if isinstance(node, ast.Name):
        assert node.id == 't'
        return Fraction(t), 1
    if isinstance(node, ast.UnaryOp):
        assert isinstance(node.op, ast.USub)
        v,d = polynomial(node.operand,t)
        return -v,d
    assert isinstance(node, ast.BinOp)
    a,d = polynomial(node.left,t)
    b,e = polynomial(node.right,t)
    if isinstance(node.op, ast.Add):
        return a+b,max(d,e)
    if isinstance(node.op, ast.Sub):
        return a-b,max(d,e)
    if isinstance(node.op, ast.Mult):
        return a*b,d+e
    assert isinstance(node.op, ast.Pow) and e == 0 and b.denominator == 1
    assert 0 <= b <= 5
    return a**int(b),d*int(b)


def main():
    packet = json.loads((ROOT/'results/17.115-21.98-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 0
    def bindings():
        for row in packet['files']:
            p = ROOT/row['path']
            assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256'],p
    bindings()
    for row in json.loads((ROOT/'results/17.115-21.98-source-downloads.json').read_text()):
        p = ROOT/row['path']
        assert row['status'] == 200 and row['bytes'] == p.stat().st_size
        assert row['sha256'] == sha(p)
    for name in ['gap','python']:
        base = ROOT/('results/21.98-path-'+name)
        record = json.loads(Path(str(base)+'-process.json').read_text())
        out,err = Path(str(base)+'.log'),Path(str(base)+'.stderr')
        assert record['actual_returncode'] == 0 and record['sentinel_seen']
        assert record['stdout_sha256'] == sha(out) and record['stderr_sha256'] == sha(err)
        assert not err.read_bytes() and 'Error' not in out.read_text()
    failed = ROOT/'results/21.98-path-initial'
    record = json.loads((failed/'21.98-path-gap-process.json').read_text())
    assert record['actual_returncode'] == 0 and not record['sentinel_seen']
    assert record['stdout_sha256'] == sha(failed/'21.98-path-gap.log')
    assert record['stderr_sha256'] == sha(failed/'21.98-path-gap.stderr')
    assert 'no 1st choice method found for `Int' in (failed/'21.98-path-gap.stderr').read_text()
    assert json.loads((failed/'wrapper-observation.json').read_text())['actual_wrapper_returncode'] == 1
    control = json.loads((ROOT/'results/21.98-path-controls.json').read_text())
    assert [control[k] for k in ['random_paths','integer_evaluations','maximum_log_degree',
                                 'distinct_explicit_directions']] == [48,384,5,100]
    rows = re.findall(r'PATH row=(\d+) col=(\d+) polynomial=([^\n]+)',
                      (ROOT/'results/21.98-path-gap.log').read_text())
    assert len(rows) == 15
    seen = set()
    for i,j,expression in rows:
        ij = int(i),int(j)
        assert ij not in seen and 1 <= ij[0] < ij[1] <= 6
        seen.add(ij)
        node = ast.parse(expression.replace('^','**'),mode='eval').body
        coefficients = list(map(Fraction,control['explicit_delta2_log'].get(str(ij),['0'])))
        for t in range(6):
            value,degree = polynomial(node,t)
            assert degree <= 5
            assert value == sum(a*t**k for k,a in enumerate(coefficients))
    for name,command in [('python',['python3','scripts/check_21_98_path.py']),
                         ('gap',['bin/gap','-o','512m','scripts/check_21_98_path.g'])]:
        p = subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT/('results/21.98-path-'+name+'.log')).read_bytes()
    bindings()
    print('PASS_17115_2198_PACKET files=%d paths=48 integer_evaluations=384 '
          'matrix_polynomials=15 distinct_directions=100 rejected_run_preserved=true '
          'new_complete_candidates=0' % len(packet['files']))


if __name__ == '__main__':
    main()
