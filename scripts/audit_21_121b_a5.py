#!/usr/bin/env python3
"""Compare the independent two-factor enumeration and GAP class weights."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def read_run(name):
    prefix=ROOT/('results/21.121b-normal-sylow-a5-'+name)
    record=json.loads(Path(str(prefix)+'-process.json').read_text())
    out=Path(str(prefix)+'.log').read_bytes();err=Path(str(prefix)+'.stderr').read_bytes()
    sha=lambda b:hashlib.sha256(b).hexdigest()
    assert record['accepted'] and record['actual_returncode']==0 and not record['timed_out']
    assert not err and sha(err)==record['stderr_sha256'] and sha(out)==record['stdout_sha256']
    assert sha((ROOT/record['command'][-1]).read_bytes())==record['script_sha256']
    assert out.count(b'PASS_21_121B_')==1
    # GAP's terminal formatter wraps a long JSON string using backslash-newline.
    # Only the parser removes those continuations; raw stdout is unchanged.
    text=out.decode().replace('\\\n','').lstrip();decoder=json.JSONDecoder();rows=[]
    while text.startswith('{'):
        row,end=decoder.raw_decode(text);rows.append(row);text=text[end:].lstrip()
    assert text.startswith('PASS_21_121B_') and len(text.splitlines())==1
    return rows


def main():
    native=read_run('native');independent=read_run('independent')
    assert len(native)==len(independent)==2
    for a,b in zip(native,independent):
        assert all(a[k]==v for k,v in b.items())
        assert sum(n for key,n in a['histogram'])==a['subgroups']
        for (order,power,index,r,border,bp),count in a['histogram']:
            assert order==60**r*border and power==4**r*bp
            assert index<=60**r*bp**2 and count>0
    assert [a['subgroups'] for a in native]==[59,8381]
    assert [a['subgroup_classes'] for a in native]==[9,113]
    old=json.loads((ROOT/'results/21.121b-packet.json').read_text())
    for row in old['files']:
        data=(ROOT/row['path']).read_bytes()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    result=dict(status='PASS',candidate_count=46,new_complete_candidates=0,outside_reviews=0,
                matched_models=2,subgroups=[59,8381],native_classes=[9,113],
                old_soluble_packet_bindings_unchanged=len(old['files']))
    (ROOT/'results/21.121b-a5-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True));print('PASS_21_121B_A5_AUDIT')


if __name__=='__main__':main()
