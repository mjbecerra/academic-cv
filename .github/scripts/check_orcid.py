#!/usr/bin/env python3
"""
Fetch works from ORCID public API and generate Hugo markdown stubs
for any publications not yet present in content/publications/.

Usage: python check_orcid.py
Prints a JSON summary to stdout; new files are written to disk.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

import requests

ORCID_ID = "0000-0001-6675-7370"
PUBLICATIONS_DIR = Path("content/publications")
ORCID_API = "https://pub.orcid.org/v3.0"

ORCID_TYPE_MAP = {
    "journal-article": "article-journal",
    "book-chapter": "chapter",
    "book": "book",
    "conference-paper": "paper-conference",
    "report": "report",
    "dataset": "dataset",
    "dissertation": "thesis",
}


def normalize_doi(raw: str) -> str:
    doi = raw.strip().strip("\"'")
    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
    ):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
    return doi.lower()


def get_existing_dois() -> set:
    dois = set()
    for md_file in PUBLICATIONS_DIR.rglob("index.md"):
        content = md_file.read_text(encoding="utf-8")
        for m in re.finditer(r'doi:\s*["\']?([^\s"\'>\n]+)["\']?', content, re.IGNORECASE):
            doi = normalize_doi(m.group(1))
            if doi:
                dois.add(doi)
    return dois


def get_orcid_works() -> list:
    url = f"{ORCID_API}/{ORCID_ID}/works"
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    works = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]  # first = preferred source

        doi = None
        for ext_id in summary.get("external-ids", {}).get("external-id", []):
            if ext_id.get("external-id-type") == "doi":
                doi = normalize_doi(ext_id.get("external-id-value", ""))
                break

        pub_date = summary.get("publication-date") or {}
        year = (pub_date.get("year") or {}).get("value", "")
        month = (pub_date.get("month") or {}).get("value", "01") or "01"
        month = str(month).zfill(2)

        journal = (summary.get("journal-title") or {}).get("value", "") or ""
        title = (
            (summary.get("title") or {}).get("title") or {}
        ).get("value", "Unknown Title") or "Unknown Title"

        works.append(
            {
                "put_code": summary.get("put-code"),
                "title": title,
                "type": summary.get("type", "journal-article"),
                "doi": doi,
                "year": year,
                "month": month,
                "journal": journal,
            }
        )
    return works


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")[:55]


def make_hugo_stub(work: dict) -> str:
    title = work["title"].replace('"', '\\"')
    doi = work["doi"] or ""
    year = work["year"] or "2024"
    month = work["month"] or "01"
    journal = (work["journal"] or "").replace('"', '\\"')
    pub_type = ORCID_TYPE_MAP.get(work["type"], "article-journal")
    date_str = f"{year}-{month}-01T00:00:00Z"

    doi_block = (
        f"\nhugoblox:\n  ids:\n    doi: \"{doi}\"\n" if doi else ""
    )
    links_block = (
        f"\nlinks:\n  - type: pdf\n    url: \"https://doi.org/{doi}\"\n"
        if doi
        else "\nlinks: []\n"
    )

    return (
        f'---\n'
        f'title: "{title}"\n'
        f'authors:\n  - me\n'
        f'date: "{date_str}"\n'
        f'publishDate: "{date_str}"\n\n'
        f'publication_types: ["{pub_type}"]\n\n'
        f'publication:\n  name: "{journal}"\n'
        f'{doi_block}\n'
        f'peer_reviewed: true\n'
        f'open_access: false\n\n'
        f'abstract: ""\n\n'
        f'tags: []\n\n'
        f'featured: false\n'
        f'{links_block}\n'
        f'projects: []\n'
        f'slides: ""\n'
        f'---\n'
    )


def main() -> int:
    existing_dois = get_existing_dois()
    print(f"Existing DOIs in repo: {len(existing_dois)}", file=sys.stderr)

    works = get_orcid_works()
    print(f"Works on ORCID: {len(works)}", file=sys.stderr)

    new_works = []
    for work in works:
        doi = work["doi"]
        if not doi:
            print(f"  Skip (no DOI): {work['title'][:70]}", file=sys.stderr)
            continue
        if doi in existing_dois:
            continue
        new_works.append(work)

    print(f"New publications to add: {len(new_works)}", file=sys.stderr)

    created = []
    for work in new_works:
        year = work["year"] or "unknown"
        slug = f"{slugify(work['title'])}-{year}"
        dest = PUBLICATIONS_DIR / slug / "index.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(make_hugo_stub(work), encoding="utf-8")
        created.append(str(dest))
        print(f"  Created: {dest}", file=sys.stderr)

    result = {
        "new_count": len(new_works),
        "total_orcid": len(works),
        "created_files": created,
        "new_works": [
            {
                "title": w["title"],
                "doi": w["doi"],
                "year": w["year"],
                "journal": w["journal"],
            }
            for w in new_works
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
