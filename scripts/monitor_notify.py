#!/usr/bin/env python3
import json
import time
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def have_all_translations() -> bool:
    papers = json.loads((ROOT / "papers.json").read_text(encoding="utf-8"))
    for p in papers:
        safe_title = p.get("safe_title") or p["title"]
        cn_path = ROOT / f"{safe_title}_cn.md"
        if not cn_path.exists() or cn_path.stat().st_size == 0:
            return False
    return True


def main():
    notify_url = "https://api.day.app/dbvdz6im6gBj2P6uvWb6HS/agent_read_done"
    while True:
        try:
            if have_all_translations():
                subprocess.run(["curl", "-sS", "-m", "20", "-L", notify_url], check=False)
                break
        except Exception:
            pass
        time.sleep(60)


if __name__ == "__main__":
    main()

