#!/usr/bin/env python3
"""Bind the elementary 11.115 proof and replay its independent word controls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULI = [2, 3, 4, 5, 7, 8, 11]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process(name, command, sentinel):
    stem = ROOT / ('results/11.115-' + name)
    receipt = json.loads(Path(str(stem) + '-process.json').read_text())
    out, err = Path(str(stem) + '.log'), Path(str(stem) + '.stderr')
    assert receipt['command'] == command
    assert receipt['actual_returncode'] == 0 and receipt['sentinel_seen'] is True
    assert sha(out) == receipt['stdout_sha256']
    assert sha(err) == receipt['stderr_sha256'] and not err.read_bytes()
    assert out.read_text().count(sentinel) == 1
    return out.read_text()


def summarize():
    native = process('native', ['bin/gap', '-o', '2g', 'scripts/verify_11_115_native.g'],
                     'PASS_11_115_NATIVE models=7')
    match = re.fullmatch(r'\s*NATIVE_11115_ROWS\s*(\[.*\])\s*'
                         r'PASS_11_115_NATIVE models=7\s*', native, flags=re.S)
    assert match is not None
    rows = json.loads(match[1])
    assert rows == [[m, m, m + 1, 5*m + 4] for m in MODULI]
    independent = process('independent', ['python3', 'scripts/verify_11_115_words.py'],
                          'PASS_11_115_WORDS models=7 rejected_corruptions=5')
    lines = independent.splitlines()
    assert len(lines) == 2
    assert lines[1] == 'PASS_11_115_WORDS models=7 rejected_corruptions=5'
    summary = json.loads((ROOT / 'results/11.115-words-summary.json').read_text())
    assert json.loads(lines[0]) == summary
    assert summary['status'] == 'PASS' and summary['moduli'] == MODULI
    assert summary['stats'] == dict(exhaustive_words=91847, long_words=7000,
                                    normal_form_products=7000, associativity_triples=7000)
    assert summary['rejected_corruptions'] == [
        'wrong_basis_power', 'omitted_wrap_conjugation', 'wrong_inverse',
        'wrong_index', 'wrong_rank']
    statement = json.loads((ROOT / 'results/11.115-statement.json').read_text())
    assert statement['id'] == '11.115' and statement['pdf_page'] == 56
    assert not statement['starred_heading'] and not statement['contains_editorial_star']
    assert 'if N is not maximal in X?' in statement['text']
    return dict(native_rows=rows, native_word_identities=sum(r[3] for r in rows),
                independent=summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--summary-only', action='store_true')
    args = parser.parse_args()
    summary = summarize()
    if args.summary_only:
        print(json.dumps(summary, indent=2))
        return
    packet = json.loads((ROOT / 'results/11.115-packet.json').read_text())
    assert packet['new_complete_candidates_added'] == 1
    assert packet['outside_reviews'] == 0 and packet['priority_established'] is False
    assert packet['summary'] == summary

    def bindings():
        assert len({row['path'] for row in packet['files']}) == len(packet['files'])
        for row in packet['files']:
            path = ROOT / row['path']
            assert path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], path

    bindings()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='11.115-replay-') as directory:
            temporary = Path(directory)
            (temporary / 'results').mkdir()
            p = subprocess.run([str(ROOT / 'bin/gap'), '-o', '2g',
                                str(ROOT / 'scripts/verify_11_115_native.g')],
                               cwd=temporary, capture_output=True, timeout=60)
            assert p.returncode == 0 and not p.stderr
            assert p.stdout == (ROOT / 'results/11.115-native.log').read_bytes()
            for m in MODULI:
                name = f'results/11.115-model-{m}.json'
                assert (temporary / name).read_bytes() == (ROOT / name).read_bytes()
        p = subprocess.run(['python3', str(ROOT / 'scripts/verify_11_115_words.py')],
                           cwd=ROOT, capture_output=True, timeout=60)
        assert p.returncode == 0 and not p.stderr
        assert p.stdout == (ROOT / 'results/11.115-independent.log').read_bytes()
        bindings()
    print(json.dumps(dict(status='PASS', files=len(packet['files']), replay=args.replay,
                          summary=summary), sort_keys=True))
    print('PASS_11_115_PACKET')


if __name__ == '__main__':
    main()
