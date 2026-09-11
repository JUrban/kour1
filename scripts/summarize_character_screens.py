#!/usr/bin/env python3
"""Audit the completion and count consistency of the two character screens."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_log(name):
    text = (ROOT / 'results' / name).read_text()
    assert not re.search(r'(^|\n)(?:Error|Syntax warning|Syntax error|HIT)\b', text, re.I), name
    return text


def fields(text, marker):
    # GAP wraps long lines at arbitrary positions. These summaries consist
    # solely of whitespace-separated name=integer fields through end of log.
    start = text.rfind(marker + ' ')
    assert start >= 0, (marker, text[-200:])
    return {k: int(v) for k, v in re.findall(r'(\w+)=\s*(\d+)', text[start:])}


def main():
    raw17 = read_log('17.100-tables.log')
    total17 = fields(raw17, 'DONE')
    rows17 = re.findall(
        r'TABLE name=(\S+) order=\s*(\d+) odd_rows=\s*(\d+) '
        r'odd_columns=\s*(\d+) non2_columns=\s*(\d+)', re.sub(r'\s+', ' ', raw17))
    assert len(rows17) == total17['simple_tables'] == 215
    assert len({r[0] for r in rows17}) == len(rows17)
    assert sum(int(r[2])*int(r[3]) for r in rows17) == total17['pairs'] == 12606
    assert sum(int(r[2])*int(r[4]) for r in rows17) == total17['non2_pairs'] == 332
    assert sum(int(r[4]) > 0 for r in rows17) == total17['non2_tables'] == 4
    assert total17['tables'] == 2750 and total17['hits'] == 0
    ctrl17 = fields(read_log('17.100-controls.log'), 'PASS')
    assert ctrl17 == dict(simplicity_checks=2750, actual_groups=8, pairs=72)
    out17 = dict(status='PASS', search=total17, controls=ctrl17,
                 coverage_unit='library character-table entries; aliases may be isomorphic',
                 non2_entries=[r[0] for r in rows17 if int(r[4])])

    raw18 = read_log('18.20-tables.log')
    total18 = fields(raw18, 'DONE')
    rows18 = re.findall(r'TABLE name=(\S+) rows=\s*(\d+) total_pairs=\s*(\d+)',
                        re.sub(r'\s+', ' ', raw18))
    assert len(rows18) == total18['tables'] == 2750
    assert len({r[0] for r in rows18}) == len(rows18)
    assert all(int(a[2]) <= int(b[2]) for a, b in zip(rows18, rows18[1:]))
    assert int(rows18[-1][2]) == total18['unequal_degree_pairs'] == 33810661
    assert sum(int(r[1])*(int(r[1])-1)//2 for r in rows18) == (
        total18['unequal_degree_pairs'] + total18['equal_degree_pairs'])
    assert total18['equal_degree_pairs'] == 1647090 and total18['hits'] == 0
    ctrl18 = fields(read_log('18.20-controls.log'), 'PASS')
    assert ctrl18 == dict(group_cases=10, row_pairs=129, positive=16, negative=113)
    out18 = dict(status='PASS', search=total18, controls=ctrl18,
                 coverage_unit='library character-table entries; aliases may be isomorphic')
    for problem, out in [('17.100', out17), ('18.20', out18)]:
        (ROOT / 'results' / f'{problem}-summary.json').write_text(json.dumps(out, indent=2)+'\n')
        print(problem, json.dumps(out))


if __name__ == '__main__':
    main()
