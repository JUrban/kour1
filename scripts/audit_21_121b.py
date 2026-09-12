#!/usr/bin/env python3
"""Cross-check the new native/integer controls and their process records."""
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]


def read_run(name):
    stem=ROOT/('results/21.121b-normal-sylow-'+name)
    record=json.loads(pathlib.Path(str(stem)+'-process.json').read_text())
    out=pathlib.Path(str(stem)+'.log').read_bytes()
    err=pathlib.Path(str(stem)+'.stderr').read_bytes()
    sha=lambda b:hashlib.sha256(b).hexdigest()
    assert record['actual_returncode']==0 and record['accepted'] and not record['timed_out']
    assert not err and sha(err)==record['stderr_sha256']
    assert sha(out)==record['stdout_sha256'] and out.count(b'PASS_21_121B_')==1
    script=next(ROOT/x for x in record['command'] if pathlib.Path(x).suffix in ('.g','.py') and (ROOT/x).is_file())
    assert sha(script.read_bytes())==record['script_sha256']
    text=out.decode().lstrip()
    decoder=json.JSONDecoder()
    rows=[]
    while text.startswith('{'):
        row,end=decoder.raw_decode(text)
        rows.append(row)
        text=text[end:].lstrip()
    assert text.startswith('PASS_21_121B_') and len(text.splitlines())==1
    return rows


def main():
    native=read_run('native')
    independent=read_run('independent')
    assert len(native)==11 and len(independent)==8
    a={r['model']:r for r in native}
    assert {r['model'] for r in independent}=={f'affine_{q}' for q in [2,3,4,5,7,8,9,16]}
    for row in independent:
        other=a[row['model']]
        for key in ['order','p','subgroups','histogram']:
            assert row[key]==other[key],(row['model'],key)
        assert sum(h[3] for h in row['histogram'])==row['subgroups']
    soluble_native=read_run('soluble-native')
    soluble_independent=read_run('soluble-independent')
    assert len(soluble_native)==11 and len(soluble_independent)==8
    b={(r['model'],r['p']):r for r in soluble_native}
    assert len(b)==11
    for row in soluble_independent:
        other=b[(row['model'],row['p'])]
        for key,value in other.items():
            assert row[key]==value,(row['model'],row['p'],key)
    neg=b[('a5_negative_control',2)]
    assert neg['J']==1 and neg['minimum_index']==60 and neg['quadratic_bound']==16
    for r in soluble_native:
        if r['model']!='a5_negative_control':
            assert r['constructed_index']<=r['quadratic_bound']
            assert r['p_prime_core_order']//r['cd_order']<=r['J']**2
    source=json.loads((ROOT/'results/21.121b-normal-sylow-source-download.json').read_text())
    assert source['http_status']==200
    for r in source['files']:
        data=(ROOT/r['path']).read_bytes()
        assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    result=dict(status='PASS',outside_reviews=0,new_complete_candidates=0,
                normal_sylow_native_models=11,normal_sylow_subgroup_classes=sum(r['subgroup_classes'] for r in native),
                normal_sylow_subgroups=sum(r['subgroups'] for r in native),
                abelian_complement_choices=sum(r['abelian_complement_choices'] for r in native),
                matched_affine_models=8,matched_affine_subgroups=sum(r['subgroups'] for r in independent),
                field_triples=sum(r['field_triples'] for r in independent),
                soluble_native_positive_models=10,soluble_native_negative_controls=1,
                matched_soluble_or_negative_models=8,
                integer_associativity_triples=sum(r['associativity_triples'] for r in soluble_independent),
                native_only_soluble_models=[list(key) for key in b if key not in {(r['model'],r['p']) for r in soluble_independent}])
    (ROOT/'results/21.121b-normal-sylow-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    print('PASS_21_121B_AUDIT')


if __name__=='__main__':
    main()
