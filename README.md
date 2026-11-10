# AVN Analytics Engineer assignment

Loads hospital CSVs and CRM API pages into SQLite, then computes four September 2026 metrics in SQL.

## Setup and run
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.load               # load data (safe to re-run)
python -m src.run_metrics        # print the four metrics
python -m pytest -q              # run tests
```

## Layout
- `src/load.py` loader (upserts, phone normalisation, UTC to IST, API pagination)
- `src/run_metrics.py` runs every file in `sql/`
- `sql/01..04_*.sql` one query per metric
- `DATA_ISSUES.md` data problems and handling
- `NOTE_TO_MANAGER.md` one-page note for the operations manager
- `tests/` pytest tests

## Results (September 2026, MDU)
Admissions 100; average stay 6.91 days; net revenue 5,116,100; leads 156, converted 17 (10.9%).

## AI tools used
Claude (Anthropic) helped me read the assignment, profile the data, draft the code and the note.
I ran, checked and understood the results myself, and checked the numbers independently with pandas.
