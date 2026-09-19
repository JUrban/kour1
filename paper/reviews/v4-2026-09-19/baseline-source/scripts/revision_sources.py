"""Bind historical checks to preserved sources and declared later corrections."""
import hashlib
import json


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def v2_source(paper, relative):
    revision = paper / 'reviews/v3-2026-09-19'
    if not (revision / 'baseline.json').exists():
        return (paper / relative).read_bytes()
    baseline = json.loads((revision / 'baseline.json').read_text())
    bindings = {row['path']: row['sha256'] for row in baseline['sources']}
    raw = (revision / 'baseline-source' / relative).read_bytes()
    assert digest(raw) == bindings[relative], ('changed v2 baseline', relative)
    return raw


def preserved_mathematical_source(paper, relative):
    """Return the old source only for a hash-bound, explicitly recorded change."""
    raw = (paper / relative).read_bytes()
    record = paper / 'reviews/v3-2026-09-19/source-change.json'
    if record.exists():
        correction = json.loads(record.read_text())
        if relative == correction['path']:
            assert digest(raw) == correction['after_sha256'], relative
            old = v2_source(paper, relative)
            assert digest(old) == correction['before_sha256'], relative
            return old
    return raw
