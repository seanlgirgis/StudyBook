import argparse
import csv
import os
from pathlib import Path

import psycopg2


def env(name: str, default: str) -> str:
    return os.getenv(name, default)


def build_connection():
    return psycopg2.connect(
        host=env("PGHOST", "localhost"),
        port=int(env("PGPORT", "5432")),
        dbname=env("PGDATABASE", "postgres"),
        user=env("PGUSER", "postgres"),
        password=env("PGPASSWORD", "postgres"),
    )


def create_table(cur):
    cur.execute(
        """
        DROP TABLE IF EXISTS students;
        CREATE TABLE students (
            "index" INTEGER,
            inter_dom TEXT,
            region TEXT,
            gender TEXT,
            academic TEXT,
            age INTEGER,
            age_cate TEXT,
            stay INTEGER,
            stay_cate TEXT,
            japanese INTEGER,
            japanese_cate TEXT,
            english INTEGER,
            english_cate TEXT,
            intimate TEXT,
            religion TEXT,
            suicide TEXT,
            dep TEXT,
            deptype TEXT,
            todep INTEGER,
            depsev TEXT,
            tosc INTEGER,
            apd TEXT,
            ahome TEXT,
            aph TEXT,
            afear TEXT,
            acs TEXT,
            aguilt TEXT,
            amiscell TEXT,
            toas INTEGER,
            partner TEXT,
            friends TEXT,
            parents TEXT,
            relative TEXT,
            profess TEXT,
            phone TEXT,
            doctor TEXT,
            reli TEXT,
            alone TEXT,
            others TEXT,
            internet TEXT,
            partner_bi TEXT,
            friends_bi TEXT,
            parents_bi TEXT,
            relative_bi TEXT,
            professional_bi TEXT,
            phone_bi TEXT,
            doctor_bi TEXT,
            religion_bi TEXT,
            alone_bi TEXT,
            others_bi TEXT,
            internet_bi TEXT
        );
        """
    )


def normalize(value: str):
    if value is None:
        return None
    v = value.strip()
    return None if v == "" else v


def to_int_or_none(value: str):
    v = normalize(value)
    return int(v) if v is not None else None


def load_csv(cur, csv_path: Path):
    columns = [
        "index", "inter_dom", "region", "gender", "academic", "age", "age_cate", "stay", "stay_cate",
        "japanese", "japanese_cate", "english", "english_cate", "intimate", "religion", "suicide",
        "dep", "deptype", "todep", "depsev", "tosc", "apd", "ahome", "aph", "afear", "acs",
        "aguilt", "amiscell", "toas", "partner", "friends", "parents", "relative", "profess", "phone",
        "doctor", "reli", "alone", "others", "internet", "partner_bi", "friends_bi", "parents_bi",
        "relative_bi", "professional_bi", "phone_bi", "doctor_bi", "religion_bi", "alone_bi", "others_bi",
        "internet_bi",
    ]

    int_cols = {"index", "age", "stay", "japanese", "english", "todep", "tosc", "toas"}

    insert_sql = f"INSERT INTO students ({', '.join([f'\"{c}\"' if c == 'index' else c for c in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            values = []
            for col in columns:
                raw = row.get(col)
                if col in int_cols:
                    values.append(to_int_or_none(raw))
                else:
                    values.append(normalize(raw))
            rows.append(tuple(values))

    cur.executemany(insert_sql, rows)


def print_checks(cur):
    cur.execute("SELECT COUNT(*) FROM students;")
    count = cur.fetchone()[0]
    print(f"Loaded rows: {count}")

    cur.execute(
        """
        SELECT "index", inter_dom, stay, todep, tosc, toas
        FROM students
        ORDER BY "index" NULLS LAST
        LIMIT 10;
        """
    )
    preview = cur.fetchall()
    print("Preview (index, inter_dom, stay, todep, tosc, toas):")
    for row in preview:
        print(row)


def main():
    parser = argparse.ArgumentParser(description="Load students CSV into local PostgreSQL")
    parser.add_argument(
        "--csv",
        default=str(Path(__file__).resolve().parents[1] / "data" / "raw" / "students.csv"),
        help="Path to students CSV file",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    conn = build_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                create_table(cur)
                load_csv(cur, csv_path)
                print_checks(cur)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
