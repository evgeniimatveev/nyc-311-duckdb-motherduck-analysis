import duckdb

print("DuckDB version:", duckdb.__version__)

conn = duckdb.connect("my_duckdb.duckdb")
print(conn.execute("SELECT 42 AS test_value;").fetchone())
conn.close()