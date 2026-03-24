import duckdb


def main() -> None:
    con = duckdb.connect()

    csv_count = con.execute(
        "SELECT COUNT(*) FROM read_csv_auto('exports/clean_requests.csv')"
    ).fetchone()[0]

    parquet_count = con.execute(
        "SELECT COUNT(*) FROM read_parquet('exports/clean_requests.parquet')"
    ).fetchone()[0]

    print("CSV rows:", csv_count)
    print("Parquet rows:", parquet_count)

    assert csv_count == parquet_count, "CSV and Parquet row counts do not match."
    print("OK: counts match")

    con.close()


if __name__ == "__main__":
    main()
