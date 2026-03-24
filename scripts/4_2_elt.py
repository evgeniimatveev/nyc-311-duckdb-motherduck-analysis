import re
from pathlib import Path

import duckdb


BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "elt.duckdb"
CSV_FILE = BASE_DIR / "data" / "311_Elevator_Service_Requests_.csv"

RAW_TABLE = "service_requests"
CLEAN_TABLE = "clean_requests"


def normalize_colname(name: str) -> str:
    name = name.strip().lower().replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def main() -> None:
    print("DuckDB ELT Pipeline")
    print(f"Database file: {DB_FILE}")
    print(f"CSV file: {CSV_FILE}")

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    con = duckdb.connect(str(DB_FILE))

    con.execute(f"""
        CREATE OR REPLACE TABLE {RAW_TABLE} AS
        SELECT *
        FROM read_csv_auto('{CSV_FILE.as_posix()}', header=True);
    """)
    print(f"Loaded raw data into '{RAW_TABLE}'.")

    con.execute(f"""
        CREATE OR REPLACE TABLE {CLEAN_TABLE} AS
        SELECT
            * REPLACE (LOWER("Complaint Type") AS "Complaint Type")
        FROM {RAW_TABLE};
    """)
    print(f"Created '{CLEAN_TABLE}'.")

    cols = con.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{CLEAN_TABLE}'
        ORDER BY ordinal_position;
    """).fetchall()

    for (old_name,) in cols:
        new_name = normalize_colname(old_name)
        if new_name != old_name:
            con.execute(
                f'ALTER TABLE {CLEAN_TABLE} RENAME COLUMN "{old_name}" TO {new_name};'
            )
            print(f"Renamed: {old_name} -> {new_name}")

    existing_columns = {
        row[1] for row in con.execute(f"PRAGMA table_info('{CLEAN_TABLE}');").fetchall()
    }

    if "closed_in_days" not in existing_columns:
        con.execute(f"""
            ALTER TABLE {CLEAN_TABLE}
            ADD COLUMN closed_in_days INTEGER;
        """)
        print("Added column: closed_in_days")

    con.execute(f"""
        UPDATE {CLEAN_TABLE}
        SET closed_in_days = DATEDIFF('day', created_date, closed_date)
        WHERE created_date IS NOT NULL
          AND closed_date IS NOT NULL;
    """)
    print("Populated column: closed_in_days")

    print("\nSchema:")
    schema_rows = con.execute(f"PRAGMA table_info('{CLEAN_TABLE}');").fetchall()
    for row in schema_rows:
        print(row)

    print("\nSample rows:")
    sample_rows = con.execute(f"""
        SELECT created_date, closed_date, closed_in_days
        FROM {CLEAN_TABLE}
        WHERE closed_date IS NOT NULL
        LIMIT 10;
    """).fetchall()
    for row in sample_rows:
        print(row)

    con.close()
    print("\nELT pipeline completed successfully.")
    print("Connection closed.")


if __name__ == "__main__":
    main()
