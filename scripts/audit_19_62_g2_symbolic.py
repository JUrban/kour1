#!/usr/bin/env python3
"""Replay the complete G2 integer certificate and its polynomial constants."""
import hashlib
import json
from pathlib import Path
import check_19_62_g2_integer_constants as constants
import verify_19_62_monomial_certificates as certificates


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    packet=json.loads(Path('results/19.62-g2-symbolic-packet.json').read_text())
    for p,h in packet['sha256'].items():assert sha(p)==h,p
    previous=json.loads(Path('results/19.61-g2-summary.json').read_text())
    for p,h in previous['sha256'].items():assert sha(p)==h,p
    assert constants.run()==json.loads(Path('results/19.62-g2-integer-constants.json').read_text())
    assert certificates.run()==json.loads(Path('results/19.62-g2-monomial-verification.json').read_text())
    observations=json.loads(Path('results/19.62-g2-symbolic-observations.json').read_text())
    assert all(p['exit_code']==0 and p['tool_chunk'] for p in observations['successful_processes'])
    assert observations['compilation_failure']['exit_code']==1
    print('PASS_1962_G2_SYMBOLIC_PACKET',len(packet['sha256']),'targets=2712 nodes=62835',flush=True)


if __name__=='__main__':run()
