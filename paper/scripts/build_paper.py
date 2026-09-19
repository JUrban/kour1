#!/usr/bin/env python3
"""Build either or both editions from shared sources, recording each invocation."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from edition_sources import ENTRIES,sources
from public_review_files import public_review_files
PAPER=Path(__file__).resolve().parents[1]
ROOT=PAPER.parent

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--require-complete',action='store_true')
    ap.add_argument('--edition',choices=['all',*ENTRIES],default='all')
    args=ap.parse_args()
    command=[sys.executable,str(PAPER/'scripts/make_inventory.py')]
    if args.require_complete:command.append('--require-complete')
    subprocess.run(command,cwd=ROOT,check=True)
    for script in ['render_editions.py','render_review_changes.py','render_v2_changes.py','render_v3_changes.py','render_v4_changes.py']:
        subprocess.run([sys.executable,str(PAPER/'scripts'/script),'--check'],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(PAPER/'scripts/audit_v4.py')],cwd=ROOT,check=True)
    correspondence=json.loads((PAPER/'external-reviews/manifest.json').read_text())
    for record in correspondence['documents']:
        for pathkey,hashkey in [('path','sha256'),('rendered_path','rendered_sha256')]:
            if pathkey in record:
                assert hashlib.sha256((PAPER/record[pathkey]).read_bytes()).hexdigest()==record[hashkey]
    tectonic=os.environ.get('PAPER_TECTONIC') or shutil.which('tectonic') or str(ROOT/'software/paper-toolchain/tectonic')
    if not Path(tectonic).is_file():raise SystemExit('Set PAPER_TECTONIC to a Tectonic binary.')
    for edition in ENTRIES if args.edition=='all' else [args.edition]:
        build=PAPER/'build'/edition;build.mkdir(parents=True,exist_ok=True)
        cmd=[tectonic,'--only-cached','--keep-logs','--keep-intermediates','--outdir',str(build.relative_to(PAPER)),ENTRIES[edition]]
        started=datetime.now(timezone.utc)
        with (build/'build-console.log').open('w') as log:
            result=subprocess.run(cmd,cwd=PAPER,stdout=log,stderr=subprocess.STDOUT)
        inputs=set(sources(PAPER,edition))|{'references.bib','figures/trajectory.pdf'}
        inputs|={str(x.relative_to(PAPER)) for x in public_review_files(PAPER)}
        receipt={'edition':edition,'entrypoint':ENTRIES[edition],'command':cmd,'cwd':str(PAPER),
          'exit_code':result.returncode,'started_utc':started.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),
          'version':subprocess.check_output([tectonic,'--version'],text=True).strip(),
          'source_sha256':{n:hashlib.sha256((PAPER/n).read_bytes()).hexdigest() for n in sorted(inputs)}}
        pdf=build/Path(ENTRIES[edition]).with_suffix('.pdf')
        if result.returncode==0 and pdf.is_file():
            receipt.update(pdf_bytes=pdf.stat().st_size,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
        (build/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        if result.returncode:
            print((build/'build-console.log').read_text()[-6000:]);raise SystemExit(result.returncode)
        (PAPER/'reviews/v4-2026-09-19'/f'{edition}-build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        # Retain the documented full-edition build locations for existing tooling.
        if edition=='full':
            for name in ['main.pdf','main.bbl','main.log','main.blg','build-receipt.json']:
                shutil.copyfile(build/name,PAPER/'build'/name)
            shutil.copyfile(build/'build-receipt.json',PAPER/'reviews/build-receipt.json')
        print(json.dumps({k:v for k,v in receipt.items() if k not in {'source_sha256','command'}},indent=2))
if __name__=='__main__':main()
