# Free Road Trip Games Pack

A free, printable, screen-light pack of family road trip games — built around
real car and van trips with kids, grandparents, and low-energy drivers. No
signups, no ads, no tracking, no internet needed after download.

Built by **Asdale Dynamics, LLC** as one of our free, practical family tools.

## What's in the pack

| Sheet (PDF) | Game | Good for |
| --- | --- | --- |
| `pdf/00-cover.pdf` | Pack overview + printing tips | Getting started |
| `pdf/01-license-plate-hunt.pdf` | License Plate Hunt | Interstates, parking lots, state-spotting races |
| `pdf/02-airport-bingo.pdf` | Airport Bingo | Waiting for boarding, two cards per sheet |
| `pdf/03-story-relay.pdf` | Story Relay | Loud-and-proud car games; prompt cards unstick stalled stories |
| `pdf/04-quiet-car-bingo.pdf` | Quiet-Car Bingo | Low-energy hours; point-and-mark, near-silent play |
| `pdf/05-twenty-questions.pdf` | Twenty Questions Cards | Day or night; starter cards so nobody stalls |
| `pdf/06-trip-memory-sheet.pdf` | Trip Memory Sheet | The ride home; one-page fill-in diary per trip |

Design notes:

- **Unbranded sheets.** The printed pages carry no logos, links, or credits —
  print them and hand them to anyone. Credits live here, in the README.
- **Screen-light.** Every game stretches the time between videos without
  needing a screen of its own.
- **Low-energy friendly.** Quiet-Car Bingo and the memory sheet are designed so
  an adult can participate with one word and a thumbs up.
- **Print-ready.** US Letter with sane margins (works fine on A4), ink-light,
  black-and-white printer friendly.

## How to use it

Fast path: print the PDFs in `pdf/` and play. Nothing else is needed.

If you want to rebuild the PDFs from the HTML sources (e.g. after editing a
sheet), run one local script — no network access required:

```sh
python3 build.py          # builds all sheets into pdf/
python3 build.py 02-airport-bingo   # rebuild one sheet
```

Requirements: Python 3.10+ and WeasyPrint (`pip install -r requirements.txt`).

## Editing the games

Every sheet is a plain HTML file in `sheets/` sharing one stylesheet,
`assets/style.css`. Open one in a text editor, change the squares or prompts,
and rebuild. Ideas that losen things up: swap bingo squares for things on your
actual route, add prompts about your own family, or translate the whole pack.

## Verification

```sh
python3 -m pytest -q
```

Tests render every sheet to PDF with WeasyPrint and check that each output is
a well-formed, parseable document (valid header and trailer, readable pages,
title text present). They also assert the sheets contain no branding.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC. Print,
copy, share, or adapt freely; attribution appreciated but not required on the
sheets themselves.

## Related free packs

- **free-travel-planner-kit** — trip logistics: routes, budgets, packing, reservations.
- **free-game-night-hosting-pack** — games for hosted nights at home.

This pack covers the drive itself; those cover everything before and after.
