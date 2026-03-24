# 4.2 Reading and Transforming Data with Python (DuckDB Lecture Script)

## Goal
Use Python + DuckDB to inspect raw data, compare raw vs cleaned tables, and understand how transformation changes the dataset.

This is where Python starts behaving like an ETL control layer.

You are moving from:
manual SQL exploration → programmatic validation workflow

---

## Why this step matters

So far you already have:
- raw table: elevator_requests
- cleaned table: clean_requests
- local DuckDB databases
- cloud exploration with MotherDuck

Now the question becomes:

What changed after cleaning?

That is a VERY important ETL mindset.

You are no longer just querying data.
You are validating transformation quality.

---

## Step 1 — Open the raw DuckDB database

Run:

duckdb elevator_data.duckdb

Then check what is inside:

SHOW TABLES;

DESCRIBE elevator_requests;

Why:
- confirm the raw table exists
- inspect original schema
- identify original column names and types

This is your raw layer.

---

## Step 2 — Inspect complaint distribution in the raw table

Run:

SELECT 
    "Complaint Type",
    COUNT(*) AS complaint_count
FROM elevator_requests
GROUP BY "Complaint Type"
ORDER BY complaint_count DESC;

What this tells you:
- whether only Elevator exists
- whether there are mixed categories
- whether raw import still contains variation in values

This is a good validation query.

It answers:
How clean is the source dataset before transformation?

---

## Step 3 — Open the transformed database

Run:

duckdb elt.duckdb

This should connect you to the transformed / ETL-ready database.

Now inspect the cleaned table:

SHOW TABLES;

DESCRIBE clean_requests;

Why this is important:
You want to compare:
raw schema vs cleaned schema

This is exactly how real ETL validation works.

---

## Step 4 — Check complaint distribution in the cleaned table

Run:

SELECT 
    complaint_type,
    COUNT(*) AS complaint_count
FROM clean_requests
GROUP BY complaint_type
ORDER BY complaint_count DESC;

What to look for:
- standardized naming
- lowercase / snake_case cleanup
- removal of inconsistent variants
- whether transformation simplified the data

This query answers:
Did cleaning improve category consistency?

---

## Step 5 — Compare raw vs clean conceptually

You now have two layers:

Raw:
- original column names
- original casing
- original structure

Clean:
- standardized column names
- cleaner schema
- easier analytical queries

Think:

raw import
→ clean transformation
→ analysis-ready dataset

This is the foundation of ETL.

---

## Step 6 — Add a strong validation query from me (VERY USEFUL)

Run this in the cleaned database:

SELECT
    complaint_type,
    borough,
    COUNT(*) AS total_requests
FROM clean_requests
GROUP BY complaint_type, borough
ORDER BY total_requests DESC
LIMIT 15;

Why I added this:
- validates cleaned dimensions
- shows whether borough values are normalized
- gives you a better analytical preview

This is a strong portfolio query because it shows:
category + geography

---

## Step 7 — Add another useful query from me (data quality mindset)

Run:

SELECT
    COUNT(*) AS total_rows,
    COUNT(created_at) AS non_null_created_at,
    COUNT(borough) AS non_null_borough,
    COUNT(complaint_type) AS non_null_complaint_type
FROM clean_requests;

Why this matters:
This is not just analysis.
This is validation.

It helps you check:
- missing timestamps
- missing borough values
- missing complaint types

This is the kind of thing good data engineers ALWAYS look at.

---

## Step 8 — Recommended Python direction from here

Your SQL validation is already strong.

The next Python step is to automate all of this in a script like:

- connect to raw DB
- connect to clean DB
- run validation queries
- print results
- optionally export summaries

Think of Python as the orchestrator.

SQL does the logic.
Python controls the workflow.

---

## Step 9 — If you hit the _ctypes error in WSL

This usually means your Python build is missing required system libraries.

Install required Linux packages:

sudo apt update
sudo apt install -y build-essential libffi-dev libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    liblzma-dev

Then clean up pyenv:

pyenv uninstall motherduck
pyenv uninstall 3.11.6
pyenv install 3.11.6

Re-create the environment:

pyenv virtualenv 3.11.6 motherduck
pyenv activate motherduck
python -m pip install --upgrade pip
pip install duckdb pandas

Why this works:
- rebuilds Python with required native modules
- restores missing dependencies
- gives you a stable DuckDB environment

---

## Mental Model

You are now working with layers:

CSV
→ raw DuckDB table
→ cleaned ETL table
→ validation queries
→ Python automation

This is already real pipeline thinking.

---

## Common Mistakes

1. Comparing raw and clean tables without checking schema
   → easy to misread differences

2. Assuming cleaned data is automatically correct
   → always validate

3. Ignoring NULL checks
   → dangerous for downstream analysis

4. Not separating raw DB and transformed DB mentally
   → creates confusion in project structure

5. Treating Python as optional
   → Python is what makes ETL reusable

---

## Pro Tip

Use this validation sequence every time:

SHOW TABLES
→ DESCRIBE
→ category distribution
→ NULL checks
→ grouped business query

This gives you both:
- technical confidence
- business understanding

---

## Screenshot Ideas

Capture these:

1. raw table schema
2. raw complaint distribution
3. clean table schema
4. clean complaint distribution
5. complaint_type + borough summary
6. non-null validation query

These screenshots will make your ETL section look very professional.

---

## Suggested screenshot file names

30_raw_schema.png
31_raw_complaint_distribution.png
32_clean_schema.png
33_clean_complaint_distribution.png
34_clean_borough_summary.png
35_data_quality_non_nulls.png

---

## Next Step

The clean continuation after this is:

4.2 Python ETL Script

There we can build a real Python file that:
- reads raw data
- transforms columns
- creates clean_requests
- validates output
- saves everything cleanly

That will be a serious upgrade 🚀