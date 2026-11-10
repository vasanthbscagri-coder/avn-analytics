import sqlite3
from pathlib import Path

import pytest

from src.load import load, normalize_phone, utc_to_ist

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def db(tmp_path):
    path = tmp_path / "test.db"
    load(db_path=path, data_dir=ROOT / "data")
    return path


def one(db, sql_file):
    con = sqlite3.connect(db)
    rows = con.execute((ROOT / "sql" / sql_file).read_text()).fetchall()
    con.close()
    return rows


@pytest.mark.parametrize("raw", ["+91 55500 00001", "05550000001", "55500-00001",
                                 "915550000001", "5550000001"])
def test_phone_formats_all_match(raw):
    assert normalize_phone(raw) == "5550000001"


def test_utc_to_ist_crosses_midnight():
    # 19:00 UTC on 30 Sep is 00:30 on 1 Oct in IST -> must NOT count as September
    assert utc_to_ist("2026-09-30T19:00:00Z").strftime("%Y-%m-%d") == "2026-10-01"
    assert utc_to_ist("2026-08-31T19:00:00Z").strftime("%Y-%m-%d") == "2026-09-01"


def test_reload_creates_no_duplicates(db):
    load(db_path=db, data_dir=ROOT / "data")
    con = sqlite3.connect(db)
    counts = [con.execute(f"select count(*) from {t}").fetchone()[0]
              for t in ("admissions", "bills", "patients", "leads")]
    con.close()
    assert counts == [330, 411, 450, 280]  # duplicate bill and 2 duplicate leads collapsed


def test_september_metrics(db):
    assert one(db, "01_admissions.sql") == [(100,)]
    assert one(db, "02_avg_length_of_stay.sql") == [(6.91, 91)]
    revenue = dict(one(db, "03_net_revenue_by_department.sql"))
    assert revenue["TOTAL"] == 5116100
    assert revenue["Dermatology"] == 2060000
    conv = {r[0]: r[1:3] for r in one(db, "04_lead_conversion.sql")}
    assert conv["TOTAL"] == (156, 17)
