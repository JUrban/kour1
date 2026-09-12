#!/usr/bin/env python3
"""Close the authorized research window, audit its artifacts, and commit locally."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
DEADLINE = datetime(2026, 9, 12, 20, 56, 46, tzinfo=timezone.utc)
PREFIX = 'results/final-closeout'
FINAL_PATHS = [
    'reports/FINAL_REPORT.md', 'reports/STATUS.md', 'research/PORTFOLIO.md',
    'research/completion-audit.md', 'reports/final-closeout-audit.md',
    PREFIX + '-integrity.json', PREFIX + '.log', PREFIX + '.stderr',
    PREFIX + '-process.json', PREFIX + '-packet.json',
]


def git(*args, capture=False):
    if capture:
        return subprocess.check_output(['git', *args], cwd=ROOT)
    subprocess.run(['git', *args], cwd=ROOT, check=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def replace_once(text, old, new):
    assert text.count(old) == 1, repr(old)
    return text.replace(old, new, 1)


def write_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def main():
    now = datetime.now(timezone.utc)
    assert now >= DEADLINE, 'The authorized research window has not ended.'
    git('diff', '--quiet')
    git('diff', '--cached', '--quiet')
    before_untracked = git('ls-files', '--others', '--exclude-standard', '-z', capture=True)
    assert len(list(filter(None, before_untracked.split(b'\0')))) == 19
    for name in FINAL_PATHS[3:]:
        assert not (ROOT / name).exists(), 'Do not overwrite an earlier closeout: ' + name
    stamp = now.isoformat()

    report_path = ROOT / 'reports/FINAL_REPORT.md'
    report = report_path.read_text()
    report = replace_once(report,
        '**Draft closeout report — research is still active until 12 September 2026,\n'
        '20:56:46 UTC.** This draft records the current results and will receive the\n'
        'actual deadline observation and final artifact audit at closeout.',
        '**The 48-hour research window ended on 12 September 2026 at\n'
        '20:56:46 UTC.** The actual closeout observation was ' + stamp + '.\n'
        'The final artifact audit and local commit are administrative closeout\n'
        'records; they do not extend the mathematical research window.')
    report = replace_once(report, 'The current outcome is **46 complete solution candidates**',
                          'The final outcome is **46 complete solution candidates**')
    report = replace_once(report,
        'The latest partial packets are committed separately and leave the older\n'
        'candidate ledger and historical evidence unchanged. The final closeout\n'
        'manifest and actual terminal-state observation will be added at the deadline.\n'
        'No mathematical jobs were live at the most recent process inspection; the\n'
        'final inspection is still pending in this draft.',
        'The latest partial packets are committed separately and leave the older\n'
        'candidate ledger and historical evidence unchanged. The final closeout\n'
        'records are `results/final-closeout-integrity.json`, its separate actual-\n'
        'process receipt, and `results/final-closeout-packet.json`. The accompanying\n'
        '`reports/final-closeout-audit.md` records the final outcome and process\n'
        'observation; `research/completion-audit.md` maps the deliverables to the\n'
        'authorized task. The research window is closed.')
    report = replace_once(report,
        'necessary sources are committed. The final report and artifact audit will be committed together; Git will\n'
        'identify the exact closeout commit. A historical untracked file is not',
        'necessary sources are committed. The final report and artifact audit are\n'
        'archived together in the closeout commit, identified by Git. A historical untracked file is not')

    status_path = ROOT / 'reports/STATUS.md'
    status = status_path.read_text()
    status = replace_once(status,
        '**18.18:** A common-centralizer interpretation proves that the cofinite\n'
        'theory of finite groups is not computably enumerable. The question\n'
        'about its complement remains unresolved here. Partial result only,\n'
        'with no novelty claim; see `research/18.18-partial.md`.',
        '**18.18 (superseded partial stage):** The earlier common-centralizer\n'
        'argument proved non-enumerability of the cofinite theory and left its\n'
        'complement unresolved. That historical stage is retained in\n'
        '`research/18.18-partial.md`. The complete candidate now covers both\n'
        'questions; see `research/18.18-proof.md` and the canonical review guide.')
    lines = status.splitlines()
    assert lines[2].startswith('Updated: ')
    lines[2] = 'Updated: ' + stamp + '.'
    status = '\n'.join(lines) + '\n'
    status = replace_once(status,
        '- Active phase: proof audit, exact searches, and broader problem triage.',
        '- Phase: the 48-hour research window is closed; the review handoff contains '
        '46 complete solution candidates, with priority unestablished and no outside reviews. '
        'Start with `reports/FINAL_REPORT.md` and `reports/REVIEW_GUIDE.md`.')
    marker = '\n## Next work\n'
    assert status.count(marker) == 1
    status = status.split(marker)[0] + (
        '\n## Handoff after the research window\n\n'
        'The authorized 48-hour window ended on **2026-09-12 at 20:56:46 UTC**. '
        'Closeout was observed at ' + stamp + '. The canonical count is 46 complete '
        'solution candidates; none has outside acceptance or established priority. '
        'The final report distinguishes full proposed resolutions, proved partial '
        'results, bounded searches, and identified prior work.\n\n'
        'Independent mathematical and priority review remains follow-up work for '
        'the supplied portfolio. Unrestricted questions explicitly left open are '
        'not claimed solved. The final artifact and process records are indexed in '
        '`results/final-closeout-packet.json` and `reports/final-closeout-audit.md`. '
        'All commits remain local; no external messages, submissions, or Git pushes '
        'have been made.\n')
    portfolio_path = ROOT / 'research/PORTFOLIO.md'
    portfolio = portfolio_path.read_text() + (
        '\n\n## Final closeout: 12 September 2026\n\n'
        'The 48-hour research window ended at 20:56:46 UTC; actual closeout was '
        'observed at ' + stamp + '. The final canonical portfolio contains '
        '46 complete solution candidates, with zero outside reviews and no '
        'established priority. Historical counts above retain their checkpoint '
        'meaning. The last selected mathematical rereads cover 22 candidates, '
        'while the separate PDF scope review covers all 46 original statements.\n\n'
        'The final report is `reports/FINAL_REPORT.md`; the proof and source '
        'entry point is `reports/REVIEW_GUIDE.md`. The final integrity observation, '
        'actual process receipt, and closeout manifest use `results/final-closeout-` '
        'paths, and `reports/final-closeout-audit.md` records their outcome. '
        'Partial 21.121(b), positive-characteristic 20.89, arbitrary-n 20.100, '
        'and finite-rank 20.124 claims remain explicitly limited. No push or '
        'outside communication was made.\n')
    report_path.write_text(report)
    status_path.write_text(status)
    portfolio_path.write_text(portfolio)

    command = ['python3', 'scripts/audit_final_closeout.py', '--phase', 'final',
               '--output', PREFIX + '-integrity.json']
    script_digest = sha((ROOT / command[1]).read_bytes())
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    with (ROOT / (PREFIX + '.log')).open('wb') as out, (ROOT / (PREFIX + '.stderr')).open('wb') as err:
        process = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
    elapsed = time.monotonic() - tick
    stdout = (ROOT / (PREFIX + '.log')).read_bytes()
    stderr = (ROOT / (PREFIX + '.stderr')).read_bytes()
    accepted = process.returncode == 0 and not stderr and stdout.splitlines().count(b'PASS_FINAL_CLOSEOUT_FINAL') == 1
    receipt = dict(command=command, started_utc=started,
                   finished_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=elapsed,
                   actual_returncode=process.returncode, accepted=accepted,
                   script_sha256=script_digest, stdout_sha256=sha(stdout), stderr_sha256=sha(stderr))
    write_json(PREFIX + '-process.json', receipt)
    print(json.dumps(receipt), flush=True)
    assert accepted, 'Final audit failed; preserve its records and investigate.'
    audit = json.loads((ROOT / (PREFIX + '-integrity.json')).read_text())
    assert audit['status'] == 'PASS' and audit['phase'] == 'final'
    assert not audit['live_mathematical_processes']

    (ROOT / 'reports/final-closeout-audit.md').write_text(
        '# Final closeout audit\n\n'
        'Research ended at 2026-09-12 20:56:46 UTC. The final auditor observed '
        + audit['observed_utc'] + ' and completed at ' + audit['finished_utc'] + '.\n\n'
        'The final phase passed with actual process exit zero, empty stderr, '
        'and its unique completion marker. It checked '
        + str(audit['total_bindings_checked']) + ' hash bindings from the accepted '
        'checkpoint and ' + str(audit['manifest_count']) + ' manifest entry points, '
        + str(audit['unique_files_hashed']) + ' distinct files totaling '
        + str(audit['unique_bytes_hashed']) + ' bytes, and '
        + str(audit['local_link_count']) + ' local links. There were no missing '
        'files, untracked required inputs, or digest mismatches. All 46 candidate '
        'rows agreed with the canonical statement index.\n\n'
        'No recognized mathematical jobs were live outside the auditor process '
        'ancestry. This is a process snapshot. The audit does not rerun mathematical '
        'verifiers, recheck PDF images, supply outside acceptance, or establish '
        'priority. The 1,252 checkpoint observations remain distinguished from '
        'the 2,979 historical manifest bindings.\n\n'
        'The raw records are `results/final-closeout-integrity.json`, '
        '`results/final-closeout.log`, `results/final-closeout.stderr`, and '
        '`results/final-closeout-process.json`. The final manifest binds these '
        'records, final reports, mutable status notes, auditors, and review entry '
        'points. Exact indexed bytes are checked before the local closeout commit. '
        'The launcher output records that commit. Nineteen unrelated untracked '
        'historical files are preserved.\n')
    (ROOT / 'research/completion-audit.md').write_text(
        '# Completion audit against the authorized task\n\n'
        '- **Time:** the requested 48-hour research window ran from '
        '2026-09-10 20:56:46 UTC to 2026-09-12 20:56:46 UTC. Closeout was '
        'observed at ' + stamp + '; artifact hashing and commit are administrative '
        'steps after the research deadline.\n'
        '- **Research deliverables:** the canonical ledger contains 46 complete '
        'solution candidates. The final report and review guide link the proofs, '
        'source audits, and evidence. Selected partial theorems, incomplete '
        'questions, finite exclusions, and prior results are distinguished.\n'
        '- **Rigor:** each candidate has its stated proof and limitations; '
        'all 46 printed statements received a fresh visual scope review, and '
        'selected proof texts for 22 candidates were reread in the final phase. '
        'Independent outside review and priority assessment remain pending. '
        'A finite non-hit is not treated as an unrestricted solution.\n'
        '- **Evidence:** the final artifact audit passed with actual exit zero '
        'and no missing required inputs or hash mismatches. Raw successful and '
        'failed historical runs retain their actual outcomes. The final audit '
        'is not a mathematical verifier replay.\n'
        '- **Resources and jobs:** bounded runners were configured for the '
        'requested 20-CPU and 100-GB working budget. The final process snapshot '
        'observed no recognized mathematical jobs. No continuous global '
        'peak-resource measurement is claimed.\n'
        '- **Documentation and Git:** detailed plans and reports and frequent '
        'local checkpoints are retained. The launcher verifies the exact final '
        'staged path set and bound indexed bytes before its local commit. '
        'Nineteen unrelated historical untracked files are preserved.\n'
        '- **External actions:** no push, submission, email, or other outside '
        'message was made. Documented source browsing and downloads are retained.\n\n'
        'The best-effort, time-bounded research task is ready for completion once '
        'the launcher has returned successfully from its final local commit. '
        'This does not certify 46 accepted or newly established theorems.\n')

    preflight = json.loads((ROOT / 'results/closeout-preflight-packet.json').read_text())
    entry_points = {row['path'] for row in preflight['files'] if row['path'].endswith(('-packet.json', '-summary.json'))}
    bound = set(FINAL_PATHS[:-1]) | entry_points | {
        'scripts/audit_final_closeout.py', 'scripts/closeout_research_window.py',
        'results/closeout-preflight-packet.json',
        'results/closeout-proof-review-addendum-packet.json',
        'results/closeout-construction-review-packet.json',
        'research/complete-candidate-ledger.json', 'reports/REVIEW_GUIDE.md',
        'research/closeout-plan.md', 'research/closeout-proof-review.md',
        'research/closeout-proof-review-addendum.md', 'research/closeout-construction-review.md',
        'reports/closeout-preflight-report.md', 'reports/pdf-statement-review.md',
    }
    rows = []
    for name in sorted(bound):
        data = (ROOT / name).read_bytes()
        rows.append(dict(path=name, bytes=len(data), sha256=sha(data)))
    write_json(PREFIX + '-packet.json', dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        scope='Final reports, deadline artifact audit and actual-process receipt, and frozen review entry points. No outside acceptance or priority certification.',
        candidate_count=46, outside_reviews=0, files=rows))
    git('add', '--', *FINAL_PATHS)
    staged = set(filter(None, git('diff', '--cached', '--name-only', '-z', capture=True).decode().split('\0')))
    assert staged == set(FINAL_PATHS), sorted(staged)
    for row in rows:
        data = git('show', ':' + row['path'], capture=True)
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    authored = [name for name in FINAL_PATHS if not name.endswith(('.log', '.stderr'))]
    git('diff', '--cached', '--check', '--', *authored)
    assert git('ls-files', '--others', '--exclude-standard', '-z', capture=True) == before_untracked
    print(json.dumps(dict(verified_staged_paths=sorted(staged), verified_indexed_bindings=len(rows))), flush=True)
    git('commit', '-m', 'Close the 48-hour research window and archive the final review handoff')
    git('diff', '--quiet')
    git('diff', '--cached', '--quiet')
    assert git('ls-files', '--others', '--exclude-standard', '-z', capture=True) == before_untracked
    print('FINAL_CLOSEOUT_COMMIT ' + git('rev-parse', 'HEAD', capture=True).decode().strip(), flush=True)
    print('PASS_RESEARCH_WINDOW_CLOSEOUT', flush=True)


if __name__ == '__main__':
    main()
