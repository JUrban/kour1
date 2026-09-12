#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
from pathlib import Path


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def run():
    root = Path.cwd()
    packet = json.loads(Path('results/21.76-packet.json').read_text())
    for path, expected in packet['sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
    for name in ['prepare', 'gap', 'controls', 'degrees']:
        record = json.loads(Path('results/21.76-'+name+'-process.json').read_text())
        assert record['returncode'] == 0 and record['stderr'] == '' and record['sentinel_present']
        assert record['script_sha256'] == packet['sha256'][record['command'][-1]]
        log = Path('results/21.76-'+name+'.log')
        assert record['stdout'] == log.read_text()
        assert record['log_sha256'] == packet['sha256'][str(log)]
        assert not re.search(r'Error|Syntax warning|Traceback', log.read_text())
    rejected = json.loads(Path('results/21.76-warning-run/21.76-gap-process.json').read_text())
    assert rejected['returncode'] == 0 and rejected['stderr'].count('Syntax warning:') == 2
    assert rejected['script_sha256'] == packet['sha256']['results/21.76-warning-run/check_21_76.g']
    certificate = json.loads(Path('results/21.76-certificate.json').read_text())
    assert certificate['pilot'] == json.loads(Path('results/21.76-initial-f9-pilot.json').read_text())
    matrices = json.loads(Path('results/21.76-gap-matrices.json').read_text())
    assert matrices == sorted(row['matrix'] for row in certificate['elements'])
    with tempfile.TemporaryDirectory(prefix='2176-audit-') as temp:
        temp = Path(temp)
        (temp/'results').mkdir()
        p = subprocess.run(['python3', str(root/'scripts/prepare_21_76.py'), '--output',
                            str(temp/'certificate.json'), '--table', str(temp/'table.md')],
                           capture_output=True, text=True)
        assert p.returncode == 0 and p.stderr == '' and 'PASS_2176_PREPARATION' in p.stdout
        assert (temp/'certificate.json').read_bytes() == Path('results/21.76-certificate.json').read_bytes()
        assert (temp/'table.md').read_bytes() == Path('research/21.76-finite-table.md').read_bytes()
        p = subprocess.run([str(root/'bin/gap'), '-o', '512m', str(root/'scripts/check_21_76.g')],
                           cwd=temp, capture_output=True, text=True)
        assert p.returncode == 0 and p.stderr == '' and 'PASS_2176_GAP' in p.stdout
        assert not re.search(r'Error|Syntax warning', p.stdout)
        assert json.loads((temp/'results/21.76-gap-matrices.json').read_text()) == matrices
        rows = re.findall(r'BETA (\d+) ORDER (\d+) UPPER\s*(\[[^]]*\]) LOWER\s*(\[[^]]*\])', p.stdout)
        observed = [dict(beta=int(b), order=int(o), upper=json.loads(u), lower=json.loads(l)) for b,o,u,l in rows]
        assert observed == certificate['pilot']
    finite = module('finite2176', 'scripts/check_21_76.py').run()
    assert finite == json.loads(Path('results/21.76-controls.json').read_text())
    degrees = module('degrees2176', 'scripts/check_21_76_degrees.py').run()
    assert degrees == json.loads(Path('results/21.76-degree-controls.json').read_text())
    assert finite['elements'] == 120 and finite['products'] == 14400
    assert degrees['word_cases'] == 36432
    print('PASS_2176_PACKET', len(packet['sha256']), 'elements=120 products=14400 polynomial_words=36432')


if __name__ == '__main__':
    run()
