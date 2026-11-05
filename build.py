#!/usr/bin/env python3
"""Build print-ready PDFs from the game sheet HTML files.

One local script, no network: renders every sheets/*.html with WeasyPrint
into pdf/<name>.pdf. Exits non-zero if any sheet fails to render.
"""

from __future__ import annotations

import sys
from pathlib import Path

from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "pdf"

ORDERED_SHEET_NAMES = [
    "00-cover",
    "01-license-plate-hunt",
    "02-airport-bingo",
    "03-story-relay",
    "04-quiet-car-bingo",
    "05-twenty-questions",
    "06-trip-memory-sheet",
]


def build_sheet(name: str, output_dir: Path) -> Path:
    """Render one HTML sheet to a PDF in output_dir and return the PDF path."""
    html_path = SHEETS_DIR / f"{name}.html"
    base_css = ASSETS_DIR / "style.css"
    pdf_path = output_dir / f"{name}.pdf"

    document = HTML(filename=str(html_path))
    document.write_pdf(target=str(pdf_path), stylesheets=[CSS(filename=str(base_css))])
    return pdf_path


def build_all(output_dir: Path = OUTPUT_DIR, sheets: list[str] | None = None) -> list[Path]:
    """Render every (or selected) sheet. Returns the list of PDFs produced."""
    names = sheets if sheets is not None else ORDERED_SHEET_NAMES
    unknown = [n for n in names if not (SHEETS_DIR / f"{n}.html").exists()]
    if unknown:
        raise SystemExit(f"No sheet HTML found for: {', '.join(unknown)}")
    output_dir.mkdir(parents=True, exist_ok=True)
    return [build_sheet(n, output_dir) for n in names]


def main(argv: list[str]) -> int:
    try:
        pdfs = build_all(sheets=argv[1:] or None)
    except SystemExit as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for pdf in pdfs:
        print(f"built {pdf.relative_to(ROOT)}")
    print(f"done: {len(pdfs)} PDF(s) in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
