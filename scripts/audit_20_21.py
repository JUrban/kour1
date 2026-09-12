#!/usr/bin/env python3
"""Verify frozen coverage and replay independent multiplication-table controls."""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re


def run():
    packet = json.loads(Path('results/20.21-summary.json').read_text())
    for name, digest in packet['sha256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    counts = [(12,5,1,0),(24,15,2,0),(48,52,8,1),
              (96,231,31,4),(192,1543,152,20),(384,20169,1047,98)]
    log = Path('results/20.21-search.log').read_text().strip()
    expected = ['ORDER_2021 %d tested=%d eligible=%d both=%d' % row for row in counts]
    assert log.splitlines() == expected + ['PASS_2021_SEARCH tested=22015']
    rows = [ast.literal_eval(line) for line in Path('results/20.21-kernels.grows').read_text().splitlines()]
    assert len(rows) == 123
    assert len({tuple(row[:2]) for row in rows}) == 123
    assert Counter(row[0] for row in rows) == {n:b for n,t,e,b in counts if b}
    for n, i, cs, aa in rows:
        bound = next(t for nn,t,e,b in counts if nn == n)
        assert 1 <= i <= bound and cs and aa
        assert all(k[0] == n//12 for k in cs + aa)
        assert set(map(tuple, cs)).isdisjoint(map(tuple, aa))
    processes = json.loads(Path('results/20.21-process-observations.json').read_text())
    assert len(processes['observations']) == 3
    for record in processes['observations']:
        assert record['observed_exit_code'] == 0
        assert record['exit_tool_chunk']
        output = Path(record['log']).read_text()
        assert record['sentinel'] in output
        assert not re.search(r'Error|Syntax warning|Traceback|Break loop', output)
    assert Path('results/20.21-table-export.log').read_text().strip() == 'PASS_2021_TABLE_EXPORT cases=25'
    spec = importlib.util.spec_from_file_location('control2021', 'scripts/check_20_21.py')
    control = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(control)
    observed = control.run()
    assert observed == json.loads(Path('results/20.21-controls.json').read_text())
    print('PASS_2021_PACKET', len(packet['sha256']), 'groups=22015 controls=25')


if __name__ == '__main__':
    run()
