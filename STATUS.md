# STATUS.md — free-road-trip-games-pack

Built: November 5, 2026

## What was built

A free, printable, screen-light pack of family road trip games, designed for
car and van trips with kids, grandparents, and low-energy drivers. Unbranded
print-ready HTML/CSS sheets that build to PDFs via one local script. Works
fully offline: no signups, no network calls, no tracking.

Seven HTML game sheets in `sheets/` sharing one print stylesheet
(`assets/style.css`):

1. `00-cover` — pack overview, printing tips, real-trip tips (motion-sensitive riders, van crowds, night legs)
2. `01-license-plate-hunt` — all 50 states + DC checklist, bonus finds, race-to-10, van team mode
3. `02-airport-bingo` — two 5x5 bingo cards per sheet with terminal-waiting squares
4. `03-story-relay` — 16 prompt cards + 8 silly-turn cards for cut-and-play storytelling
5. `04-quiet-car-bingo` — two point-and-mark bingo sheets for near-silent, low-energy play
6. `05-twenty-questions` — 12 starter category cards + a 20-question counter
7. `06-trip-memory-sheet` — one-page fill-in diary with doodle box and trip records

Output PDFs in `pdf/` are committed so they can be printed with zero setup.

## How to run it

```sh
pip install -r requirements.txt   # weasyprint, pillow, pypdf, pytest
python3 build.py                  # builds all sheets -> pdf/
python3 build.py 04-quiet-car-bingo   # rebuild one sheet
python3 -m pytest -q              # run the test suite
```

Requirements: Python 3.10+. Rendering is fully local (WeasyPrint), so no
internet is needed to build or use the pack.

## Verification results

- `python3 build.py` renders all 7 sheets successfully.
- `python3 -m pytest -q` — **40 passed, 0 failed**.
- Tests verify per-sheet (parametrized): HTML exists, PDF renders, `%PDF`
  header and `%%EOF` trailer present, pypdf parses it, page count sane,
  expected game title present in the text layer.
- Additional tests: the sheet list matches the HTML directory exactly,
  `build.build_all` covers every sheet and rejects unknown names, no sheet
  contains branding (Asdale/URLs/email), and the committed `pdf/` files parse.
- Page counts: cover, license-plate-hunt, twenty-questions, memory sheet are
  single-page; airport bingo, story relay, and quiet-car bingo are two-page
  (cards/rules second page), which is intentional for a print pack.

## Known gaps

- Sheets are designed for US Letter; A4 prints fine but page counts for the
  two-page sheets may shift slightly by printer.
- No Spanish (or other) translation yet, though the HTML is easy to translate.
- Fonts rely on locally installed sans fonts (Noto Sans / DejaVu Sans / Arial
  fallback), so minor spacing may vary across systems.
- A few bingo squares reference US road culture (silos, sunflower gardens);
  international players may want to swap some squares.

## Credits and license

Built by **Asdale Dynamics, LLC** as a free practical tool.
MIT License — see `LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC).
Game sheets are unbranded by design; grading/credits live here and in the README.

Distinct from **free-travel-planner-kit** (trip logistics) and
**free-game-night-hosting-pack** (at-home hosted games).
