# 2.3 Using DuckDB UI (DuckDB Lecture Script)

## Goal
Use DuckDB UI to explore data, create reusable views, and run analytical queries.

This step upgrades you from:
terminal SQL → interactive data exploration

---

## Step 1 — Start DuckDB UI

Run from terminal:

duckdb -ui

What happens:
- browser opens automatically
- you get a visual SQL editor
- tables + results are interactive

---

## Alternative (inside CLI)

If you are already inside DuckDB:

CALL start_ui();

---

## Why UI matters

CLI = learning  
UI = exploration + speed  

In UI you can:
- run queries faster
- scroll results
- debug visually
- inspect data like in BI tools

---

## Step 2 — Create a View (IMPORTANT)

Instead of querying CSV every time,
we create a reusable layer.

CREATE VIEW elevator_requests AS
SELECT *
FROM read_csv_auto('311_Elevator_Service_Requests_.csv', HEADER=TRUE);

What is a VIEW:
- virtual table
- stored query
- no data duplication

Think:
CSV → VIEW → ANALYSIS

---

## Step 3 — Run your first aggregation

Now we move into REAL analytics.

SELECT 
    strftime('%Y-%m', "Created Date") AS month,
    COUNT(*) AS complaints
FROM elevator_requests
WHERE "Borough" = 'MANHATTAN'
GROUP BY month
ORDER BY month;

What this does:
- extracts month from timestamp
- groups data
- counts complaints
- shows time trend

This is your FIRST insight query 🔥

---

## Step 4 — Improve the query (VERY IMPORTANT)

Let’s make it cleaner and more "production-ready":

SELECT 
    strftime('%Y-%m', CAST("Created Date" AS TIMESTAMP)) AS month,
    COUNT(*) AS complaints
FROM elevator_requests
WHERE "Borough" = 'MANHATTAN'
  AND "Complaint Type" = 'Elevator'
GROUP BY month
ORDER BY month;

Why this is better:
- explicit type casting
- avoids mixed complaint types
- safer for real pipelines

---

## Step 5 — Advanced version (🔥 THIS IS STRONG)

Add ranking + more insight:

SELECT
    strftime('%Y-%m', CAST("Created Date" AS TIMESTAMP)) AS month,
    COUNT(*) AS complaints,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_by_volume
FROM elevator_requests
WHERE "Borough" = 'MANHATTAN'
GROUP BY month
ORDER BY complaints DESC;

Now you have:
- aggregation
- window function
- ranking logic

This is already mid-level SQL.

---

## Step 6 — Multi-borough comparison (PORTFOLIO GOLD)

SELECT
    borough,
    COUNT(*) AS total_requests
FROM (
    SELECT
        "Borough" AS borough
    FROM elevator_requests
) t
GROUP BY borough
ORDER BY total_requests DESC;

This shows:
→ which borough has most elevator issues

---

## Mental Model

You now have:

CSV → VIEW → AGGREGATION → INSIGHTS

This is the foundation of:
- dashboards
- BI tools
- data pipelines

---

## Common Mistakes

1. Not casting dates
   → wrong grouping

2. Forgetting WHERE filters
   → mixed results

3. Overusing SELECT *
   → unclear logic

4. Not using views
   → repeating code

---

## Pro Tip (REAL WORLD)

Always build layers:

VIEW → CLEAN DATA → ANALYTICAL QUERY

Never mix everything in one query.

---

## Screenshot ideas (DO THIS 🔥)

Capture:

1. DuckDB UI open  
2. VIEW created  
3. monthly aggregation result  
4. borough comparison  

These 4 screenshots = strong portfolio section

---

## Step 7 — Comparative Analysis (Storytelling Layer 🔥)

Now we move from single analysis → comparison.

This is where real insights begin.

---

### Query 1 — Monthly trend by borough

SELECT
    strftime('%Y-%m', CAST("Created Date" AS TIMESTAMP)) AS month,
    "Borough" AS borough,
    COUNT(*) AS complaints
FROM elevator_requests
GROUP BY month, borough
ORDER BY month, borough;

What this shows:
- how complaints evolve over time
- differences between boroughs
- seasonal patterns across locations

---

### Query 2 — Total complaints by borough

SELECT
    "Borough" AS borough,
    COUNT(*) AS total_requests
FROM elevator_requests
GROUP BY borough
ORDER BY total_requests DESC;

What this shows:
- which borough has highest demand/issues
- overall distribution of complaints

---

### Query 3 — Peak months detection

SELECT
    strftime('%Y-%m', CAST("Created Date" AS TIMESTAMP)) AS month,
    COUNT(*) AS complaints
FROM elevator_requests
GROUP BY month
ORDER BY complaints DESC
LIMIT 6;

What this shows:
- highest activity periods
- peak demand windows

---

## Storytelling (IMPORTANT 🔥)

Now combine insights:

- Complaints increase mid-year across multiple boroughs
- Manhattan shows a clear seasonal pattern
- Peak months indicate increased infrastructure stress

This is no longer just SQL.

This is:
→ Data storytelling
→ Insight generation
→ Business interpretation

---

## Why this matters

You just moved from:

- writing queries  
→ explaining data behavior  

This is what companies expect from:
- Data Analysts
- BI Analysts
- MLOps (data understanding layer)

---

## Portfolio Tip (🔥 MUST DO)

Create a slide or README section:

"NYC Elevator Complaints — Comparative Analysis"

Include:
- 1 trend query
- 1 comparison query
- 1 insight summary

This is a complete mini-case study.