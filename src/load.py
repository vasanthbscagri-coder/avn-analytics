"""Load the hospital CSVs and the CRM API pages into SQLite.

Safe to run many times: every table has a primary key and rows are upserted
(INSERT OR REPLACE), so a re-run never creates duplicates.
Run:  python -m src.load
"""
import csv
import json
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB_PATH = ROOT / "db" / "avn.db"
IST = timedelta(hours=5, minutes=30)

SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (dept_id TEXT PRIMARY KEY, name TEXT);
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY, phone_raw TEXT, phone_norm TEXT, registered_on TEXT);
CREATE TABLE IF NOT EXISTS admissions (
    admission_id TEXT PRIMARY KEY, patient_id TEXT, dept_id TEXT, branch TEXT,
    admit_date TEXT, discharge_date TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS bills (
    bill_id TEXT PRIMARY KEY, admission_id TEXT, bill_date TEXT,
    gross_amount INTEGER, gst_amount INTEGER, is_cancelled INTEGER);
CREATE TABLE IF NOT EXISTS leads (
    lead_id TEXT PRIMARY KEY, created_at_utc TEXT, created_at_ist TEXT,
    created_date_ist TEXT, phone_raw TEXT, phone_norm TEXT, channel TEXT);
"""


def normalize_phone(raw):
    """Return the bare 10-digit number: strip spaces/dashes/+, then a leading 91 or 0."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    return digits


def utc_to_ist(utc_text):
    """'2026-09-30T19:00:00Z' -> datetime in IST (UTC+5:30)."""
    dt = datetime.strptime(utc_text, "%Y-%m-%dT%H:%M:%SZ")
    return dt + IST


def read_csv(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_api_pages(folder):
    """Start at leads_page_1.json and follow info.next_page until it is null."""
    leads, page = [], "leads_page_1.json"
    while page:
        with open(folder / page, encoding="utf-8") as f:
            body = json.load(f)
        leads.extend(body["data"])
        page = body["info"]["next_page"]
    return leads


def load(db_path=DB_PATH, data_dir=None):
    global DATA
    if data_dir:
        DATA = Path(data_dir)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA)

    con.executemany("INSERT OR REPLACE INTO departments VALUES (?,?)",
                    [(r["dept_id"], r["name"]) for r in read_csv("departments.csv")])
    con.executemany(
        "INSERT OR REPLACE INTO patients VALUES (?,?,?,?)",
        [(r["patient_id"], r["phone"], normalize_phone(r["phone"]), r["registered_on"])
         for r in read_csv("patients.csv")])
    con.executemany(
        "INSERT OR REPLACE INTO admissions VALUES (?,?,?,?,?,?,?)",
        [(r["admission_id"], r["patient_id"], r["dept_id"], r["branch"], r["admit_date"],
          r["discharge_date"] or None, r["status"]) for r in read_csv("admissions.csv")])
    bills = read_csv("bills.csv")
    con.executemany(
        "INSERT OR REPLACE INTO bills VALUES (?,?,?,?,?,?)",
        [(r["bill_id"], r["admission_id"], r["bill_date"], int(r["gross_amount"]),
          int(r["gst_amount"]), int(r["is_cancelled"])) for r in bills])

    leads = read_api_pages(DATA / "crm_api")
    rows = []
    for r in leads:
        ist = utc_to_ist(r["created_at"])
        rows.append((r["lead_id"], r["created_at"], ist.strftime("%Y-%m-%d %H:%M:%S"),
                     ist.strftime("%Y-%m-%d"), r["phone"], normalize_phone(r["phone"]),
                     r["channel"]))
    con.executemany("INSERT OR REPLACE INTO leads VALUES (?,?,?,?,?,?,?)", rows)
    con.commit()

    print(f"bills in file: {len(bills)}, in db: {con.execute('select count(*) from bills').fetchone()[0]}")
    print(f"leads from API: {len(leads)}, in db: {con.execute('select count(*) from leads').fetchone()[0]}")
    con.close()


if __name__ == "__main__":
    load()
