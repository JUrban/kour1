#!/usr/bin/env python3
"""Validate both edition archives and the common source tree outside the repository."""
import hashlib,json,os,re,shutil,subprocess,sys,tarfile,tempfile,zipfile
from pathlib import Path
from datetime import datetime,timezone
from edition_sources import ENTRIES,OUTPUTS
PAPER=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check_manifest(root,name):
    m=json.loads((root/name).read_text())
    for n,r in m.items():
        f=root/n;assert f.is_file() and f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],n
    return m

def main():
    tectonic=os.environ.get('PAPER_TECTONIC') or shutil.which('tectonic') or str(PAPER.parent/'software/paper-toolchain/tectonic')
    tectonic=str(Path(tectonic).resolve());commands=[];results={};build=PAPER/'build'
    def run(command,cwd,name):
        r=subprocess.run(command,cwd=cwd,capture_output=True,text=True)
        (build/name).write_text(r.stdout+r.stderr)
        commands.append({'command':command,'location':cwd.name,'exit_code':r.returncode,'log':name})
        if r.returncode:raise RuntimeError(f'{command}: {r.stdout[-1500:]} {r.stderr[-1500:]}')
    with tempfile.TemporaryDirectory(prefix='kourovka-v4-') as temporary:
        root=Path(temporary);assert PAPER.parent not in root.parents
        full=root/'shared-source';full.mkdir()
        with zipfile.ZipFile(PAPER/'dist/kourovka-experiment-full-source.zip') as z:
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(full)
        fullmanifest=check_manifest(full,'SOURCE-MANIFEST.json')
        for script,args in [('make_inventory.py',['--require-complete']),('render_review_changes.py',['--check']),('render_editions.py',['--check']),('audit_reader_revision.py',[]),('audit_v2.py',[]),('audit_v3.py',[]),('audit_v4.py',[])]:
            run([sys.executable,'scripts/'+script,*args],full,'portable-'+script.removesuffix('.py')+'.log')
        # Inventory regeneration must reproduce the packaged current inventory.
        for n in ['sections/inventory.tex','sections/candidate-proofs.tex']:
            assert sha(full/n)==fullmanifest[n]['sha256']
        run([sys.executable,'reviews/v2-2026-09-19/check_identities.py'],full,'portable-v2-identities.log')
        ancillary_roots=[]
        for edition,entry in ENTRIES.items():
            dest=root/edition;dest.mkdir();stem=Path(entry).stem
            with tarfile.open(PAPER/'dist'/(OUTPUTS[edition]+'-arxiv-source.tar.gz')) as t:
                assert all(m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts for m in t.getmembers())
                t.extractall(dest,filter='data')
            m=check_manifest(dest,'anc/SOURCE-MANIFEST.json')
            run([tectonic,'--only-cached','--keep-logs',entry],dest,'portable-'+edition+'-tex.log')
            log=(dest/f'{stem}.log').read_text()
            assert not re.search(r'undefined|multiply defined|Overfull|LaTeX Warning',log,re.I),(edition,'TeX diagnostics')
            current=subprocess.check_output(['pdftotext','-layout',str(PAPER/'build'/edition/f'{stem}.pdf'),'-'])
            portable=subprocess.check_output(['pdftotext','-layout',str(dest/f'{stem}.pdf'),'-'])
            assert current==portable,('portable PDF differs',edition)
            info=subprocess.check_output(['pdfinfo',str(dest/f'{stem}.pdf')],text=True)
            results[edition]={'status':'PASS','archive_members_checked':len(m),'pages':int(re.search(r'Pages:\s+(\d+)',info)[1]),
              'tex_input_sha256':{n:r['sha256'] for n,r in m.items() if n.endswith(('.tex','.bib','.bbl','.pdf')) or n.startswith('external-reviews/')},
              'ancillary_original_manifest_sha256':sha(dest/'anc/manifest.json'),
              'pdf_text_sha256':hashlib.sha256(portable).hexdigest()}
            ancillary_roots.append(dest/'anc')
        assert results['full']['ancillary_original_manifest_sha256']==results['mathematics']['ancillary_original_manifest_sha256']
        for script in ['verify_19_62_rank_two.py','verify_19_61_square_completion.py','check_19_62_g2_integer_constants.py','verify_19_62_monomial_certificates.py']:
            run([sys.executable,'scripts/'+script],ancillary_roots[1],'portable-'+script.removesuffix('.py')+'.log')
        for anc in ancillary_roots:
            for r in json.loads((anc/'manifest.json').read_text())['files']:assert sha(anc/r['path'])==r['sha256']
        for d in [full,root/'full',root/'mathematics']:
            for name in ['editors-reply1.md','editors-reply2.md','editors-reply3.md']:assert not (d/'external-reviews'/name).exists()
        result={'status':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),
          'scope':'Three archives extracted outside Git; manifests, shared/current/historical source checks, two standalone cached TeX builds, both PDF text comparisons, v2 exact identities and all four ancillary proof checks. All three raw editor emails excluded. No new verification of all mathematical arguments or large omitted certificates.',
          'shared_source_members_checked':len(fullmanifest),'editions':results,'commands':commands}
    (PAPER/'reviews/portable-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'commands','editions'}},indent=2))
    print({e:{k:v for k,v in r.items() if k!='tex_input_sha256'} for e,r in results.items()})
    print(f'All {len(commands)} execution commands exited zero.')
if __name__=='__main__':main()
