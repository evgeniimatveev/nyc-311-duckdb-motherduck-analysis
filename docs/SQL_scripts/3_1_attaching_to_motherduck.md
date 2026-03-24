# 3.1 Attaching to MotherDuck (DuckDB Lecture Script)

## Goal
Connect DuckDB to MotherDuck, attach a shared cloud dataset, and compare cloud queries with your local CSV workflow.

This step is a BIG upgrade.

You move from:
local DuckDB file → cloud-connected analytics

Now you are learning hybrid workflow:
DuckDB + MotherDuck

---

## Why this matters

Until now, you worked with:
- local CSV files
- local DuckDB database files
- local tables and views

Now you add:
- cloud datasets
- shared databases
- reusable remote analytics

Think:

local SQL skills
+ cloud access
= stronger portfolio story

---

## Step 1 — Configure the MotherDuck token

MotherDuck uses an authentication token.

Set it as an environment variable.

macOS / Linux:

export MOTHERDUCK_TOKEN="your_token_here"

Windows PowerShell (persistent):

setx MOTHERDUCK_TOKEN "your_token_here"

Important:
- replace your_token_here with your real token
- restart terminal after setx if needed
- never commit real tokens to GitHub

Tip:
For secure workflows later, keep secrets in .env or secret manager tooling.

---

## Step 2 — Test the connection

Run:

duckdb md:

What this does:
- opens DuckDB connected to MotherDuck
- proves your token works
- confirms cloud connectivity

If this opens successfully:
you are ready for shared cloud datasets.

---

## Step 3 — Attach a shared MotherDuck dataset

Run:

ATTACH 'md:_share/sample_data/23b0d623-1361-421d-ae77-62d701d471e6';

What this means:
- md: = MotherDuck connector
- _share/... = shared cloud database
- you are attaching a remote dataset into your current DuckDB session

This is very powerful:
you can query shared cloud data with normal SQL.

---

## Step 4 — Inspect available databases

Run:

SHOW DATABASES;

What to expect:
You should now see:
- local/system databases
- the attached shared database

This confirms:
the dataset is mounted and visible.

---

## Step 5 — Run a broad cloud query

Run:

SELECT 
    strftime('%Y', created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
GROUP BY year
ORDER BY year;

What this does:
- groups all service requests by year
- uses the shared cloud dataset
- gives you a quick dataset-wide trend

Why start broad:
Always understand the full shape before narrowing scope.

---

## Step 6 — Run a focused cloud query

Run:

SELECT 
    strftime('%Y-%m', created_date) AS month,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
WHERE strftime('%Y', created_date) = '2023'
  AND complaint_type ILIKE 'elevator'
  AND borough = 'MANHATTAN'
GROUP BY month
ORDER BY month;

What this shows:
- monthly trend
- one year only
- one borough only
- one complaint category only

This is already a real business question:
How do Manhattan elevator complaints behave over time in 2023?

---

## Step 7 — Run a yearly filtered trend

Run:

SELECT 
    strftime('%Y', created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE 'elevator'
  AND borough = 'MANHATTAN'
GROUP BY year
ORDER BY year;

Why this query matters:
- compares years directly
- shows long-term trend
- useful for historical storytelling

This is stronger than a single-year monthly chart
because it gives strategic context.

---

## Step 8 — Compare cloud vs local workflow

Now compare the MotherDuck shared dataset
with your local CSV workflow.

Run:

SELECT 
    strftime('%Y', "Created Date") AS year,
    COUNT(*) AS complaints
FROM read_csv_auto('311_Elevator_Service_Requests_.csv')
WHERE "Borough" = 'MANHATTAN'
GROUP BY year
ORDER BY year;

What this teaches you:
- local CSV queries still work
- cloud and local can coexist
- same SQL thinking applies in both places

This is the real lesson:

DuckDB is not just a local database.
It is a flexible analytics engine.

---

## Step 9 — Add one extra query: borough comparison in MotherDuck

Run:

SELECT
    borough,
    COUNT(*) AS elevator_complaints
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE 'elevator'
GROUP BY borough
ORDER BY elevator_complaints DESC;

Why I added this:
- very clean comparison query
- excellent for screenshots
- useful for future charts
- immediately shows geographic distribution

Business question:
Which borough has the highest elevator complaint volume?

---

## Step 10 — Add one extra query: top complaint descriptors

Run:

SELECT
    descriptor,
    COUNT(*) AS total_requests
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE 'elevator'
  AND borough = 'MANHATTAN'
GROUP BY descriptor
ORDER BY total_requests DESC
LIMIT 10;

Why this is valuable:
- moves beyond counts
- shows issue categories
- gives better operational insight

Business question:
What are the most common Manhattan elevator issue descriptions?

---

## Step 11 — Detach the shared database

Run:

DETACH sample_data;

Why this matters:
- clean session management
- removes attached remote database from current session
- good habit when working with multiple sources

---

## Mental Model

You now understand:

local CSV
→ local DuckDB file
→ cloud-attached MotherDuck share
→ same SQL mindset across all layers

This is exactly the kind of flexibility modern analytics teams want.

---

## Common Mistakes

1. Token not configured correctly
   → MotherDuck connection fails

2. Forgetting to restart terminal after setx
   → environment variable is not visible yet

3. Mixing local and cloud schemas carelessly
   → confusing query targets

4. Assuming column names are identical everywhere
   → local CSV and shared datasets may differ slightly

5. Forgetting to detach shares
   → messy multi-source sessions

---

## Pro Tip

Use this workflow:

authenticate
→ connect
→ attach
→ inspect
→ run broad query
→ run focused query
→ compare with local
→ detach cleanly

This creates a professional cloud workflow.

---

## Screenshot Ideas

Capture these:

1. duckdb md: successful connection
2. ATTACH shared database
3. SHOW DATABASES result
4. yearly cloud trend
5. monthly Manhattan elevator trend
6. borough comparison
7. top descriptors query

These screenshots will make the MotherDuck section of your project look VERY strong.

---

## Suggested screenshot file names

09_motherduck_connection.png
10_attach_shared_dataset.png
11_show_databases.png
12_cloud_yearly_trend.png
13_cloud_manhattan_monthly_trend.png
14_cloud_borough_comparison.png
15_top_descriptors_manhattan.png

---

## Next Step

After this, the best next script is:

3.2 Cloud Query Execution

There we can focus on:
- performance mindset
- cleaner analytical queries
- cloud-first exploration
- stronger comparison between local and cloud workflows