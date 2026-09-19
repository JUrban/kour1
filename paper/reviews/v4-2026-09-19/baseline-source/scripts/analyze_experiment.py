#!/usr/bin/env python3
"""Derive paper measurements from the supplied export and frozen Git history.

This analyzes retained artifacts, not the unexported underlying session.
No network access or mathematical verifier execution is performed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
from html import unescape
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FROZEN = 'cff2c37b9bf6b737e8ad5f7ead12291a551b5201'
START = datetime(2026, 9, 10, 20, 56, 46, tzinfo=timezone.utc)
END = datetime(2026, 9, 12, 20, 56, 46, tzinfo=timezone.utc)
TOKEN_LABELS = ['Total tokens', 'Input', 'Cached input', 'Cache write input',
                'Output', 'Reasoning output']


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)


class SessionParser(HTMLParser):
    """Parse actual exported event elements and their labeled token sections."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.event = None
        self.li_depth = 0
        self.capture = None
        self.capture_text = []
        self.section = None
        self.term = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'li':
            if self.event is None and attrs.get('class', '').startswith('trace-event '):
                self.event = dict(kind=attrs['class'].split()[1], text_parts=[], usage={})
                self.li_depth = 1
            elif self.event is not None:
                self.li_depth += 1
        if self.event is None:
            return
        if tag in ('p', 'pre', 'h4', 'dt', 'dd', 'section', 'br'):
            self.event['text_parts'].append('\n')
        if tag == 'p' and attrs.get('class') == 'event-label':
            self.capture = 'label'
            self.capture_text = []
        if tag == 'section' and attrs.get('aria-label') in ('Total token usage', 'Last token usage'):
            self.section = attrs['aria-label'].split()[0].lower()
            self.event['usage'][self.section] = {}
        if self.section and tag in ('dt', 'dd'):
            self.capture = tag
            self.capture_text = []

    def handle_data(self, data):
        if self.event is not None:
            self.event['text_parts'].append(data)
            if self.capture:
                self.capture_text.append(data)

    def handle_endtag(self, tag):
        if self.event is None:
            return
        if tag == 'p' and self.capture == 'label':
            label = ''.join(self.capture_text).strip()
            match = re.fullmatch(r'(.+) · (\d+)', label)
            assert match, label
            self.event['label'] = match[1]
            self.event['event_id'] = int(match[2])
            self.capture = None
        if tag == 'dt' and self.capture == 'dt':
            self.term = ''.join(self.capture_text).strip()
            self.capture = None
        if tag == 'dd' and self.capture == 'dd':
            value = ''.join(self.capture_text).strip()
            assert self.term in TOKEN_LABELS and re.fullmatch(r'[\d,]+', value), (self.term, value)
            self.event['usage'][self.section][self.term] = int(value.replace(',', ''))
            self.capture = None
        if tag == 'section':
            self.section = None
        if tag == 'li':
            self.li_depth -= 1
            if self.li_depth == 0:
                self.event['text'] = ''.join(self.event.pop('text_parts')).strip()
                assert 'event_id' in self.event
                self.events.append(self.event)
                self.event = None
                self.capture = self.section = None


def json_text(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def csv_text(fieldnames, rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def analyze():
    html_path = ROOT / 'session/session.html'
    txt_path = ROOT / 'session/session.txt'
    raw = html_path.read_bytes()
    html = raw.decode()
    txt = txt_path.read_text()
    parser = SessionParser()
    parser.feed(html)
    parser.close()
    assert parser.event is None
    events = parser.events
    ids = [e['event_id'] for e in events]
    assert ids == sorted(set(ids)), 'Exported event IDs must be strictly increasing.'
    kinds = Counter(e['kind'] for e in events)

    # Independent extraction from literal tags checks the structural parser.
    regex_kinds = Counter(re.findall(r'<li class="trace-event ([^" ]+)"', html))
    assert kinds == regex_kinds
    advertised = re.search(r'<p class="session-meta">([^<]+) · (\d+) events</p>', html)
    assert advertised
    origin = re.search(r'<p class="session-origin">([^<]+)</p>', html)
    assert origin
    text_roles = Counter(re.findall(r'^(Assistant commentary|Assistant final|User) · \d+$', txt, re.M))
    assert text_roles == Counter({'Assistant commentary': kinds['assistant'],
                                  'Assistant final': kinds['final'], 'User': kinds['human']})

    tokens = [e for e in events if e['kind'] == 'token']
    previous = dict.fromkeys(TOKEN_LABELS, 0)
    duplicate_cumulative = 0
    unitemized_last_records = []
    token_rows = []
    for e in tokens:
        assert set(e['usage']) == {'total', 'last'}
        total, last = e['usage']['total'], e['usage']['last']
        for row in (total, last):
            assert set(row) == set(TOKEN_LABELS)
            assert row['Cached input'] <= row['Input']
            assert row['Reasoning output'] <= row['Output']
        assert total['Total tokens'] == total['Input'] + total['Output']
        if last['Total tokens'] != last['Input'] + last['Output']:
            assert last['Total tokens'] > 0 and all(last[k] == 0 for k in TOKEN_LABELS[1:]), (e['event_id'], last)
            unitemized_last_records.append(dict(event_id=e['event_id'], reported_last=last))
        assert all(total[k] >= previous[k] for k in TOKEN_LABELS), ('counter reset', e['event_id'])
        duplicate_cumulative += total == previous
        row = {'event_id': e['event_id']}
        for label in TOKEN_LABELS:
            key = label.lower().replace(' ', '_')
            row['cumulative_' + key] = total[label]
            row['reported_last_' + key] = last[label]
            row['observed_delta_' + key] = total[label] - previous[label]
        token_rows.append(row)
        previous = total

    # A second, tag-local parse checks the last cumulative token numbers.
    total_sections = re.findall(r'<section aria-label="Total token usage">(.*?)</section>', html, re.S)
    assert len(total_sections) == len(tokens)
    last_pairs = re.findall(r'<dt>([^<]+)</dt><dd>([\d,]+)</dd>', total_sections[-1])
    assert {unescape(k): int(v.replace(',', '')) for k, v in last_pairs} == previous

    end_usage = tokens[-1]['usage']['total']
    begin_usage = tokens[0]['usage']['total']
    directives = [e for e in events if e['kind'] == 'directive']
    goal_directives = [e for e in directives if '<codex_internal_context source="goal">' in e['text']]
    commits = []
    for line in git('log', '--reverse', '--format=%H%x09%cI%x09%aI%x09%s', FROZEN).splitlines():
        commit, committed, authored, subject = line.split('\t', 3)
        when = datetime.fromisoformat(committed)
        commits.append(dict(commit=commit, committed_utc=when.astimezone(timezone.utc).isoformat(),
                            author_date=authored, elapsed_hours=(when-START).total_seconds()/3600,
                            in_research_window=START <= when <= END, subject=subject))
    assert commits[-1]['commit'] == FROZEN
    files_by_dir = defaultdict(lambda: dict(files=0, bytes=0))
    tree_files = {}
    for line in git('ls-tree', '-r', '-l', '--full-tree', FROZEN).splitlines():
        meta, name = line.split('\t', 1)
        mode, kind, object_id, size = meta.split()
        assert kind == 'blob'
        size = int(size)
        tree_files[name] = dict(bytes=size, git_blob=object_id)
        directory = name.split('/')[0] if '/' in name else '[root]'
        files_by_dir[directory]['files'] += 1
        files_by_dir[directory]['bytes'] += size

    additions = {}
    current_commit = None
    for line in git('log', '--reverse', '--diff-filter=A', '--format=COMMIT %H', '--name-status', FROZEN).splitlines():
        if line.startswith('COMMIT '):
            current_commit = line[7:]
        elif line.startswith('A\t'):
            additions.setdefault(line[2:], current_commit)
    commit_info = {r['commit']: r for r in commits}
    ledger = json.loads(git('show', FROZEN + ':research/complete-candidate-ledger.json'))
    births = []
    for item in ledger['candidates']:
        choices = [(commit_info[additions[p]]['committed_utc'], p, additions[p]) for p in item['principal_proofs']]
        when, path, commit = min(choices)
        births.append(dict(problem=item['problem'], covered_subparts=item['covered_subparts'],
                           first_principal_file=path, commit=commit, committed_utc=when,
                           elapsed_hours=commit_info[commit]['elapsed_hours']))
    births.sort(key=lambda r:(r['committed_utc'], r['problem']))
    for i, row in enumerate(births, 1):
        row['cumulative_final_problem_families_with_proof_artifact'] = i

    metrics = dict(
        schema_version=1,
        frozen_research_commit=FROZEN,
        window=dict(start_utc=START.isoformat(), end_utc=END.isoformat(), wall_seconds=int((END-START).total_seconds())),
        sources=[dict(path=str(p.relative_to(ROOT)), bytes=p.stat().st_size, sha256=digest(p.read_bytes()))
                 for p in (html_path, txt_path)],
        export=dict(software_label=unescape(origin[1]), advertised_event_count=int(advertised[2]),
                    displayed_session_metadata=unescape(advertised[1]),
                    exported_event_elements=len(events), exported_event_kinds=dict(sorted(kinds.items())),
                    first_exported_event_id=ids[0], last_exported_event_id=ids[-1],
                    visible_goal_directives=len(goal_directives),
                    text_export_message_kinds=dict(sorted(text_roles.items())),
                    token_event_count=len(tokens), identical_successive_cumulative_snapshots=duplicate_cumulative,
                    unitemized_last_record_count=len(unitemized_last_records),
                    unitemized_last_records=unitemized_last_records,
                    cumulative_counters_monotone=True, first_token_event_id=tokens[0]['event_id'],
                    final_token_event_id=tokens[-1]['event_id'], first_cumulative_tokens=begin_usage,
                    final_cumulative_tokens=end_usage,
                    derived_uncached_input=end_usage['Input']-end_usage['Cached input'],
                    derived_uncached_input_plus_output=end_usage['Input']-end_usage['Cached input']+end_usage['Output'],
                    cache_fraction_of_input=end_usage['Cached input']/end_usage['Input']),
        git=dict(commits_through_closeout=len(commits),
                 commits_in_research_window=sum(r['in_research_window'] for r in commits),
                 commits_before_window=sum(datetime.fromisoformat(r['committed_utc'])<START for r in commits),
                 commits_after_window=sum(datetime.fromisoformat(r['committed_utc'])>END for r in commits),
                 first_commit=commits[0], last_commit=commits[-1],
                 tracked_files=len(tree_files), tracked_logical_bytes=sum(r['bytes'] for r in tree_files.values()),
                 tracked_by_directory=dict(sorted(files_by_dir.items()))),
        deadline_candidates=dict(count=ledger['candidate_count'], outside_reviews=sum(r['outside_reviews'] for r in ledger['candidates'])),
        limitations=[
            'The supplied HTML is a rendered subset, not the raw session event stream.',
            'No tool or internal-analysis event bodies are exported; their counts cannot be recovered from this file.',
            'The single exported human message is not a census of all human instructions: the initial objective is retained in a directive.',
            'Event IDs order retained observations but do not provide per-event wall-clock timestamps.',
            'Cumulative input includes cached input; reasoning output is a subcounter of output. Neither is added a second time.',
            'Token counts are reported by the session renderer, not independently reconciled with provider invoices.',
            'Identical token snapshots are retained in the data but are not summed as additional usage.',
            'Some Last records give a positive total with zero components; these are retained as unitemized records, not attributed to a request type or added to cumulative usage.',
            'The export alone does not identify the historical model ID or reasoning-effort setting.',
            'Git timestamps date commits, not the moments when a proof was conceived or independently accepted.',
            'A first proof-file appearance is not a certification date or necessarily the date when full final scope was reached.',
            'Logical tracked-file bytes are not repository pack size or physical disk usage.',
        ])
    message_rows = []
    for e in events:
        if e['kind'] in ('assistant', 'final', 'human'):
            message_rows.append(dict(event_id=e['event_id'], kind=e['kind'], text=e['text']))
    outputs = {
        'paper/data/experiment-metrics.json': json_text(metrics),
        'paper/data/session-tokens.csv': csv_text(list(token_rows[0]), token_rows),
        'paper/data/research-commits.csv': csv_text(list(commits[0]), commits),
        'paper/data/proof-artifact-timeline.csv': csv_text(list(births[0]), births),
        'paper/data/session-visible-messages.jsonl': ''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in message_rows),
    }
    return outputs, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare with generated files without modifying them.')
    args = parser.parse_args()
    outputs, metrics = analyze()
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.read_text() == content, name
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print(json.dumps(dict(status='PASS', mode='check' if args.check else 'generate',
                          exported_events=metrics['export']['exported_event_elements'],
                          token_snapshots=metrics['export']['token_event_count'],
                          final_cumulative_tokens=metrics['export']['final_cumulative_tokens'],
                          commits=metrics['git']['commits_through_closeout'],
                          commits_in_window=metrics['git']['commits_in_research_window'],
                          files_generated=len(outputs))))


if __name__ == '__main__':
    main()
