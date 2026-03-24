# 2.4 Saving and Reusing Local Databases (DuckDB Lecture Script)

## Goal
Create a persistent DuckDB database file, save imported data locally, and reuse it across sessions.

This step is IMPORTANT because we move from:
temporary CSV-based exploration → reusable local analytics database

Now your work starts to feel like a real project.

---

## Why this matters

So far, you have been querying:
- CSV files
- views on top of CSV
- ad hoc exploration

That is good for learning.

But in real workflows, you usually want:
- one local database file
- one reusable table
- faster future queries
- a stable base for dashboards and screenshots

Think:

CSV → DuckDB file → persistent table → reusable analysis layer

---

## Step 1 — Create a local DuckDB database file

Run from terminal:

duckdb elevator_data.duckdb

What this does:
- creates a new DuckDB database file if it does not exist
- opens the DuckDB CLI connected to that file
- gives you a persistent local database

Important:
Everything you save here can be reopened later.

---

## Step 2 — Import the CSV into a persistent table

Run:

CREATE TABLE elevator_requests AS
SELECT *
FROM read_csv_auto(
    '311_Elevator_Service_Requests_.csv',
    HEADER = true,
    AUTO_DETECT = true
);

What this does:
- reads the CSV
- infers schema automatically
- stores the data physically inside elevator_data.duckdb

This is different from a VIEW:
- VIEW = saved query
- TABLE = saved data

TABLE is what you want for reuse.

---

## Step 3 — Sanity check row counts

Always validate the import.

Run:

SELECT COUNT(*) AS table_rows
FROM elevator_requests;

SELECT COUNT(*) AS csv_rows
FROM read_csv_auto(
    '311_Elevator_Service_Requests_.csv',
    HEADER = true,
    AUTO_DETECT = true
);

What to verify:
- both counts should match
- if not, stop and investigate

Why this matters:
Import validation is a real ETL habit.

---

## Step 4 — Inspect schema

Run:

DESCRIBE elevator_requests;

What to look at:
- column names
- inferred data types
- date columns
- numeric vs text fields

Tip:
Schema check should become automatic for you.

---

## Step 5 — Preview stored data

Run:

SELECT *
FROM elevator_requests
LIMIT 5;

This confirms:
- table exists
- import succeeded
- data is readable from local DB

---

## Step 6 — Run a reusable monthly trend query

Run:

SELECT 
    strftime('%Y-%m', CAST("Created Date" AS TIMESTAMP)) AS month,
    COUNT(*) AS complaints
FROM elevator_requests
WHERE "Borough" = 'MANHATTAN'
  AND "Complaint Type" = 'Elevator'
GROUP BY month
ORDER BY month;

What this shows:
- monthly complaint trend
- filtered business scope
- better analytical precision

This is already a solid portfolio query.

---

## Step 7 — Add one more query: borough comparison

Run:

SELECT
    "Borough" AS borough,
    COUNT(*) AS total_complaints
FROM elevator_requests
WHERE "Complaint Type" = 'Elevator'
GROUP BY "Borough"
ORDER BY total_complaints DESC;

Why I added this:
- very clear business comparison
- great for screenshot
- easy future chart in Tableau / DuckDB UI

This query answers:
Which borough generated the most elevator complaints?

---

## Step 8 — Add one more query: top agencies handling requests

Run:

SELECT
    "Agency" AS agency,
    COUNT(*) AS total_requests
FROM elevator_requests
WHERE "Complaint Type" = 'Elevator'
GROUP BY "Agency"
ORDER BY total_requests DESC
LIMIT 10;

Why this is useful:
- shows operational ownership
- good for storytelling
- useful for dashboards

This query answers:
Which agencies appear most often in elevator-related requests?

---

## Step 9 — Quit DuckDB CLI

Run:

.quit

Simple, but important.

You are closing the session,
not deleting the data.

Your database file remains saved locally.

---

## Step 10 — Reopen and reuse the database

Later, reopen it with:

duckdb elevator_data.duckdb

Then verify:

SHOW TABLES;

SELECT *
FROM elevator_requests
LIMIT 5;

This proves:
your work is persistent and reusable.

That is a BIG upgrade from CSV-only exploration.

---

## Mental Model

You now have:

raw CSV
→ imported local table
→ persistent DuckDB database file
→ repeatable analytics workflow

This is how real local analytics starts.

---

## Common Mistakes

1. Recreating the same table again and again
   → causes confusion or duplicate workflow

2. Forgetting to validate row counts
   → dangerous habit in ETL

3. Mixing VIEW and TABLE concepts
   → can lead to wrong assumptions

4. Not casting date fields before time analysis
   → broken trends

---

## Pro Tip

Use this workflow every time:

create DB file
→ import raw data
→ validate counts
→ inspect schema
→ preview rows
→ run analysis

This gives you:
- structure
- repeatability
- clean portfolio evidence

---

## Screenshot Ideas

Capture these:

1. CREATE TABLE completed successfully
2. COUNT(*) validation
3. DESCRIBE elevator_requests
4. Manhattan monthly trend query
5. Borough comparison query

These screenshots will look VERY strong in README or slides.

---

## Suggested file names for screenshots

04_create_persistent_table.png
05_row_count_validation.png
06_schema_describe.png
07_monthly_trend_manhattan.png
08_borough_comparison.png

---

## Next Step

After this file, the logical next move is:

3.1 Attaching to MotherDuck

There we will move from:
local DuckDB workflow → cloud-connected DuckDB workflow

That will make the project even stronger.