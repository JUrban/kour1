#!/usr/bin/env python3
"""Deterministic archives, each checked against the producer's raw SHA256."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def archive(shard):
    raw = ROOT/f'results/21.99-words-shard{shard}-certificate.jsonl'
    target = raw.with_suffix(raw.suffix+'.gz')
    process = json.loads((ROOT/f'results/21.99-words-shard{shard}-process.json').read_text())
    assert process['actual_returncode'] == 0 and process['sentinel_seen']
    raw_hash = hashlib.sha256(); raw_size = 0
    with raw.open('rb') as source,target.open('wb') as dest:
        with gzip.GzipFile(filename='',mode='wb',compresslevel=6,fileobj=dest,mtime=0) as compressed:
            while chunk := source.read(1<<20):
                raw_hash.update(chunk); raw_size += len(chunk); compressed.write(chunk)
    assert raw_hash.hexdigest() == process['certificate_sha256']
    assert raw_size == process['certificate_bytes']
    check = hashlib.sha256(); check_size = 0
    with gzip.open(target,'rb') as source:
        while chunk := source.read(1<<20):
            check.update(chunk); check_size += len(chunk)
    assert check.digest() == raw_hash.digest() and check_size == raw_size
    return dict(shard=shard,path=str(target.relative_to(ROOT)),bytes=target.stat().st_size,
                sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                raw_sha256=raw_hash.hexdigest(),raw_bytes=raw_size)


def main():
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(archive,range(8)))
    result = dict(status='PASS_LOSSLESS_WORD_ARCHIVES',archives=records)
    (ROOT/'results/21.99-words-archives.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2199_WORD_ARCHIVES files=8 raw_bytes=%d compressed_bytes=%d' %
          (sum(r['raw_bytes'] for r in records),sum(r['bytes'] for r in records)))


if __name__ == '__main__':
    main()
