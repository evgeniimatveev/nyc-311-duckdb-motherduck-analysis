This step is very important because now you are not just querying data.
You are comparing environments.

That is already closer to real analytics engineering.

---

## Why this matters

So far you have learned:
- local CSV workflow
- local DuckDB tables
- MotherDuck shared datasets
- EXPLAIN / EXPLAIN ANALYZE

Now we combine all of that into one script.

Think:

local execution
vs
cloud execution

This teaches you:
- how the same business question behaves in different environments
- how filters change query scope
- how to compare outputs in one result table

---

## Step 1 — Compare yearly counts from local vs cloud

Run:

EXPLAIN ANALYZE
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
    'sample_data' AS source
  FROM sample_data.nyc.service_requests
  GROUP BY year
)
SELECT *
FROM local_counts
UNION ALL
SELECT *
FROM md_counts
ORDER BY year, source;

What this does:
- builds one yearly summary from your local table
- builds one yearly summary from MotherDuck shared data
- adds a source label
- combines both results into one comparison table

This is a very strong pattern:
standardize → label → combine → compare

---

## Step 2 — Understand what you are comparing

Important:
This query compares two DIFFERENT scopes.

Local side:
- your imported elevator dataset

Cloud side:
- all service requests from sample_data.nyc.service_requests

That means:
the result is useful for learning execution,
but NOT a fair business comparison yet.

This is still valuable because it teaches:
- structure comparison
- execution plan comparison
- multi-source query design

---

## Step 3 — Make the comparison more fair

Now reduce the cloud scope so it gets closer to your local project focus.

Run:

EXPLAIN ANALYZE
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
    'sample_data' AS source
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

What changed:
- cloud side now keeps only elevator-related complaints
- comparison becomes much more meaningful
- execution should also improve because filter reduces rows

This is already a better analytics design.

---

## Step 4 — Add one more improvement from me (VERY IMPORTANT)

Your local data is already elevator-focused.
Let’s bring both sides closer with borough scope too.

Run:

EXPLAIN ANALYZE
WITH local_counts AS (
  SELECT
    EXTRACT(YEAR FROM "Created Date") AS year,
    COUNT(*) AS complaints,
    'local_manhattan' AS source
  FROM elevator_requests
  WHERE "Borough" = 'MANHATTAN'
  GROUP BY year
),
md_counts AS (
  SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints,
    'motherduck_manhattan' AS source
  FROM sample_data.nyc.service_requests
  WHERE complaint_type ILIKE '%elevator%'
    AND borough = 'MANHATTAN'
  GROUP BY year
)
SELECT *
FROM local_counts
UNION ALL
SELECT *
FROM md_counts
ORDER BY year, source;

Why I added this:
- now the comparison is much more aligned
- same business logic on both sides
- much stronger screenshot
- better storytelling for README or slides

This query answers:
How do local and cloud Manhattan elevator trends compare by year?

---

## Step 5 — Add a difference view (portfolio gold)

Now let’s compare yearly counts side by side instead of stacked rows.

Run:

WITH local_counts AS (
  SELECT
    EXTRACT(YEAR FROM "Created Date") AS year,
    COUNT(*) AS local_complaints
  FROM elevator_requests
  WHERE "Borough" = 'MANHATTAN'
  GROUP BY year
),
md_counts AS (
  SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS md_complaints
  FROM sample_data.nyc.service_requests
  WHERE complaint_type ILIKE '%elevator%'
    AND borough = 'MANHATTAN'
  GROUP BY year
)
SELECT
  COALESCE(l.year, m.year) AS year,
  l.local_complaints,
  m.md_complaints,
  m.md_complaints - l.local_complaints AS difference
FROM local_counts l
FULL OUTER JOIN md_counts m
  ON l.year = m.year
ORDER BY year;

Why this query is strong:
- easier to read than UNION ALL
- shows absolute difference
- great for screenshots
- stronger for business explanation

This is exactly the kind of query that makes a project look serious.

---

## Step 6 — What to look for in EXPLAIN ANALYZE

When you run the UNION comparison queries,
pay attention to:

- which side takes longer
- whether filter reduces cloud work
- whether local scan is simpler
- how sorting and grouping behave
- row counts flowing through the plan

You are training a new skill here:
reading execution, not just results.

---

## Mental Model

You are now comparing:

local source
→ smaller / controlled / reusable

cloud source
→ larger / shared / remote / broader

Same SQL ideas,
different execution context.

That is modern analytics.

---

## Common Mistakes

1. Comparing unmatched scopes
   → misleading conclusions

2. Forgetting borough filter on one side
   → bad comparison

3. Using UNION instead of UNION ALL
   → unnecessary deduplication work

4. Ignoring the source label
   → hard to interpret mixed results

5. Jumping to business conclusions too early
   → first validate scope alignment

---

## Pro Tip

When comparing data sources, always ask:

- same years?
- same filters?
- same complaint definition?
- same borough?
- same grain?

If not:
you are comparing apples to oranges.

---

## Screenshot Ideas

Capture these:

1. union comparison (local vs sample_data)
2. filtered elevator-only comparison
3. Manhattan-aligned comparison
4. side-by-side difference table
5. EXPLAIN ANALYZE for the aligned query

These will look excellent in your project.

---

## Suggested screenshot file names

21_union_local_vs_cloud.png
22_filtered_elevator_comparison.png
23_manhattan_aligned_comparison.png
24_side_by_side_difference.png
25_explain_analyze_comparison.png

---

## Tiny note for correctness

If "Created Date" in your local table is still TEXT,
you may need:

EXTRACT(YEAR FROM CAST("Created Date" AS TIMESTAMP))

But if DuckDB already inferred it as TIMESTAMP,
your current version is fine.

Always verify with:

DESCRIBE elevator_requests;

---

## Next Step

The next clean continuation is:

3.4 Using MotherDuck UI

There we can show:
- cloud exploration in UI
- visual workflow
- analyst-friendly interaction
- more screenshot-friendly project artifacts