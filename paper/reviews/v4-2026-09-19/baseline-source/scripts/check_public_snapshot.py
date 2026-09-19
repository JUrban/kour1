#!/usr/bin/env python3
"""Compare the pinned public and unfiltered research snapshots; network required."""
import hashlib,json,subprocess,urllib.request,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[1]; local='cff2c37b9bf6b737e8ad5f7ead12291a551b5201';public='bbfac1ac810117da37f01716d4594dc2b2e96980'
def fetch(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'paper-revision'})).read()
data=json.loads(fetch(f'https://api.github.com/repos/JUrban/kour1/git/trees/{public}?recursive=1'));assert not data['truncated']
remote={r['path']:r for r in data['tree'] if r['type']=='blob'}
raw=subprocess.check_output(['git','-C',str(P.parent),'ls-tree','-rlz',local]);original={}
for line in raw.split(b'\0'):
 if not line:continue
 head,path=line.split(b'\t',1);mode,kind,oid,size=head.split()
 if kind==b'blob':original[path.decode()]={'sha':oid.decode(),'bytes':int(size)}
changed=[path for path in remote if path not in original or original[path]['sha']!=remote[path]['sha']]
assert not changed,changed
omitted=[{'path':path,**r} for path,r in original.items() if path not in remote]
print('Retained',len(remote),'omitted',len(omitted),'min omitted',min(r['bytes'] for r in omitted))
names=['research/complete-candidate-ledger.json','reports/FINAL_REPORT.md','results/19.62-g2-monomial-certificates.jsonl','results/15.92-summary.json','results/20.100-n7-integrity.json']
def check(name):
 b=fetch(f'https://raw.githubusercontent.com/JUrban/kour1/{public}/{name}');l=subprocess.check_output(['git','-C',str(P.parent),'show',local+':'+name]);assert b==l
 return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:checks=list(e.map(check,names))
pdf=fetch('https://raw.githubusercontent.com/JUrban/kour1/315e6c4ddf3b67aca8c97506f078cdc98d5413c1/paper/kourovka-experiment.pdf');assert pdf==(P/'versions/kourovka-experiment-2026-09-15.pdf').read_bytes()
result={'checked_utc':'2026-09-17','public_repository':'https://github.com/JUrban/kour1','filter_reported_by_owner':'--strip-blobs-bigger-than 90M','local_unfiltered_research_commit':local,'public_filtered_research_commit':public,'local_baseline_manuscript_commit':'8a59409','public_baseline_manuscript_commit':'315e6c4ddf3b67aca8c97506f078cdc98d5413c1','retained_blobs':len(remote),'retained_blob_git_ids_match':True,'comparison_scope':'Final research trees; not an assertion that commit hashes or complete histories are identical.','omitted_blobs':omitted,'byte_checked_public_files':checks,'baseline_pdf_sha256':hashlib.sha256(pdf).hexdigest(),'undistributed_n7':{'path':'results/20.100-n7-certificate.g.gz','bytes':1271256410,'sha256':'e1b116fa80a4b77a03256d69480b996318522c227ef48e6be7fdf62cbd8bcd8c'}}
(P/'data/public-artifacts.json').write_text(json.dumps(result,indent=2)+'\n')
print('Public snapshot and baseline PDF matched.')
