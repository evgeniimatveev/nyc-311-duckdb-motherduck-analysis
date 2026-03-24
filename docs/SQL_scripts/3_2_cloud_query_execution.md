# 3.2 Cloud Query Execution (DuckDB Lecture Script)

## Goal
Understand how queries are executed in DuckDB vs MotherDuck,
and learn how to analyze performance using EXPLAIN and EXPLAIN ANALYZE.

This is where you move from:
"writing queries" → "understanding execution"

This is a BIG jump in level.

---

## Why this matters

Until now:
- you focused on correctness

Now:
- you start thinking about performance
- execution plans
- query efficiency

This is what separates:
junior → mid-level data engineers

---

## Step 1 — Understand EXPLAIN

EXPLAIN shows:
- how DuckDB plans to execute your query
- what steps are involved
- how data flows internally

Run (LOCAL TABLE):

EXPLAIN 
SELECT 
    strftime('%Y', "created date") AS year,
    COUNT(*) AS complaints
FROM elevator_requests
GROUP BY year
ORDER BY year;

What to look for:
- scan type (table scan vs something else)
- aggregation step
- ordering step

You are not looking for perfection.
You are learning how queries are executed.

---

## Step 2 — Compare with MotherDuck (CLOUD)

Run:

EXPLAIN
SELECT 
    strftime('%Y', created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
GROUP BY year
ORDER BY year;

Key difference:
- data is remote (MotherDuck)
- execution may involve cloud optimizations

Think:
Same SQL → different execution context

---

## Step 3 — Use EXPLAIN ANALYZE (REAL PERFORMANCE)

Now we go deeper.

Run:

EXPLAIN ANALYZE
SELECT 
    strftime('%Y', created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
GROUP BY year
ORDER BY year;

What this adds:
- actual execution time
- rows processed
- operator timing

This is REAL performance data.

---

## Step 4 — Compare with LOCAL execution

Run:

EXPLAIN ANALYZE
SELECT 
    strftime('%Y', "created date") AS year,
    COUNT(*) AS complaints
FROM elevator_requests
GROUP BY year
ORDER BY year;

Now compare:

LOCAL vs CLOUD

Ask yourself:
- which is faster?
- where is time spent?
- how many rows processed?

This is how real performance analysis works.

---

## Step 5 — Improve the query (BEST PRACTICE)

strftime works, but there is a cleaner approach.

Run:

EXPLAIN ANALYZE
SELECT
  EXTRACT(YEAR FROM created_date) AS year,
  COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
GROUP BY year
ORDER BY year;

Why this is better:
- more standard SQL
- often clearer execution
- better readability

Rule:
Prefer EXTRACT over string functions for dates.

---

## Step 6 — Add filter optimization (IMPORTANT 🔥)

Now improve performance by reducing scanned data.

Run:

EXPLAIN ANALYZE
SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE 'elevator'
  AND borough = 'MANHATTAN'
GROUP BY year
ORDER BY year;

Why this matters:
- filters reduce dataset size early
- faster execution
- less memory usage

This is a CORE optimization pattern.

---

## Step 7 — Add projection optimization

Only select needed columns.

Run:

EXPLAIN ANALYZE
SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints
FROM sample_data.nyc.service_requests
WHERE complaint_type ILIKE 'elevator'
GROUP BY year
ORDER BY year;

Notice:
We did NOT select unnecessary columns.

Why:
Less data → faster queries

---

## Mental Model

Query execution pipeline:

SCAN → FILTER → PROJECT → GROUP → SORT

Your job:
Make each step lighter.

---

## Common Mistakes

1. Using SELECT *
   → loads unnecessary data

2. Filtering too late
   → expensive queries

3. Using string functions on dates
   → slower than EXTRACT

4. Ignoring EXPLAIN
   → blind querying

---

## Pro Tip (REAL ENGINEERING MINDSET)

Always ask:

- how much data is scanned?
- can I filter earlier?
- can I reduce columns?
- is my function optimal?

This is how performance thinking develops.

---

## Screenshot Ideas (VERY STRONG)

Capture:

1. EXPLAIN output (local)
2. EXPLAIN output (cloud)
3. EXPLAIN ANALYZE (cloud)
4. optimized query result
5. filtered query result

These screenshots show:
→ you understand execution, not just SQL

---

## Suggested screenshot names

16_explain_local.png  
17_explain_cloud.png  
18_explain_analyze_cloud.png  
19_optimized_query.png  
20_filtered_query.png  

---

## Next Step

Next script:

3.3 Comparing Cloud vs Local

There we will:
- directly compare performance
- show differences clearly
- build strong portfolio storytelling 🔥