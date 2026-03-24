
## Goal
Load data from CSV, apply basic transformations, and prepare it for analysis.

This is where we move from:
"just looking at data" → "working with data"

---

## Step 1 — Load data as a virtual table

We continue using:

311_Elevator_Service_Requests_.csv

Instead of repeatedly calling read_csv_auto(...),
we can think of it as a temporary table.

Run:

SELECT *
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
LIMIT 5;

Reminder:
This is NOT stored yet — it’s a query over a file.

---

## Step 2 — Select only useful columns

Real datasets are messy.
You almost NEVER need all columns.

Example:

SELECT
    "Unique Key",
    "Created Date",
    "Agency",
    "Complaint Type",
    "Borough"
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
LIMIT 5;

Why this matters:
- reduces noise
- improves performance
- makes logic clearer

---

## Step 3 — Rename columns (cleaning)

Column names with spaces are painful.

Fix them early:

SELECT
    "Unique Key"        AS request_id,
    "Created Date"      AS created_at,
    "Agency"            AS agency,
    "Complaint Type"    AS complaint_type,
    "Borough"           AS borough
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
LIMIT 5;

Best practice:
Use snake_case for all columns.

---

## Step 4 — Convert data types

Dates often come as TEXT.

Fix it immediately:

SELECT
    "Unique Key" AS request_id,
    CAST("Created Date" AS TIMESTAMP) AS created_at,
    "Borough" AS borough
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
LIMIT 5;

Why:
String dates = broken time analysis.

---

## Step 5 — Filter data

Now we start thinking like analysts.

Example:
Only Elevator complaints in Brooklyn

SELECT *
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
WHERE "Complaint Type" = 'Elevator'
  AND "Borough" = 'BROOKLYN'
LIMIT 10;

---

## Step 6 — Create a reusable table

Now we move from:
"querying a file" → "building a dataset"

CREATE TABLE elevator_requests AS
SELECT
    "Unique Key"        AS request_id,
    CAST("Created Date" AS TIMESTAMP) AS created_at,
    "Agency"            AS agency,
    "Complaint Type"    AS complaint_type,
    "Borough"           AS borough
FROM read_csv_auto('311_Elevator_Service_Requests_.csv');

What this does:
- stores cleaned data
- avoids re-reading CSV
- improves performance

---

## Step 7 — Validate the table

Always verify:

SELECT *
FROM elevator_requests
LIMIT 5;

---

## Mental Model

Raw CSV → Clean SELECT → Structured Table

You are building layers:
1. raw data
2. cleaned data
3. analysis-ready dataset

---

## Common Mistakes

1. Not renaming columns
   → leads to messy queries later

2. Skipping type casting
   → breaks aggregations and time logic

3. Not saving results
   → re-reading CSV every time = slow

4. Filtering too early
   → lose important data

---

## Pro Tip

Think like a pipeline:

read_csv_auto → SELECT → CLEAN → CREATE TABLE

This is already ETL.

---

## Next Step

Now that we have a clean table,
we will:
- aggregate data
- analyze patterns
- build insights

→ Continue to: aggregations & analysis