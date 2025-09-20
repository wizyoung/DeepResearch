#!/usr/bin/env python3
import json
from pathlib import Path
import fitz  # PyMuPDF


ROOT = Path(__file__).resolve().parents[1]
RAW_PDFS = ROOT / "raw_pdfs"
OUT_DIR = ROOT / "extracted"


def extract_pdf(pdf_path: Path, out_root: Path):
    doc = fitz.open(pdf_path)
    title = pdf_path.stem
    safe_dir = out_root / title
    text_dir = safe_dir / "text"
    img_dir = safe_dir / "images"
    text_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"title": title, "pages": []}
    for page in doc:
        page_idx = page.number + 1
        txt = page.get_text("text")
        text_file = text_dir / f"page_{page_idx:03d}.txt"
        text_file.write_text(txt, encoding="utf-8")

        page_images = []
        for i, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n >= 5:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            img_name = f"page{page_idx:03d}_img{i+1:02d}.png"
            out_img = img_dir / img_name
            pix.save(out_img)
            pix = None
            page_images.append(img_name)

        manifest["pages"].append({
            "page": page_idx,
            "text_file": str(text_file.relative_to(safe_dir)),
            "images": page_images,
        })

    (safe_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return safe_dir


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for pdf in sorted(RAW_PDFS.glob("*.pdf")):
        extract_pdf(pdf, OUT_DIR)
    print(json.dumps({"status": "ok", "out": str(OUT_DIR)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

