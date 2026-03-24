# 4.1 DuckDB + Python Setup (DuckDB Lecture Script)

## Goal
Set up a Python environment with DuckDB and start querying data programmatically.

This is a MAJOR upgrade.

You move from:
SQL-only workflow → Python + SQL hybrid workflow

Now you can:
- automate queries
- build ETL pipelines
- integrate with real applications

---

## Why this matters

Until now:
- you manually ran SQL
- used CLI / UI tools

Now:
- Python becomes your control layer
- DuckDB becomes your engine
- SQL becomes your language

Think:

Python → DuckDB → SQL → Data → Results

---

## Step 1 — Verify environment

After setup, make sure everything works.

Run:

python -c "import duckdb; print(duckdb.__version__)"

Expected:
- version number printed
- no errors

If this works → you are ready.

---

## Step 2 — Create your first Python script

Create file:

4_1_duckdb_python.py

---

## Step 3 — Connect to DuckDB

Basic connection:

import duckdb

conn = duckdb.connect('elevator_data.duckdb')

What this does:
- opens your local database file
- allows SQL execution from Python

---

## Step 4 — Run your first query

query = """
SELECT *
FROM elevator_requests
LIMIT 5;
"""

result = conn.execute(query).fetchdf()

print(result)

What happens:
- SQL runs inside DuckDB
- result is returned as pandas DataFrame
- you can print / manipulate it

---

## Step 5 — Run your first aggregation

query = """
SELECT 
    EXTRACT(YEAR FROM "Created Date") AS year,
    COUNT(*) AS complaints
FROM elevator_requests
WHERE "Borough" = 'MANHATTAN'
GROUP BY year
ORDER BY year;
"""

df = conn.execute(query).fetchdf()

print(df)

Now you are doing:
SQL + Python + DataFrames

This is real data workflow.

---

## Step 6 — Connect to MotherDuck from Python

IMPORTANT:
Make sure your token is already set.

Then:

conn = duckdb.connect('md:')

query = """
SELECT 
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE '%elevator%'
  AND borough = 'MANHATTAN'
GROUP BY year
ORDER BY year;
"""

df = conn.execute(query).fetchdf()

print(df)

This is HUGE:
You are now querying cloud data from Python.

---

## Step 7 — Compare local vs cloud in Python

query = """
WITH local_counts AS (
  SELECT
    EXTRACT(YEAR FROM "Created Date") AS year,
    COUNT(*) AS complaints,
    'local' AS source
  FROM elevator_requests
  GROUP BY year
),
md_counts AS (
  SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints,
    'motherduck' AS source
  FROM sample_data.nyc.service_requests
  WHERE complaint_type ILIKE '%elevator%'
  GROUP BY year
)
SELECT *
FROM local_counts
UNION ALL
SELECT *
FROM md_counts
ORDER BY year, source;
"""

df = conn.execute(query).fetchdf()

print(df)

Now you:
- combine sources
- compare datasets
- do analytics in Python

---

## Step 8 — Save results to CSV (VERY IMPORTANT)

df.to_csv('outputs/yearly_comparison.csv', index=False)

Why:
- reproducibility
- sharing results
- Tableau / BI integration
- portfolio artifact

---

## Step 9 — Close connection

conn.close()

Always clean up connections.

---

## Mental Model

You now have:

Python
→ controls execution

DuckDB
→ executes queries

SQL
→ defines logic

DataFrame
→ stores results

This is the foundation of:
- ETL pipelines
- data apps
- analytics workflows

---

## Common Mistakes

1. Forgetting connection string
   → connecting to wrong DB

2. Not using triple quotes for SQL
   → syntax errors

3. Not closing connection
   → bad practice in pipelines

4. Mixing local and cloud incorrectly
   → broken queries

---

## Pro Tip

Keep SQL inside Python clean:

query = """SQL HERE"""

Don’t build messy string concatenations.

Clean SQL = readable code.

---

## Project Upgrade Idea (🔥)

Create structure:

/scripts
    4_1_duckdb_python.py
/outputs
    yearly_comparison.csv

This turns your project into:
→ reproducible pipeline

---

## Screenshot Ideas

Capture:

1. Python script running
2. printed DataFrame output
3. saved CSV file
4. cloud query result in Python

---

## Suggested file names

26_python_connection.png  
27_python_query_output.png  
28_python_cloud_query.png  
29_export_csv.png  

---

## Next Step

Next script:

4.2 Reading and Transforming Data (Python ETL)

There we will:
- automate CSV ingestion
- build transformations in Python
- simulate real ETL workflow 🚀