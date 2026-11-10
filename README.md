AVN Analytics Engineer Assignment

Loads hospital CSVs and CRM API pages into SQLite, then computes four September 2026 metrics in SQL.

Setup and Run

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.load
python -m src.run_metrics
python -m pytest -q

Project Layout

- "src/load.py" – Loader (upserts, phone normalisation, UTC to IST, API pagination)
- "src/run_metrics.py" – Runs every SQL file in "sql/"
- "sql/01..04_*.sql" – One query per metric
- "DATA_ISSUES.md" – Data problems and handling
- "NOTE_TO_MANAGER.md" – One-page note for the operations manager
- "tests/" – Pytest tests

Results (September 2026, MDU)

- Admissions: 100
- Average stay: 6.91 days
- Net revenue: 5,116,100
- Leads: 156
- Converted: 17 (10.9%)

AI Tools Used

Claude (Anthropic) helped me read the assignment, profile the data, draft the code and the note.

I ran, checked and understood the results myself, and checked the numbers independently with pandas.