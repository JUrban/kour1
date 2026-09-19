"""Explicit public correspondence set shared by the build and packager.

New local correspondence is not automatically a publication attachment.
The historical manifest identifies the reports and replies reproduced here.
"""
import json


def public_review_files(paper):
    manifest = paper / 'external-reviews/manifest.json'
    records = json.loads(manifest.read_text())
    names = {'external-reviews/manifest.json', 'external-reviews/review-update1.diff'}
    names.update(row['path'] for row in records['documents'])
    return [paper / name for name in sorted(names)]
