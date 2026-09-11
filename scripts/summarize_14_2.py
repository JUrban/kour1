#!/usr/bin/env python3
"""Audit exact coverage and arithmetic totals in the completed 14.2 screens."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text().replace('\r', '')

def fields(line):
    return {k: int(v) for k, v in re.findall(r'(\w+)=(\d+)(?=\s|$)', line)}

manifest = [line for line in read('results/14.2-table-manifest.log').splitlines() if line]
names = [line.removeprefix('NAME ') for line in manifest if line.startswith('NAME ')]
assert len(names) == len(set(names)) == 2750
assert manifest[:2] == ['GAP 4.16.1', 'CTBLLIB 1.3.11']

def audit_screen(path, prefix, ending, keys):
    log = read(path)
    assert 'Error' not in log and 'Syntax warning' not in log
    rows = [line for line in log.splitlines() if line.startswith(prefix + ' ')]
    assert len(rows) == len(names)
    totals = dict.fromkeys(keys, 0)
    for i, (row, name) in enumerate(zip(rows, names), 1):
        parsed = fields(row)
        assert parsed['index'] == i
        assert re.search(r' name=(.*?) (?:order|classes)=', row)[1] == name
        for key in keys:
            totals[key] += parsed[key]
        if prefix == 'TABLE':
            r = parsed['rational_rows']
            assert parsed['pairs'] == r * (r - 1) // 2
            assert 0 <= parsed['nonmonomial'] <= parsed['integral_swaps'] <= parsed['conductor_matched'] <= parsed['pairs']
        else:
            assert 0 <= parsed['nonmonomial'] <= parsed['integral'] <= parsed['tested']
            assert (' eligible=true ' in row) == (parsed['classes'] <= 100)
    final = [line for line in log.splitlines() if line.startswith(ending + ' ')]
    assert len(final) == 1 and log.rstrip().endswith(final[0])
    assert fields(final[0]) == dict(tables=len(names), **totals)
    return dict(tables=len(names), **totals)

paths = ['scripts/search_14_2.g', 'scripts/verify_14_2.g',
         'results/14.2-rational-swaps.log', 'results/14.2-controls.log',
         'results/14.2-table-manifest.log',
         'references/cache/hertweck-centres-2006.pdf']
swaps = audit_screen(paths[2], 'TABLE', 'DONE',
                     ['rational_rows', 'pairs', 'conductor_matched', 'integral_swaps', 'nonmonomial'])
control = read(paths[3])
assert 'Error' not in control and 'Syntax warning' not in control
controls = [fields(x) for x in control.splitlines() if x.startswith('CONTROL ')]
assert len(controls) == 10
assert sum(x['pairs'] for x in controls) == 76
assert sum(x['integral_swaps'] for x in controls) == 19
assert control.rstrip().endswith('PASS groups=10 element_products=33572 pairs=76 '
    'integral_swaps=19 nonintegral_swaps=57 multiplicativity_checks=503')
result = dict(status='COMPLETE_RESTRICTED_SWAP_SCREEN', gap_version='4.16.1',
              ctbllib_version='1.3.11', swaps=swaps,
              independent_controls=fields(control.splitlines()[-1]))

block_path = 'results/14.2-blocks.log'
if (ROOT / block_path).exists() and '\nDONE_BLOCKS ' in read(block_path):
    result['blocks'] = audit_screen(block_path, 'BLOCK_TABLE', 'DONE_BLOCKS',
                                   ['blocks', 'tested', 'integral', 'nonmonomial'])
    bc_path = 'results/14.2-block-controls.log'
    bc = read(bc_path)
    assert 'Error' not in bc and 'Syntax warning' not in bc
    assert bc.rstrip().endswith('PASS_BLOCK_CONTROLS groups=3 tested=174 '
        'integral=9 nonintegral=165 degree_changed=0')
    result['independent_block_controls'] = fields(bc.splitlines()[-1])
    paths.extend([block_path, bc_path, 'scripts/search_14_2_blocks.g', 'scripts/verify_14_2_blocks.g'])
    result['status'] = 'COMPLETE_RESTRICTED_SWAP_AND_BLOCK_SCREENS'
result['sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
result['limitation'] = ('Only rational idempotent transpositions and, if reported, '
    'degree-changing permutations within one mixed-degree conductor block of size '
    'at most six in tables with at most 100 classes. Coordinated changes in different '
    'blocks and nonrational components are not covered. Table names can represent '
    'isomorphic groups. No general solution or novelty claim.')
(ROOT / 'results/14.2-summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
