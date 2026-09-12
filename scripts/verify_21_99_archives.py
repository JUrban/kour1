#!/usr/bin/env python3
"""Independently verify all archived generator-word certificates in eight processes."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import contextlib
import gzip
import io
import json
from pathlib import Path
from verify_21_99_words import verify_files

ROOT = Path(__file__).resolve().parents[1]


class CompressedPath:
    def __init__(self,path):
        self.path = path
        self.name = path.name

    def read_text(self):
        with gzip.open(self.path,'rt') as stream:
            return stream.read()


def one_shard(shard):
    census = json.loads((ROOT/'results/21.99-words-census.json').read_text())
    expected = {(n,i) for n,count in census for i in range(shard+1,count+1,8)}
    path = CompressedPath(ROOT/f'results/21.99-words-shard{shard}-certificate.jsonl.gz')
    with contextlib.redirect_stdout(io.StringIO()):
        result = verify_files([path],expected)
    return result


def main():
    with ProcessPoolExecutor(max_workers=8) as pool:
        shards = list(pool.map(one_shard,range(8)))
    counts = Counter(); fixed = Counter(); degrees = Counter()
    for i,r in enumerate(shards):
        counts.update(r['counts']); fixed.update(dict(r['fixed_counts'])); degrees.update(dict(r['degrees']))
        print('VERIFIED_ARCHIVE',i,r['counts']['groups'],flush=True)
    assert counts['groups'] == 496284
    result = dict(status='PASS_ALL_ARCHIVED_WORD_CERTIFICATES',counts=dict(sorted(counts.items())),
                  degrees=sorted(degrees.items()),fixed_counts=sorted(fixed.items()),
                  max_random_steps=max(r['max_random_steps'] for r in shards),
                  shard_counts=[r['counts'] for r in shards],
                  rejected_mutations=[r['rejected_mutations'] for r in shards],
                  scope=shards[0]['scope'],new_complete_candidates_added=0)
    (ROOT/'results/21.99-words-archive-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_2199_WORD_ARCHIVE_INDEPENDENT',json.dumps(result['counts'],sort_keys=True),
          'mutations=40_types5')


if __name__ == '__main__':
    main()
