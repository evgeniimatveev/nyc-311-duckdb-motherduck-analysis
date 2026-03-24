from pathlib import Path

import duckdb


BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "elt.duckdb"
CSV_EXPORT = BASE_DIR / "clean_requests.csv"
PARQUET_EXPORT = BASE_DIR / "clean_requests.parquet"


def main() -> None:
    print("DuckDB Export Pipeline")
    print(f"Database file: {DB_FILE}")

    con = duckdb.connect(str(DB_FILE))

    con.execute(f"""
        COPY clean_requests TO '{CSV_EXPORT.as_posix()}' (HEADER, DELIMITER ',');
    """)
    print(f"Exported clean_requests to {CSV_EXPORT}")

    con.execute(f"""
        COPY clean_requests TO '{PARQUET_EXPORT.as_posix()}' (FORMAT PARQUET);
    """)
    print(f"Exported clean_requests to {PARQUET_EXPORT}")

    rows = con.execute(f"""
        SELECT complaint_type, COUNT(*) AS issues
        FROM read_parquet('{PARQUET_EXPORT.as_posix()}')
        GROUP BY complaint_type
        ORDER BY issues DESC
        LIMIT 10;
    """).fetchall()

    print("\nTop complaint types from Parquet:")
    for row in rows:
        print(row)

    con.close()
    print("\nExport pipeline completed successfully.")
    print("Connection closed.")


if __name__ == "__main__":
    main()
