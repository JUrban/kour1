#!/usr/bin/env python3
"""Audit the final report and archived evidence; never replay mathematics."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
DEADLINE=datetime(2026,9,12,20,56,46,tzinfo=timezone.utc)
EXTRA_MANIFESTS=[
    'results/review-handoff-packet.json',
    'results/pdf-statement-review-packet.json',
    'results/21.121b-packet.json',
    'results/21.121b-a5-packet.json',
    'results/21.121-permanence-packet.json',
    'results/21.121-finite-kernels-packet.json',
    'results/20.89-packet.json',
    'results/20.89-metabelian-packet.json',
    'results/20.89-char0-packet.json',
    'results/20.89-normal-algebra-packet.json',
    'results/20.89-bounded-torsion-packet.json',
    'results/20.124-packet.json',
    'results/17.118-packet.json',
    'results/21.114-packet.json',
    'results/18.120-summary.json',
    'results/6.47-vector-packet.json',
    'results/20.100-final-packet.json',
    'results/20.21-order1536-packet.json',
    'results/19.20-through511-summary.json',
    'results/18.43-summary.json',
]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['preflight','final'],required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args();tick=time.monotonic()
    output=ROOT/args.output
    if output.exists():raise FileExistsError('Use a fresh output path: '+str(output))
    now=datetime.now(timezone.utc)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))
    observations={};bindings=[];missing=set();untracked=set();mismatches=[];manifests=set();errors=[]

    def inspect(name):
        if name in observations:return observations[name]
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:raise ValueError(name)
        p=ROOT/rel
        if not p.is_file():missing.add(name);observations[name]=None;return None
        if name not in tracked:untracked.add(name)
        h=hashlib.sha256();size=0
        with p.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):
                h.update(block);size+=len(block)
        row=dict(path=name,bytes=size,sha256=h.hexdigest());observations[name]=row;return row

    def bind(source,row):
        current=inspect(row['path'])
        good=current is not None and current['sha256']==row['sha256'] and ('bytes' not in row or current['bytes']==row['bytes'])
        item=dict(source=source,path=row['path'],expected_sha256=row['sha256'],matches=good)
        if 'bytes' in row:item['expected_bytes']=row['bytes']
        bindings.append(item)
        if not good:mismatches.append(dict(item,observed=current))

    def audit_manifest(name):
        if name in manifests:return
        current=inspect(name)
        if current is None or not name.endswith('.json'):return
        obj=json.loads((ROOT/name).read_text())
        if not isinstance(obj,dict):return
        rows=[]
        if isinstance(obj.get('sha256'),dict):
            rows.extend(dict(path=n,sha256=h) for n,h in obj['sha256'].items() if isinstance(h,str))
        if isinstance(obj.get('files'),list):
            rows.extend(r for r in obj['files'] if isinstance(r,dict) and isinstance(r.get('path'),str) and isinstance(r.get('sha256'),str))
        if not rows:return
        manifests.add(name)
        for row in rows:
            bind(name,row)
            if row['path'].endswith(('-packet.json','-summary.json','-provenance.json')):audit_manifest(row['path'])

    checkpoint_name='results/candidate-handoff-integrity.json'
    checkpoint=json.loads((ROOT/checkpoint_name).read_text())
    assert checkpoint['status']=='PASS' and checkpoint['candidate_count']==46
    # These are explicitly the 19:00 checkpoint's current-file observations,
    # not retrospectively invented manifests for the early seventeen candidates.
    for row in checkpoint['current_file_observations']:bind(checkpoint_name+':current_file_observations',row)
    for name in sorted(set(checkpoint['historical_manifests']+EXTRA_MANIFESTS)):audit_manifest(name)
    ledger=json.loads((ROOT/'research/complete-candidate-ledger.json').read_text())
    assert ledger['candidate_count']==len(ledger['candidates'])==46
    assert [r['candidate_number'] for r in ledger['candidates']]==list(range(1,47))
    assert len({r['problem'] for r in ledger['candidates']})==46
    assert all(r['outside_reviews']==0 for r in ledger['candidates'])
    index={r['id']:r for r in json.loads((ROOT/'research/problem-index.json').read_text())}
    report=(ROOT/'reports/FINAL_REPORT.md').read_text()
    for row in ledger['candidates']:
        assert row['original_statement']==index[row['problem']]['text']
        assert row['statement_index_pdf_page']==index[row['problem']]['pdf_page']
        expected=f"| {row['problem']} | {row['covered_subparts']} | {row['result']} | [proof](../{row['principal_proofs'][0]}) |"
        assert report.count(expected)==1,row['problem']
    documents=['reports/FINAL_REPORT.md','research/closeout-plan.md','research/closeout-proof-review.md']
    links=[]
    for name in documents:
        inspect(name);p=ROOT/name
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in link or link.startswith('#'):continue
            target=(p.parent/link.split('#')[0]).resolve()
            relative=str(target.relative_to(ROOT));inspect(relative);links.append(dict(document=name,target=relative))
    for name in ['scripts/audit_final_closeout.py',checkpoint_name,'research/complete-candidate-ledger.json','reports/STATUS.md','research/PORTFOLIO.md']:
        inspect(name)
    ancestors={os.getpid()};pid=os.getpid()
    while pid>1:
        try:
            status=Path('/proc',str(pid),'status').read_text()
            pid=int(re.search(r'^PPid:\s+(\d+)',status,re.M).group(1));ancestors.add(pid)
        except (OSError,AttributeError):break
    ps=subprocess.check_output(['ps','-eo','pid,ppid,etimes,rss,pcpu,comm','--no-headers'],text=True)
    processes=[];live=[]
    for line in ps.splitlines():
        a=line.split(None,5)
        row=dict(pid=int(a[0]),ppid=int(a[1]),elapsed_seconds=int(a[2]),rss_kib=int(a[3]),pcpu=a[4],command_name=a[5])
        processes.append(row)
        if row['pid'] not in ancestors and a[5].lower().startswith(('gap','python','check_','verify_','run_','g++','cc1','clang')):live.append(row)
    if args.phase=='final':
        if now<DEADLINE:errors.append('The 48-hour deadline has not arrived.')
        if 'Draft closeout report' in report or 'still pending in this draft' in report:errors.append('Final report still has draft closeout wording.')
        if live:errors.append('Recognized mathematical processes remain live.')
    ok=not (missing or untracked or mismatches or errors)
    result=dict(status='PASS' if ok else 'FAIL',phase=args.phase,observed_utc=now.isoformat(),
                finished_utc=datetime.now(timezone.utc).isoformat(),deadline_utc=DEADLINE.isoformat(),
                elapsed_seconds=round(time.monotonic()-tick,6),head_before_audit=head,
                scope='Artifact availability, final-report links and candidate coverage, historical hashes, and process observation only. No mathematical verifier replay, new PDF visual review, outside acceptance, or priority certification.',
                candidate_count=46,outside_reviews=0,checkpoint_snapshot_bindings=len(checkpoint['current_file_observations']),
                total_bindings_checked=len(bindings),manifest_count=len(manifests),manifests=sorted(manifests),
                unique_files_hashed=sum(x is not None for x in observations.values()),
                unique_bytes_hashed=sum(x['bytes'] for x in observations.values() if x),local_link_count=len(links),
                missing_paths=sorted(missing),untracked_required_paths=sorted(untracked),hash_mismatches=mismatches,
                final_phase_errors=errors,live_mathematical_processes=live,processes=processes,
                current_file_observations=[observations[n] for n in sorted(observations) if observations[n]],bindings=bindings,links=links)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','phase','candidate_count','checkpoint_snapshot_bindings','total_bindings_checked','manifest_count','unique_files_hashed','unique_bytes_hashed','local_link_count','missing_paths','untracked_required_paths','hash_mismatches','final_phase_errors','live_mathematical_processes','elapsed_seconds']}))
    print('PASS_FINAL_CLOSEOUT_'+args.phase.upper() if ok else 'FAIL_FINAL_CLOSEOUT_'+args.phase.upper())
    return 0 if ok else 1


if __name__=='__main__':raise SystemExit(main())
