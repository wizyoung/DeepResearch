#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
RAW_PDFS_DIR = ROOT / "raw_pdfs"
PAPERS_JSON = ROOT / "papers.json"


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def extract_papers_from_readme(readme_text: str):
    section_pattern = re.compile(r"##\s*Deep Research Agent Family[\s\S]*?##\s", re.M)
    section_match = section_pattern.search(readme_text + "\n## ")
    section_text = readme_text if not section_match else section_match.group(0)

    line_pattern = re.compile(r"\[(\d+)\]\s*\[(.*?)\]\((https?://[^)]+)\)")
    entries = []
    for m in line_pattern.finditer(section_text):
        idx = int(m.group(1))
        title = m.group(2).strip()
        url = m.group(3).strip()
        entries.append({"index": idx, "title": title, "url": url})
    entries.sort(key=lambda x: x["index"])  # ensure order 1..11
    return entries


def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_text = f.read()

    papers = extract_papers_from_readme(readme_text)
    if not papers:
        raise RuntimeError("Failed to extract papers from README.md")

    RAW_PDFS_DIR.mkdir(parents=True, exist_ok=True)
    for p in papers:
        p["safe_title"] = sanitize_filename(p["title"])  # add for file naming
        p["pdf_path"] = str(RAW_PDFS_DIR / f"{p['safe_title']}.pdf")

    with open(PAPERS_JSON, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    # Use curl to download each PDF (follow redirects)
    # We do not download here to keep this script idempotent for parsing only
    print(json.dumps({"status": "ok", "papers": papers}, ensure_ascii=False))


if __name__ == "__main__":
    main()

