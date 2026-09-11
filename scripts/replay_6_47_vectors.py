#!/usr/bin/env python3
"""Compare full independent vector cosets with all frozen GAP enumerations."""
import json
from pathlib import Path

from word_vectors_6_47 import enumerate_derived, verify_certificate, normalized_export
from run_6_47_extension import check
from classify_6_47_tables import classify

ROOT = Path(__file__).resolve().parents[1]


def run():
    records = []
    for packet in ['pilot', 'extension']:
        summary = json.loads((ROOT/f'results/6.47-{packet}-summary.json').read_text())
        for case in summary['cases']:
            if case['status'] != 'EXPORTED':
                continue
            stem = f"results/6.47-{packet}-{case['n']}-{case['id']}"
            data = json.loads((ROOT/(stem+'.json')).read_text())
            old_controls = json.loads((ROOT/(stem+'-controls.json')).read_text())
            certificate = enumerate_derived(data)
            verified = verify_certificate(data, certificate)
            assert verified['complete']
            result = normalized_export(data, certificate)
            # Compare actual vectors, not just their number or group order.
            assert {tuple(v) for v in result['word_functions']} == {
                tuple(v) for v in data['word_functions']}
            controls = check(result)
            tables = lambda rows: {tuple(map(tuple, r['table']))
                                   for r in rows['associative_operations']}
            assert tables(controls) == tables(old_controls)
            assert classify(result, controls)['all_variety_memberships_certified']
            assert data['function_group_order'] == result['function_group_order']
            # Force the independent search to stop before completion.
            capped = enumerate_derived(data, cap=max(1,certificate['node_count']-1))
            cap_verified = verify_certificate(data, capped)
            assert not cap_verified['complete']
            assert set(capped['vectors_hex']).issubset(certificate['vectors_hex'])
            records.append({'n': data['n'], 'id': data['id'], 'source': stem+'.json',
                            'normalized_operations': result['normalized_count'],
                            'associative_count': controls['associative_count'],
                            'triples': controls['checked_triples'],
                            'certificate_checks': verified, 'cap_control': cap_verified})
    assert len(records) == 26
    assert sum(r['normalized_operations'] for r in records) == 911
    return {'status': 'PASS_647_VECTOR_REGRESSION', 'cases': records,
            'scope': 'Full vector sets and associative tables agree with 26 frozen GAP enumerations.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
