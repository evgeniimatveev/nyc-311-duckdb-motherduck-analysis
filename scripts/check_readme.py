"""Re-compute the figures quoted in the README from the raw CSV and check the pipeline output.

Run after the pipeline (scripts/run_pipeline.py). Needs duckdb.

    uv run --no-project --with duckdb python scripts/check_readme.py [committed_exports_dir]
"""
import os
import sys

import duckdb

RAW = "data/311_Elevator_Service_Requests_.csv"
con = duckdb.connect()
con.execute(f"CREATE VIEW r AS SELECT * FROM read_csv_auto('{RAW}', header=True)")
q = lambda sql: con.execute(sql).fetchall()

results = []  # (claim, readme, data)
total = q("SELECT COUNT(*) FROM r")[0][0]
results.append(("records", 22504, total))
boro = dict((b, n) for b, n in q("SELECT Borough, COUNT(*) FROM r GROUP BY 1"))
results.append(("Bronx complaints", 9339, boro["BRONX"]))
results.append(("Bronx share of all, %", 41.5, round(boro["BRONX"] * 100 / total, 1)))
results.append(("Staten Island complaints", 208, boro["STATEN ISLAND"]))
results.append(("Staten Island share, %", 0.9, round(boro["STATEN ISLAND"] * 100 / total, 1)))
results.append(("Bronx vs Staten Island, times", 45, round(boro["BRONX"] / boro["STATEN ISLAND"])))
month = dict(q('SELECT month("Created Date"), COUNT(*) FROM r GROUP BY 1'))
results.append(("July peak", 2432, month[7]))
results.append(("February low", 1502, month[2]))
results.append(("July above February, %", 62, round((month[7] / month[2] - 1) * 100)))
dob = q("SELECT COUNT(*) FROM r WHERE Agency = 'DOB'")[0][0]
results.append(("DOB records", 20825, dob))
results.append(("DOB share, %", 92.5, round(dob * 100 / total, 1)))
alt = q("SELECT COUNT(*) FROM r WHERE \"Descriptor\" = 'Elevator - Single Device On Property/No Alternate Service'")[0][0]
results.append(("'No alternate service' cases", 13195, alt))
results.append(("'No alternate service' share, %", 58.6, round(alt * 100 / total, 1)))

# pipeline output: exports must hold every raw row plus the derived column
if os.path.exists("exports/clean_requests.parquet"):
    n_csv = q("SELECT COUNT(*) FROM read_csv_auto('exports/clean_requests.csv')")[0][0]
    n_par = q("SELECT COUNT(*) FROM read_parquet('exports/clean_requests.parquet')")[0][0]
    cols = [c[0] for c in q("DESCRIBE SELECT * FROM read_parquet('exports/clean_requests.parquet')")]
    results.append(("export rows (parquet) = raw rows", total, n_par))
    results.append(("export rows (csv) = raw rows", total, n_csv))
    results.append(("export has closed_in_days", True, "closed_in_days" in cols))
    results.append(("export columns are snake_case", True, all(c == c.lower() and " " not in c for c in cols)))
    if len(sys.argv) > 1:   # compare with the exports committed to the repo
        old = f"{sys.argv[1]}/clean_requests.parquet"
        results.append(("committed export has the same row count", q(f"SELECT COUNT(*) FROM read_parquet('{old}')")[0][0], n_par))
        old_cols = [c[0] for c in q(f"DESCRIBE SELECT * FROM read_parquet('{old}')")]
        results.append(("committed export has the same columns", old_cols, cols))

bad = [(c, a, b) for c, a, b in results if a != b]
for c, a, b in results:
    print(f"{'OK  ' if a == b else 'FAIL'} {c:<44} README/expected {a!s:<12} data {b}")
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as fh:
        fh.write("## README figures re-computed from the raw CSV\n\n| Check | README / expected | Data | |\n|---|--:|--:|:-:|\n")
        for c, a, b in results:
            fh.write(f"| {c} | {a} | {b} | {'✅' if a == b else '❌'} |\n")
print(f"\n{len(results) - len(bad)} of {len(results)} checks passed")
sys.exit(1 if bad else 0)
