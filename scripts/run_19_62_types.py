#!/usr/bin/env python3
"""Run bounded disjoint intervals of the ten type certificates, with actual exits."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from prepare_19_62_types import TYPES


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    source='scripts/derive_19_62_types.cpp';binary='results/19.62-derive-types'
    expected=Path('results/19.62-g2-monomial-certificates.jsonl')
    control=Path('results/19.62-g2-monomial-generic-control.jsonl')
    assert expected.read_bytes()==control.read_bytes()
    assert Path('results/19.62-g2-monomial-generic-control.log').read_text().splitlines()[-1]=='PASS_1962_MONOMIAL_INTERVAL 1 2712 2712 0'
    jobs=[];started=time.monotonic();created=datetime.datetime.now(datetime.timezone.utc).isoformat()
    hashes={source:sha(source),binary:sha(binary)}
    for label in TYPES:
        path=Path('results/19.62-'+label+'-monomial-input.json');data=json.loads(path.read_text())
        text=path.with_suffix('.txt');hashes[str(path)]=sha(path);hashes[str(text)]=sha(text)
        for first in range(1,len(data['cases'])+1,1000):
            last=min(first+999,len(data['cases']));tag=f'19.62-{label}-{first}-{last}'
            log=Path('results/'+tag+'-generation.log');certificate=Path('results/'+tag+'-certificate.jsonl')
            assert not log.exists() and not certificate.exists()
            jobs.append(dict(type=label,first=first,last=last,log=str(log),certificate=str(certificate),
                             command=[binary,str(text),str(first),str(last),str(certificate)]))
    manifest=Path('results/19.62-types-launch-manifest.json');assert not manifest.exists()
    manifest.write_text(json.dumps(dict(created_utc=created,sha256=hashes,jobs=jobs,workers=4),indent=2)+'\n')
    def task(job):
        t=time.monotonic()
        with Path(job['log']).open('w') as f:p=subprocess.run(job['command'],stdout=f,stderr=subprocess.STDOUT,timeout=12000)
        job=dict(job,returncode=p.returncode,elapsed_seconds=time.monotonic()-t)
        output=Path(job['log']).read_text();match=re.findall(r'PASS_1962_MONOMIAL_INTERVAL (\d+) (\d+) (\d+) (\d+)',output)
        job['counts']=list(map(int,match[0])) if len(match)==1 else None
        job['sha256']={name:sha(name) for name in [job['log'],job['certificate']] if Path(name).exists()}
        print('OBSERVED_1962_TYPE_INTERVAL',job['type'],job['first'],job['last'],job['returncode'],job['counts'],flush=True)
        return job
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        completed=list(pool.map(task,jobs))
    success=all(j['returncode']==0 and j['counts']==[j['first'],j['last'],j['last']-j['first']+1,0] for j in completed)
    if success:
        for label in TYPES:
            path=Path('results/19.62-'+label+'-monomial-certificates.jsonl');assert not path.exists()
            with path.open('wb') as f:
                for j in completed:
                    if j['type']==label:f.write(Path(j['certificate']).read_bytes())
    result=dict(created_utc=created,elapsed_seconds=time.monotonic()-started,
                status='COMPLETE' if success else 'FAILED',jobs=completed,launch_sha256=sha(manifest))
    Path('results/19.62-types-generation-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    assert success,'not every target has a completed certificate'
    print('PASS_1962_ALL_TYPE_CERTIFICATES',len(completed),sum(j['last']-j['first']+1 for j in completed),flush=True)


if __name__=='__main__':main()
