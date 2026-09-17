#!/usr/bin/env python3
"""Index only structured completed web-tool observations in the supplied JSONL.

No reasoning, command bodies, snippets, system/developer messages or compaction
summaries are exported. A result URL records visibility in the tool response;
it does not establish opening, reading, use, or source independence.
"""
import argparse, collections, csv, hashlib, io, json
from pathlib import Path
from analyze_rollout import phase
PAPER=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path);ap.add_argument('--check',action='store_true');args=ap.parse_args()
 if args.input: source=args.input
 else:
  candidates=list((PAPER.parent/'session').glob('rollout-*.jsonl'));assert len(candidates)==1;source=candidates[0]
 observations=[];digest=hashlib.sha256();size=0;exact_url=b'https://github.com/TPColor/kourovka-notebook-problem-21.106';hits=0
 for number,line in enumerate(source.open('rb'),1):
  digest.update(line);size+=len(line);hits+=line.count(exact_url)
  row=json.loads(line);p=row.get('payload',{});it=p.get('item',{})
  if p.get('type')!='item_completed' or it.get('type')!='Extension' or not it.get('kind','').startswith('web.'):continue
  action=it.get('action',{});results=it.get('results',[])
  observations.append({'line':number,'timestamp':row['timestamp'],'phase':phase(row['timestamp']),'kind':it['kind'],
   'action':action,'display_query':it.get('query',''),
   'result_links':[{'url':r['url'],'ref_id':r.get('ref_id',''),'title':r.get('title','')} for r in results if isinstance(r,dict) and r.get('url','').startswith(('https://','http://'))]})
 urls={}
 def record(url,ob,role):
  if not url.startswith(('https://','http://')):return
  if url not in urls:urls[url]={'url':url,'first_utc':ob['timestamp'],'last_utc':ob['timestamp'],'requested_action_count':0,'result_visibility_count':0}
  urls[url]['last_utc']=ob['timestamp'];urls[url][role]+=1
 for ob in observations:
  record(ob['action'].get('url') or '',ob,'requested_action_count')
  for url in {r['url'] for r in ob['result_links']}:record(url,ob,'result_visibility_count')
 out=io.StringIO();writer=csv.DictWriter(out,lineterminator='\n',fieldnames=['url','first_utc','last_utc','requested_action_count','result_visibility_count']);writer.writeheader();writer.writerows(urls[u] for u in sorted(urls))
 metrics={'input_bytes':size,'input_sha256':digest.hexdigest(),'web_observations':len(observations),'phase_counts':dict(collections.Counter(o['phase'] for o in observations)),'action_counts':dict(collections.Counter(o['action'].get('type') for o in observations)),'distinct_urls':len(urls),'exact_repository_url':exact_url.decode(),'exact_url_occurrences_in_raw_input':hits,'scope':'Structured completed web observations only; shell downloads are not indexed. Search-result visibility is distinct from a requested page action and from evidence of mathematical use. The raw trace remains separately retained; this index alone cannot prove absence of exposure.'}
 outputs={'retrieval-observations.jsonl':''.join(json.dumps(o,ensure_ascii=False)+'\n' for o in observations),'retrieval-urls.csv':out.getvalue(),'retrieval-metrics.json':json.dumps(metrics,indent=2)+'\n'}
 for name,value in outputs.items():
  path=PAPER/'data'/name
  if args.check:assert path.read_bytes()==value.encode(),('stale',name)
  else:path.write_bytes(value.encode())
 print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
