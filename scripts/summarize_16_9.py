#!/usr/bin/env python3
"""Audit coverage and bind the completed 16.9 control artifacts."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
py = json.loads((root/'results/16.9-python-summary.json').read_text())
log = (root/'results/16.9-python.log').read_text()
assert py == json.loads(log[log.index('{'):])
assert py['status'] == 'PASS'
assert [py[k] for k in ('brute_deletion_words', 'exhaustive_free_words',
                        'frid_two_factor_checks', 'special_cases',
                        'random_long_cases', 'gap_witness_cases')] == [
                            9841, 36558, 36558, 40, 100, 36698]
assert log.count('PASS_DELETION_ENUMERATION words=9841') == 1
assert log.count('PASS_FREE_WORDS cases=36558') == 1
gap = (root/'results/16.9-gap.log').read_text().strip()
assert gap == ('PASS_FREE_GROUP_WITNESSES cases=36698 '
               'palindrome_letters=310658 rank=22 parity_lower_bounds=36698')

literal = (root/'results/16.9-witnesses.g').read_text()
assert literal.startswith('PalindromicCases:=') and literal.endswith(';\n')
cases = json.loads(literal[len('PalindromicCases:='):-2])
assert len(cases) == 36698
assert sum(len(p) for _, factors, _ in cases for p in factors) == 310658
assert all(len(factors) == length for _, factors, length in cases)

# Distinct valid inputs plus the theoretical count for each length prove
# exact coverage without copying the generator's ordering or recurrence.
offset, distributions = 0, {}
for rank, maximum, total in [(2, 8, 13121), (3, 6, 23437)]:
    family = cases[offset:offset+total]
    words = [tuple(row[0]) for row in family]
    assert len(set(words)) == total
    assert all(all(1 <= abs(a) <= rank for a in w) and
               all(w[i] != -w[i-1] for i in range(1, len(w))) for w in words)
    expected = {0: 1, **{n: 2*rank*(2*rank-1)**(n-1)
                         for n in range(1, maximum+1)}}
    assert dict(Counter(map(len, words))) == expected
    distributions.update({str((rank, length)): count
                          for length, count in Counter(row[2] for row in family).items()})
    offset += total
assert distributions == py['distributions']

files = ['research/16.9-proof.md', 'research/16.9-review.md',
         'scripts/palindromic_length.py', 'scripts/verify_16_9.py',
         'scripts/verify_16_9.g', 'scripts/summarize_16_9.py',
         'results/16.9-python-summary.json', 'results/16.9-python.log',
         'results/16.9-witnesses.g', 'results/16.9-gap.log',
         'references/cache/frid-small-palindromic-2025.pdf',
         'references/cache/lotz-reflection-length-2024.pdf', 'docs/21tkt.pdf']
report = dict(status='PASS', observed_utc=datetime.now(timezone.utc).isoformat(),
              problem='16.9', conclusion='Complete candidate affirmative algorithm',
              word_operations='O(L^3)', stored_integers='O(L^2)',
              python=py, gap=dict(cases=36698, palindrome_letters=310658,
                                  ambient_rank=22, parity_lower_bounds=36698),
              exact_input_coverage=True,
              process_evidence='Python and GAP actual exit statuses zero were observed through the execution tool. This report separately checks retained completion markers and exhaustive input coverage.',
              scope='The self-contained proof supplies arbitrary-input minimality. GAP checks witnesses and parity lower bounds, not independent minimum length in every case. Outside review and further priority checks pending.',
              sha256={p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files})
(root/'results/16.9-summary.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
