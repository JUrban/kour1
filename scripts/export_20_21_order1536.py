#!/usr/bin/env python3
"""Export every retained kernel table, then compress only completed outputs."""
import ast
from datetime import datetime,timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while block:=f.read(2**20):h.update(block)
    return h.hexdigest()


def main():
    search=json.loads((ROOT/'results/20.21-order1536-interval-summary.json').read_text())
    assert search['status']=='COMPLETE_NO_CANDIDATE' and all(j['returncode']==0 for j in search['jobs'])
    rows=[]
    for job in search['jobs']:
        for p,h in job['sha256'].items():assert sha(ROOT/p)==h
        rows.extend(ast.literal_eval(line) for line in (ROOT/job['rows']).read_text().splitlines())
    rows.sort();assert len(rows)==search['totals']['both']
    script=ROOT/'scripts/export_20_21_interval_kernels.g'
    summary=ROOT/'results/20.21-order1536-export-summary.json'
    assert not summary.exists()
    report=dict(status='RUNNING',started_utc=datetime.now(timezone.utc).isoformat(),
                script_sha256=sha(script),runner_sha256=sha(__file__),workspace_mib_each=512,jobs=[])
    started=time.monotonic();processes=[];handles=[]
    try:
        for i in range(4):
            subset=rows[i::4];targets=[r[:2] for r in subset]
            prefix=ROOT/f'results/20.21-order1536-export-shard{i}'
            source=Path(str(prefix)+'.g');log=Path(str(prefix)+'.log');raw=Path(str(prefix)+'-tables.grows')
            compressed=Path(str(raw)+'.gz')
            assert not any(p.exists() for p in [source,log,raw,compressed])
            source.write_text('Targets2021:='+json.dumps(targets,separators=(',',':'))+';\nExportRows2021:='+json.dumps(str(raw))+';\n')
            command=[str(ROOT/'bin/gap'),'-o','512m',str(source),str(script)]
            handle=log.open('w');handles.append(handle)
            process=subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=handle,stderr=subprocess.STDOUT)
            processes.append(process)
            report['jobs'].append(dict(index=i,pid=process.pid,command=command,returncode=None,
                                       groups=len(targets),kernels=sum(len(r[2])+len(r[3]) for r in subset),
                                       input=str(source.relative_to(ROOT)),log=str(log.relative_to(ROOT)),
                                       raw=str(raw.relative_to(ROOT)),compressed=str(compressed.relative_to(ROOT))))
        print(json.dumps(report),flush=True)
        for process,job in zip(processes,report['jobs']):
            job['returncode']=process.wait();assert job['returncode']==0
            job['observed_completion_utc']=datetime.now(timezone.utc).isoformat()
            output=(ROOT/job['log']).read_text()
            assert not re.search(r'Error|Syntax warning|Traceback|Assertion failure',output)
            values=re.findall(r'PASS_2021_KERNEL_EXPORT\s*(\[[^\]]+\])',output)
            assert len(values)==output.count('PASS_2021_KERNEL_EXPORT')==1
            assert ast.literal_eval(values[0])==[job['groups'],job['kernels']]
            digest=hashlib.sha256();size=0
            with (ROOT/job['raw']).open('rb') as f,(ROOT/job['compressed']).open('wb') as target:
                with gzip.GzipFile(filename='',mode='wb',fileobj=target,mtime=0,compresslevel=6) as z:
                    while block:=f.read(2**20):digest.update(block);size+=len(block);z.write(block)
            job['raw_sha256']=digest.hexdigest();job['raw_bytes']=size
            job['sha256']={p:sha(ROOT/p) for p in [job['input'],job['log'],job['compressed']]}
            print('PASS_2021_EXPORT_SHARD',job['index'],job['groups'],job['kernels'],flush=True)
    finally:
        for process in processes:
            if process.poll() is None:process.terminate()
        for process in processes:process.wait()
        for handle in handles:handle.close()
    assert sha(script)==report['script_sha256']
    report.update(status='COMPLETE',groups=len(rows),kernels=sum(j['kernels'] for j in report['jobs']),
                  elapsed_seconds=time.monotonic()-started,completed_utc=datetime.now(timezone.utc).isoformat())
    summary.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS_2021_ORDER1536_EXPORT',report['groups'],report['kernels'],flush=True)


if __name__=='__main__':main()
