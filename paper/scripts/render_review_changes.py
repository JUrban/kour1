#!/usr/bin/env python3
"""Validate exact before/after excerpts and render the revision appendix."""
import argparse,hashlib,json
from pathlib import Path
from make_inventory import tex
PAPER=Path(__file__).resolve().parents[1]
REV=PAPER/'reviews/revision-2026-09-17'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 baseline=json.loads((REV/'baseline.json').read_text());revised=json.loads((REV/'revised-version.json').read_text());changes=json.loads((REV/'changes.json').read_text())
 out=[r'''\section{Changes following external review}
\label{app:review-changes}
This appendix compares the reviewed 15 September version with the
first review revision of 17 September (local commit \artifact{f9e1956}).
The later reorganization of the paper is recorded at the end of this
appendix. Quotations and file locations refer to their respective historical
versions, before that reorganization. The first review revision's PDF is
preserved as \artifact{paper/versions/kourovka-experiment-2026-09-17-review.pdf}.
The 15 September baseline PDF is preserved as
\artifact{paper/versions/kourovka-experiment-2026-09-15.pdf}; its SHA-256 is
\begin{center}\small
\nolinkurl{ec9a5482cdfb9ee2b3937fd1980eed6448ab5f954454c9d5287d06aa8a4c3c25}.
\end{center}
The local baseline manuscript commit is \artifact{8a59409}; its public
filtered counterpart is \artifact{315e6c4ddf3b67aca8c97506f078cdc98d5413c1}.
Before/after quotations below are exact source excerpts, typeset with
this paper's macros. Their file locations are relative to \artifact{paper/};
section numbers can change when material moves. The structured change
record and source copies of both versions are in
\artifact{paper/reviews/revision-2026-09-17/}. A validation script checks
each quotation against its version. The deadline candidate ledger,
research artifacts and usage measurements have not been rewritten.
''']
 for i,r in enumerate(changes,1):
  old=REV/'baseline-source'/r['path'];current=REV/'revised-source'/r['path']
  assert hashlib.sha256(old.read_bytes()).hexdigest()==baseline['inputs'][r['path']]['sha256'],r['path']
  assert hashlib.sha256(current.read_bytes()).hexdigest()==revised['source_sha256'][r['path']],r['path']
  assert r['before'] in old.read_text(),('before',r['title']);assert r['after'] in current.read_text(),('after',r['title'])
  out.append('\\subsection{'+tex(r['title'])+'}\n\\noindent\\textbf{Review point.} '+tex(r['issue'])+'.\\par\n\\noindent\\textbf{Location.} \\artifact{'+r['path']+'}.\n')
  out.append('\\paragraph{Original text.}\n\\begin{quote}\\small\n'+r['before']+'\n\\end{quote}\n')
  out.append('\\paragraph{Revised text.}\n\\begin{quote}\\small\n'+r['after']+'\n\\end{quote}\n')
  out.append('\\noindent\\textbf{Reason.} '+tex(r['rationale'])+'\n\n\\noindent\\textbf{Validation.} '+tex(r['validation'])+'\n')
 out.append(r'''
\subsection{Withdrawn objections and retained scope}
The follow-up withdraws the algebraic-closedness objection to 16.28(a):
the original field was already the algebraic closure of \(\F_5(t)\).
That proof is unchanged. We retain characteristic five in part (b),
without asserting the identical conjugacy-class argument over every odd
characteristic. The suggested unrestricted extension is unnecessary;
in characteristic three its trace-one class does not have the same
semisimple description.

For 12.40, the follow-up accepts that nonexistence of any finite-valued
bound is a negative answer to the printed question. No proof change is
needed. The estimated count of ``roughly seven'' unintended readings,
the speculation about proposer intent, and the priority inference from
artifact dates are withdrawn in the follow-up and are not adopted here.
Proof length and speed of formalisation are not measures of discovery
difficulty. The original reports retain those earlier statements solely
as part of the correspondence record.

For 15.65, the source-index discrepancy discussed in its proof remains
explicit. The revision does not claim a new resolution of that discrepancy.
For 21.114, the external follow-up checks the retained order-512 inputs,
their central quotients and derived series. The order-8,192 construction
in the paper still uses the subsequent central-product argument; the
report is not described as a direct enumeration of that final group.
The 46 historical candidate classifications and their unresolved priority
status remain unchanged.

\subsection{Correspondence, packaging and validation records}
The four documents reproduced next were added to the manuscript without
rewriting their words. The lightly updated first report is retained as
\artifact{external-reviews/review-update1.md}, with its exact diff in
\artifact{external-reviews/review-update1.diff}. The final reply corrects
our first reply's claims about bundle completeness and large-certificate
availability. The digest manifest binds the raw documents and their
rendered counterparts. Markdown headings and tables have print formatting;
this does not change the review text or its historical references.

Both source bundles include the correspondence and the missing small
certificate. The full source additionally includes the retrieval index,
structured change record, baseline excerpts and PDF, and revision checks.
The build receipt, structure audit and portable-validation receipt bind
the resulting sources, PDF and ancillary inputs. The latter records all
four documented ancillary executions after archive extraction, and a
standalone typesetting comparison. The supplemental symbolic check of
the 14.72 restriction is an exact algebra check, not a formalisation of
the geometric proof. None of these checks is a fresh replay of the
undistributed 20.100 certificate or of all the reviewer's programs.
''')
 out.append((PAPER/'reviews/polish-2026-09-17/editorial-changes.tex').read_text())
 out.append('\\input{appendices/v2-changes}\n')
 result='\n'.join(out);dest=PAPER/'appendices/review-changes.tex'
 if args.check:assert dest.read_text()==result,'stale change appendix'
 else:dest.write_text(result)
 print(f'Validated {len(changes)} exact before/after pairs against bound baseline sources.')
if __name__=='__main__':main()
