"""Tests for the free road trip games pack.

Verifies that every game sheet renders a valid PDF with WeasyPrint and that
the output is a well-formed PDF that pypdf can parse.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pypdf import PdfReader
from weasyprint import CSS, HTML

import build

EXPECTED_SHEETS = build.ORDERED_SHEET_NAMES


@pytest.fixture(scope="module", params=EXPECTED_SHEETS)
def built_pdf(request, tmp_path_factory):
    """Render one sheet per test case into an isolated temp directory."""
    tmp_dir = tmp_path_factory.mktemp("pdf")
    pdf_path = build.build_sheet(request.param, tmp_dir)
    return pdf_path, request.param, build.SHEETS_DIR / f"{request.param}.html"


def test_every_sheet_is_accounted_for():
    html_files = sorted(p.stem for p in build.SHEETS_DIR.glob("*.html"))
    assert html_files == sorted(EXPECTED_SHEETS), (
        f"sheet dir and known list disagree: {html_files} vs {EXPECTED_SHEETS}"
    )


def test_sheet_html_exists(built_pdf):
    _, _, html_path = built_pdf
    assert html_path.is_file()
    content = html_path.read_text(encoding="utf-8")
    assert "<html" in content


def test_pdf_file_created(built_pdf):
    pdf_path, _, _ = built_pdf
    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 0


def test_pdf_has_valid_header_and_trailer(built_pdf):
    pdf_path, _, _ = built_pdf
    raw = pdf_path.read_bytes()
    assert raw.startswith(b"%PDF-"), "missing %PDF header"
    assert b"%%EOF" in raw[-1024:], "missing %%EOF marker"


def test_pdf_parses_with_expected_pages(built_pdf):
    pdf_path, name, _ = built_pdf
    reader = PdfReader(str(pdf_path))
    assert reader.is_encrypted is False
    page_count = len(reader.pages)
    if name.endswith("cover") or name.endswith("memory-sheet"):
        assert page_count == 1
    else:
        assert page_count >= 1
    for page in reader.pages:
        assert float(page.mediabox.width) > 0
        assert float(page.mediabox.height) > 0


def test_pdf_contains_expected_title_text(built_pdf):
    """Each sheet should carry its game title into the PDF text layer."""
    pdf_path, name, _ = built_pdf
    reader = PdfReader(str(pdf_path))
    text = " ".join(page.extract_text() or "" for page in reader.pages).lower()
    expected_tokens = {
        "00-cover": "print & play",
        "01-license-plate-hunt": "license plate hunt",
        "02-airport-bingo": "airport bingo",
        "03-story-relay": "story relay",
        "04-quiet-car-bingo": "quiet-car bingo",
        "05-twenty-questions": "twenty questions",
        "06-trip-memory-sheet": "memory sheet",
    }
    assert expected_tokens[name] in text, f"missing title text '{expected_tokens[name]}' in {name}"


def test_sheets_are_unbranded():
    """Game sheets must not carry product or company branding."""
    for name in EXPECTED_SHEETS:
        content = (build.SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
        for brand in ("Asdale", "dylanasdale", "gmail.com", "http://", "https://"):
            assert brand.lower() not in content.lower(), f"{name} mentions {brand}"


def test_built_pdfs_in_repo_match_expectations():
    """If pdf/ output was committed/built, it should parse cleanly too."""
    pdf_dir = build.ROOT / "pdf"
    for name in EXPECTED_SHEETS:
        pdf_path = pdf_dir / f"{name}.pdf"
        if not pdf_path.is_file():
            pytest.fail(f"pdf/{name}.pdf missing; run `python3 build.py`")
        PdfReader(str(pdf_path))  # raises on malformed PDF


def test_build_all_reports_every_sheet(tmp_path):
    pdfs = build.build_all(output_dir=tmp_path)
    assert [p.name for p in pdfs] == [f"{n}.pdf" for n in EXPECTED_SHEETS]


def test_build_all_fails_on_unknown_sheet(tmp_path):
    with pytest.raises(SystemExit):
        build.build_all(output_dir=tmp_path, sheets=["99-nope"])
