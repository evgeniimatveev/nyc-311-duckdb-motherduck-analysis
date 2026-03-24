import duckdb


def main() -> None:
    print("Running DuckDB smoke test...")

    # Check version
    version = duckdb.__version__
    print(f"DuckDB version: {version}")

    # Simple query test
    con = duckdb.connect()
    result = con.execute("SELECT 42 AS test_value;").fetchone()

    assert result[0] == 42, "Smoke test failed: unexpected query result"

    print(f"Test query result: {result[0]}")
    con.close()

    print("DuckDB smoke test passed successfully.")


if __name__ == "__main__":
    main()
