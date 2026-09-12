#!/usr/bin/env python3
"""Discard redundant gcd edges and print short, directly readable proofs."""
import json
from pathlib import Path
from verify_19_62_monomial_certificates import verify_case

SELECTED = {'a2': [2], 'b2': [2, 3], 'g2': [3, 5]}


def coordinate(label, value):
    x, y = value
    if label == 'a2':
        assert (2*x+y) % 3 == (x+2*y) % 3 == 0
        return (2*x+y)//3, (x+2*y)//3
    if label == 'b2':
        assert y % 2 == 0
        return x+y, x+y//2
    return 2*x+3*y, x+2*y


def run():
    text = ['# Nineteen short rank-two derivations for 19.62', '',
            'Generated from the checked certificates. Coordinates (m,n) mean',
            'm*a+n*b, with a,b simple and a short in B2 and G2. Each initial',
            'variable belongs to the displayed original subgroup A. Every',
            'subsequent line belongs to B at its displayed root, hence also to A.',
            'An expression c*z_i^u*z_j^v uses the corresponding Chevalley carpet',
            'rule. When two expressions are listed, their monomial coefficients',
            'have the displayed gcd; subtraction and integer multiplication',
            'give the stated membership without division in the ring.', '',
            'These are all targets at one root of each length. Weyl transport',
            'covers the other roots. The checker also checks all 104 targets',
            'directly and verifies invariance and coverage under simple reflections.', '']
    reports = []
    for label in SELECTED:
        prefix = 'results/19.62-'+label+'-rank-two-'
        data = json.loads(Path(prefix+'input.json').read_text())
        nr = len(data['roots'])
        rows = []
        total = largest = displayed = 0
        for index, original in map(json.loads, Path(prefix+'certificate.jsonl').read_text().splitlines()):
            verify_case(data, index, original)
            known = {v[0]: v for v in original}
            def coefficient(key):
                return 2**known[key][1]*3**known[key][2]
            def edge_coefficient(edge):
                rule, left, right = edge
                r, s, k, i, j, c = data['rules'][rule]
                return c*coefficient(left)**i*coefficient(right)**j
            changed = {}
            for node in original:
                key, a, b, var, left, right = node
                if var < 0:
                    exact = [e for e in [left, right] if edge_coefficient(e) == coefficient(key)]
                    if exact:
                        left = right = exact[0]
                changed[key] = [key, a, b, var, left, right]
            keep = set()
            case = data['cases'][index-1]
            count = 1
            for r, e in case['variables']:
                count *= e+1
            pending = [(count-1)*nr+case['root']]
            for key in pending:
                if key in keep:
                    continue
                keep.add(key)
                node = changed[key]
                if node[3] < 0:
                    for rule, left, right in node[4:]:
                        pending.extend([left, right])
            nodes = [changed[k] for k in sorted(keep)]
            size = verify_case(data, index, nodes)
            rows.append([index, nodes]); total += size; largest = max(largest, size)
            if case['root'] not in SELECTED[label]:
                continue
            displayed += 1
            root = lambda r: str(coordinate(label, data['roots'][r])).replace(' ', '')
            names = {v[0]: k for k, v in enumerate(nodes, 1)}
            text += ['## '+label.upper()+' target '+str(index)+', p='+root(case['root']), '',
                     'Variables: '+', '.join('X'+str(k+1)+' in A_'+root(r)
                                           for k, (r, e) in enumerate(case['variables']))+'.',
                     'Requested coefficient: '+str(case['coefficient'])+'.', '',
                     '| Line | Element | Root | Carpet applications |',
                     '|---|---|---|---|']
            for key, a, b, var, left, right in nodes:
                code, r = divmod(key, nr)
                parts = []
                for k, (rr, bound) in enumerate(case['variables'], 1):
                    code, exponent = divmod(code, bound+1)
                    if exponent:
                        parts.append('X'+str(k)+('^'+str(exponent) if exponent > 1 else ''))
                c = 2**a*3**b
                expression = (str(c)+'*' if c != 1 else '')+'*'.join(parts)
                if var >= 0:
                    reason = 'initial'
                else:
                    applications = []
                    for edge in [left, right]:
                        rule, lkey, rkey = edge
                        rr, ss, k, i, j, cc = data['rules'][rule]
                        value = (str(cc)+'*' if cc != 1 else '')
                        value += 'z'+str(names[lkey])+('^'+str(i) if i > 1 else '')
                        value += '*z'+str(names[rkey])+('^'+str(j) if j > 1 else '')
                        if value not in applications:
                            applications.append(value)
                    reason = '; '.join(applications)
                    if left != right:
                        reason += '; gcd('+str(edge_coefficient(left))+','+str(edge_coefficient(right))+')='+str(c)
                text.append('| z'+str(names[key])+' | '+expression+' | '+root(r)+' | '+reason+' |')
            text += ['']
        path = Path(prefix+'short-certificate.jsonl')
        path.write_text(''.join(json.dumps(v, separators=(',', ':'))+'\n' for v in rows))
        reports.append(dict(type=label, cases=len(rows), nodes=total, largest=largest, representatives=displayed))
        print('PASS_1962_SHORT_PROOFS', label, len(rows), total, largest, displayed, flush=True)
    assert sum(v['representatives'] for v in reports) == 19
    Path('research/19.62-rank-two-derivations.md').write_text('\n'.join(text))
    return reports


if __name__ == '__main__':
    Path('results/19.62-rank-two-short-summary.json').write_text(json.dumps(run(), indent=2)+'\n')
