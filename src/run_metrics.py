"""Run the four metric queries in sql/ against the database and print the results.
Run:  python -m src.run_metrics
"""
import sqlite3
from pathlib import Path

from src.load import DB_PATH, ROOT


def run(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    for sql_file in sorted((ROOT / "sql").glob("*.sql")):
        cur = con.execute(sql_file.read_text())
        print(f"\n== {sql_file.name}")
        print(" | ".join(c[0] for c in cur.description))
        for row in cur.fetchall():
            print(" | ".join(str(v) for v in row))
    con.close()


if __name__ == "__main__":
    run()
