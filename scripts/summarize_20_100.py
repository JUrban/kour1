#!/usr/bin/env python3
"""Validate completed certificate counts and identify live jobs by command+stdout."""
from datetime import datetime, timezone
from pathlib import Path
import gzip
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]


def live_job(argument, logfile):
    matches = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            command = (entry/'cmdline').read_bytes().split(b'\0')
            if argument.encode() not in command:
                continue
            if not str((entry/'fd/1').resolve()) == str(logfile.resolve()):
                continue
            matches.append(int(entry.name))
        except (OSError, FileNotFoundError, PermissionError):
            pass
    return matches


results = []
for n in [4, 5, 6, 7]:
    generator_path = root/f'results/20.100-n{n}-generator.log'
    verifier_path = root/f'results/20.100-n{n}-verifier.log'
    certificate = root/f'results/20.100-n{n}-certificate.g.gz'
    generated = []
    for line in generator_path.read_text().splitlines():
        try:
            generated.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    completed = next((row for row in reversed(generated)
                      if row.get('status') == 'CERTIFICATE_COMPLETE_PENDING_VERIFICATION'), None)
    item = {'n': n}
    if completed:
        assert completed['n'] == n and completed['prime_bound'] == n+1
        assert hashlib.sha256(certificate.read_bytes()).hexdigest() == completed['compressed_sha256']
        count, digest, final = 0, hashlib.sha256(), b''
        with gzip.open(certificate, 'rb') as stream:
            for line in stream:
                digest.update(line)
                count += line.startswith(b'CheckNode(')
                final = line
        assert count == completed['states']
        assert final == f'FinishProof({count});\n'.encode()
        item.update({key: completed[key] for key in ['states', 'leaves', 'edges']})
        item['uncompressed_sha256'] = digest.hexdigest()
        log = verifier_path.read_text() if verifier_path.exists() else ''
        assert 'Error,' not in log and 'Assertion failure' not in log
        match = re.search(r'PASS n=(\d+) nodes=(\d+) leaves=(\d+) edges=(\d+) relation_implications=\s*(\d+)', log)
        if match:
            assert list(map(int, match.groups()[:4])) == [n, count, completed['leaves'], completed['edges']]
            item['relation_implications'] = int(match.group(5))
            item['status'] = 'VERIFIED'
        else:
            pids = live_job(f'results/20.100-n{n}-certificate.g.gz', verifier_path)
            assert pids, f'n={n}: verification has neither completion evidence nor a verified live process'
            item.update(status='VERIFYING', verified_live_pids=pids)
    else:
        pids = live_job(f'results/20.100-n{n}-certificate.g.gz', generator_path)
        assert pids, f'n={n}: generation has neither completion evidence nor a verified live process'
        item.update(status='GENERATING', verified_live_pids=pids)
        if generated:
            item['last_progress'] = generated[-1]
    results.append(item)

summary = {'observed_utc': datetime.now(timezone.utc).isoformat(), 'results': results,
           'all_log_checks_pass': True}
(root/'results/20.100-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
