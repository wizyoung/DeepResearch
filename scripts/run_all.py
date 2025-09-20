#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]):
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main():
    # 1) Extract (idempotent)
    run([sys.executable, str(ROOT / "scripts" / "extract_and_download.py")])

    # 2) Download PDFs
    run([sys.executable, str(ROOT / "scripts" / "download_pdfs.py")])

    # 3) Translate PDFs to Chinese Markdown with images
    run([sys.executable, str(ROOT / "scripts" / "translate_pdfs.py")])

    # 4) Generate Chinese explanations with code snippets
    run([sys.executable, str(ROOT / "scripts" / "generate_explanations.py")])

    # 5) Notify completion
    notify_url = "https://api.day.app/dbvdz6im6gBj2P6uvWb6HS/agent_read_done"
    run(["curl", "-sS", "-m", "20", "-L", notify_url])


if __name__ == "__main__":
    main()

