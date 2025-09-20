#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from typing import List, Tuple

import fitz  # PyMuPDF
from tqdm import tqdm


def ensure_argos_en_zh():
    import argostranslate.package
    import argostranslate.translate

    available_packages = argostranslate.package.get_available_packages()
    en_zh_packages = [p for p in available_packages if p.from_code == "en" and p.to_code in ("zh", "zh-cn", "zh-CN")]
    installed = argostranslate.package.get_installed_packages()
    has_installed = any(p.from_code == "en" and p.to_code.startswith("zh") for p in installed)
    if not has_installed:
        # Choose the first en->zh package
        if not en_zh_packages:
            raise RuntimeError("No Argos Translate en->zh packages available.")
        pkg = en_zh_packages[0]
        download_path = pkg.download()
        argostranslate.package.install_from_path(download_path)


def translate_text(text: str) -> str:
    import argostranslate.translate

    # Argos prefers shorter chunks. Split by paragraphs.
    paragraphs = re.split(r"(\n\s*\n)", text)
    translated_parts: List[str] = []
    for part in paragraphs:
        if part.strip() == "":
            translated_parts.append(part)
            continue
        if part.isspace() or part == "\n\n":
            translated_parts.append(part)
            continue
        translated_parts.append(argostranslate.translate.translate(part, "en", "zh"))
    return "".join(translated_parts)


def save_image(page, image_index: int, assets_dir: Path) -> str:
    xref = page.get_images(full=True)[image_index][0]
    pix = fitz.Pixmap(page.parent, xref)
    if pix.n >= 5:  # CMYK or with alpha
        pix = fitz.Pixmap(fitz.csRGB, pix)
    out_path = assets_dir / f"page{page.number+1:03d}_img{image_index+1:02d}.png"
    pix.save(out_path)
    pix = None
    return out_path.name


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def render_pdf_to_markdown(pdf_path: Path, md_path: Path, assets_dir: Path):
    doc = fitz.open(pdf_path)
    assets_dir.mkdir(parents=True, exist_ok=True)

    md_lines: List[str] = []
    md_lines.append(f"<!-- Source: {pdf_path.name} -->\n")
    md_lines.append(f"# {pdf_path.stem}\n\n")

    for page in tqdm(doc, desc=f"Parsing {pdf_path.name}"):
        md_lines.append(f"\n---\n\n")
        md_lines.append(f"## Page {page.number+1}\n\n")

        # Extract images first in order and reference them inline after their block positions
        images = page.get_images(full=True)

        # Extract text blocks preserving reading order
        blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type, ...)
        blocks_sorted = sorted(blocks, key=lambda b: (round(b[1]/10)*10, round(b[0]/10)*10))

        # Simple heuristic: insert images at top of page before text
        for idx, _ in enumerate(images):
            img_name = save_image(page, idx, assets_dir)
            md_lines.append(f"![figure]({assets_dir.name}/{img_name})\n\n")

        page_text = "\n\n".join(b[4] for b in blocks_sorted if isinstance(b[4], str) and b[4].strip())
        if page_text.strip():
            # Preserve code-looking blocks by fencing before translation
            # For academic PDFs this is rare; we directly translate the text
            cn = translate_text(page_text)
            md_lines.append(cn + "\n\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md_lines))


def main():
    ROOT = Path(__file__).resolve().parents[1]
    RAW_PDFS = ROOT / "raw_pdfs"
    ensure_argos_en_zh()

    for pdf_file in sorted(RAW_PDFS.glob("*.pdf")):
        safe_stem = sanitize_filename(pdf_file.stem)
        md_out = ROOT / f"{safe_stem}_cn.md"
        assets_dir = ROOT / f"{safe_stem}_assets"
        if md_out.exists():
            continue
        render_pdf_to_markdown(pdf_file, md_out, assets_dir)


if __name__ == "__main__":
    main()

