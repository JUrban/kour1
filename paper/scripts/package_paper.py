#!/usr/bin/env python3
"""Package two PDFs, two standalone TeX archives and one shared full source ZIP."""
import gzip,hashlib,io,json,shutil,tarfile,zipfile
from pathlib import Path
from edition_sources import ENTRIES,OUTPUTS,sources
from public_review_files import public_review_files
PAPER=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()
def manifest(files):return json.dumps({n:{'bytes':len(b),'sha256':digest(b)} for n,b in sorted(files.items())},indent=2).encode()+b'\n'
def main():
    dist=PAPER/'dist';dist.mkdir(exist_ok=True);products=[];union={}
    for edition,entry in ENTRIES.items():
        stem=Path(entry).stem;build=PAPER/'build'/edition
        receipt=json.loads((build/'build-receipt.json').read_text())
        pdf=(build/f'{stem}.pdf').read_bytes()
        assert receipt['exit_code']==0 and receipt['edition']==edition and digest(pdf)==receipt['pdf_sha256']
        for n,h in receipt['source_sha256'].items():assert digest((PAPER/n).read_bytes())==h,('stale build',edition,n)
        files={n:(PAPER/n).read_bytes() for n in sources(PAPER,edition)}
        files['references.bib']=(PAPER/'references.bib').read_bytes()
        files[f'{stem}.bbl']=(build/f'{stem}.bbl').read_bytes()
        if edition=='full':
            files['figures/trajectory.pdf']=(PAPER/'figures/trajectory.pdf').read_bytes()
            for f in public_review_files(PAPER):files[str(f.relative_to(PAPER))]=f.read_bytes()
        union.update(files)
        for f in sorted((PAPER/'ancillary').rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts:
                files['anc/'+str(f.relative_to(PAPER/'ancillary'))]=f.read_bytes()
        files['anc/SOURCE-README.txt']=(
            f'{edition.capitalize()} edition. Compile {entry} from the archive root with Tectonic, or XeLaTeX and BibTeX. '
            f'{stem}.bbl is included. The other edition uses the same shared mathematical files in the full source archive.\n'
            'No shell escape or network retrieval is required with the TeX packages installed. '
            'The anc directory contains portable carpet proof inputs and four checkers; see anc/README.md. '
            'These archives have not been submitted.\n').encode()
        files['anc/SOURCE-MANIFEST.json']=manifest(files)
        target=dist/(OUTPUTS[edition]+'-arxiv-source.tar.gz')
        with target.open('wb') as stream:
            with gzip.GzipFile(filename='',mode='wb',fileobj=stream,mtime=0) as gz:
                with tarfile.open(fileobj=gz,mode='w') as archive:
                    for n,b in sorted(files.items()):
                        info=tarfile.TarInfo(n);info.size=len(b);info.mode=0o644;info.mtime=0
                        archive.addfile(info,io.BytesIO(b))
        handoff=dist/(OUTPUTS[edition]+'.pdf');handoff.write_bytes(pdf)
        (PAPER/handoff.name).write_bytes(pdf);products.extend([handoff,target])
    for name in ['README.md','PLAN.md','STATUS.md']:union[name]=(PAPER/name).read_bytes()
    for folder in ['scripts','data','reviews','ancillary','figures','versions']:
        for f in sorted((PAPER/folder).rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts and f.suffix not in {'.log','.aux','.synctex','.xdv'}:
                union[str(f.relative_to(PAPER))]=f.read_bytes()
    union['SOURCE-MANIFEST.json']=manifest(union)
    target=dist/'kourovka-experiment-full-source.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for n,b in sorted(union.items()):
            info=zipfile.ZipInfo(n,(2026,9,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,b)
    products.append(target)
    result={f.name:{'bytes':f.stat().st_size,'sha256':digest(f.read_bytes())} for f in products}
    (dist/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
