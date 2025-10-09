#!/usr/bin/env python3
import os
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PDFS_DIR = ROOT / "raw_pdfs"
PAPERS_JSON = ROOT / "papers.json"


def robust_download(url: str, dest: Path):
    dest_tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "5",
        "--retry-delay",
        "2",
        "--connect-timeout",
        "15",
        "--max-time",
        "600",
        "-o",
        str(dest_tmp),
        url,
    ]
    subprocess.run(cmd, check=True)
    dest_tmp.replace(dest)


def main():
    with open(PAPERS_JSON, "r", encoding="utf-8") as f:
        papers = json.load(f)

    RAW_PDFS_DIR.mkdir(parents=True, exist_ok=True)

    summary = []
    for p in papers:
        dest = Path(p["pdf_path"]) if p.get("pdf_path") else RAW_PDFS_DIR / f"{p['safe_title']}.pdf"
        if dest.exists() and dest.stat().st_size > 0:
            status = "exists"
        else:
            try:
                robust_download(p["url"], dest)
                status = "downloaded"
            except Exception as e:
                status = f"error: {e}"
        summary.append({"title": p["title"], "url": p["url"], "path": str(dest), "status": status})

    print(json.dumps({"summary": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

