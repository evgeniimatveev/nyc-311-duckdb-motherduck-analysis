# 6.1 Setting Up DuckLake with S3 and MotherDuck (DuckDB Lecture Script)

## Goal
Create a DuckLake database backed by S3, connect it through MotherDuck, copy clean data into it, query it, test inserts, and clean up safely.

This is a SERIOUS step.

You move from:
local analytics
→ cloud-connected analytics
→ lakehouse-style storage

This is already much closer to real modern data platform work.

---

## Why this step matters

Until now, you worked with:
- CSV files
- local DuckDB databases
- MotherDuck shared datasets

Now you add:
- S3 object storage
- credentials / secrets
- DuckLake database creation
- table copy into cloud-backed storage

Think:

raw data
→ clean table
→ cloud-backed DuckLake
→ reusable analytical storage

That is big.

MotherDuck’s current docs describe DuckLake as a database type that can be fully managed by MotherDuck or use your own object storage bucket, and S3 credentials are typically stored as a MotherDuck secret. :contentReference[oaicite:0]{index=0}

---

## Architecture in simple words

What you are building:

AWS S3
→ stores the data files

MotherDuck
→ manages access / metadata / cloud workflow

DuckDB SQL
→ creates and queries the database

DuckLake
→ gives you a lakehouse-style storage layer

This is not just a normal local table anymore.

---

## Step 1 — Create an S3 bucket

In AWS Console:

1. Open S3
2. Click Create bucket
3. Set:
   - bucket name: globally unique
   - region: choose one region and keep it consistent
   - block public access: keep enabled
4. Create the bucket

Example bucket:
ducklake-andreas-001

Good practice:
Use a dedicated bucket or folder prefix for this project.

Example path:
s3://ducklake-andreas-001/nyc/

---

## Step 2 — Create IAM user access

In AWS IAM:

1. Go to IAM → Users
2. Add a user
3. Give it programmatic-style access through access keys
4. Attach permissions

For learning / testing:
AmazonS3FullAccess is the fastest route

For better practice:
scope permissions only to your bucket

Example policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": [
        "arn:aws:s3:::ducklake-andreas-001",
        "arn:aws:s3:::ducklake-andreas-001/*"
      ]
    }
  ]
}

Why this matters:
Lakehouse work always starts with access control.

---

## Step 3 — Create access keys

Inside the IAM user:

1. Open Security credentials
2. Create access key
3. Choose:
   Application running outside AWS

Save:
- Access Key ID
- Secret Access Key

Important:
The secret key is shown once.

Store it safely.

---

## Step 4 — Collect connection info

You need:

- Access Key ID
- Secret Access Key
- AWS Region
- bucket path

Typical endpoint pattern:
https://s3.<region>.amazonaws.com

Example:
https://s3.us-east-1.amazonaws.com

---

## Step 5 — Create / store the S3 secret in MotherDuck

This part is IMPORTANT.

Your draft says:
“Go to MotherDuck → Secrets and set secret ducklake”

That idea is correct,
but current MotherDuck docs show S3 secrets are created with `CREATE SECRET IN MOTHERDUCK` in SQL, or via the UI Secrets panel. :contentReference[oaicite:1]{index=1}

SQL version:

CREATE SECRET IN MOTHERDUCK (
    TYPE S3,
    KEY_ID 'your_access_key_id',
    SECRET 'your_secret_access_key',
    REGION 'us-east-1',
    SCOPE 'ducklake-andreas-001'
);

Why this is strong:
- credentials stay in MotherDuck
- easier reuse
- better than hardcoding keys in queries

Optional test:

SELECT count(*)
FROM 's3://ducklake-andreas-001/path/to/a/test/file.parquet';

If this works, your S3 secret is valid. MotherDuck documents this pattern for testing S3 connectivity. :contentReference[oaicite:2]{index=2}

---

## Step 6 — Create the DuckLake database

Run:

CREATE DATABASE my_ducklake (
  TYPE DUCKLAKE,
  DATA_PATH 's3://ducklake-andreas-001/nyc/'
);

What this does:
- creates a DuckLake database
- stores data in your S3 path
- gives you a cloud-backed analytical storage layer

This matches the current DuckLake bring-your-own-bucket model described in the MotherDuck docs. :contentReference[oaicite:3]{index=3}

Important:
Use a clean, dedicated folder path.

Example:
s3://ducklake-andreas-001/nyc/

Do not mix random project files there.

---

## Step 7 — Inspect what was created

Run:

SHOW DATABASES;

You should see:
- your normal databases
- my_ducklake

Then run:

SHOW TABLES FROM my_ducklake.main;

At this stage it may be empty.
That is normal.

---

## Step 8 — Copy your clean table into DuckLake

Run:

CREATE TABLE my_ducklake.main.clean_requests AS
SELECT *
FROM course_demo.main.clean_requests;

What this does:
- reads clean data from your existing source
- writes the table into DuckLake-backed storage
- materializes analytical data into your S3-backed database

This is your actual lakehouse load step.

VERY IMPORTANT:
Make sure `course_demo.main.clean_requests` really exists in your environment.

If your real source is local or differently named, adapt it.

For example, your actual source might instead be:

CREATE TABLE my_ducklake.main.clean_requests AS
SELECT *
FROM clean_requests;

or:

CREATE TABLE my_ducklake.main.clean_requests AS
SELECT *
FROM elt.main.clean_requests;

Use the source you really have.

---

## Step 9 — Validate the copied data

Always validate after loading.

Run:

SELECT COUNT(*) AS ducklake_rows
FROM my_ducklake.main.clean_requests;

Then compare with source:

SELECT COUNT(*) AS source_rows
FROM course_demo.main.clean_requests;

Counts should match.

This is non-negotiable ETL discipline.

---

## Step 10 — Run a yearly trend query

Run:

SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints
FROM my_ducklake.main.clean_requests
GROUP BY 1
ORDER BY 1;

What this shows:
- DuckLake table is queryable
- timestamps work
- your analytical layer is alive

This is your first real cloud-backed result.

---

## Step 11 — Add one strong query from me: borough comparison

Run:

SELECT
    borough,
    COUNT(*) AS complaints
FROM my_ducklake.main.clean_requests
GROUP BY borough
ORDER BY complaints DESC;

Why I added this:
- fast business insight
- great screenshot
- easy validation of dimension quality
- strong for dashboard planning

This answers:
Which borough has the largest complaint volume in DuckLake?

---

## Step 12 — Add one more strong query from me: open vs closed status

Run:

SELECT
    status,
    COUNT(*) AS total_requests
FROM my_ducklake.main.clean_requests
GROUP BY status
ORDER BY total_requests DESC;

Why this matters:
- operational insight
- validates real business columns
- useful for support / service workflow storytelling

This answers:
What is the complaint status distribution?

---

## Step 13 — Insert a new record

Run:

INSERT INTO my_ducklake.main.clean_requests (
  unique_key,
  created_date,
  closed_date,
  agency,
  agency_name,
  complaint_type,
  descriptor,
  location_type,
  incident_zip,
  incident_address,
  street_name,
  cross_street_1,
  cross_street_2,
  intersection_street_1,
  intersection_street_2,
  address_type,
  city,
  landmark,
  facility_type,
  status,
  due_date,
  resolution_description,
  resolution_action_updated_date,
  community_board,
  bbl,
  borough,
  x_coordinate_state_plane_,
  y_coordinate_state_plane_,
  open_data_channel_type,
  park_facility_name,
  park_borough,
  vehicle_type,
  taxi_company_borough,
  taxi_pick_up_location,
  bridge_highway_name,
  bridge_highway_direction,
  road_ramp,
  bridge_highway_segment,
  latitude,
  longitude,
  location,
  closed_in_days
)
VALUES (
  90000001,
  TIMESTAMP '2025-09-08 09:15:00',
  NULL,
  'HPD',
  'Department of Housing Preservation',
  'Elevator',
  'Elevator Stuck Between Floors',
  'Residential Building',
  '10001',
  '350 5TH AVE',
  '5TH AVE',
  '33RD ST',
  '34TH ST',
  NULL,
  NULL,
  'ADDRESS',
  'NEW YORK',
  'Empire State Building',
  'Residential',
  'Open',
  TIMESTAMP '2025-09-10 23:59:00',
  NULL,
  NULL,
  '05 MANHATTAN CB5',
  '1015560001',
  'MANHATTAN',
  985000,
  211000,
  'MOBILE',
  'Central Park',
  'MANHATTAN',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  40.748817,
  -73.985428,
  '(40.748817, -73.985428)',
  NULL
);

What this proves:
- table supports writes
- storage is functional
- lakehouse path is active

This is a very strong demonstration step.

---

## Step 14 — Verify the insert

Run:

SELECT
    EXTRACT(YEAR FROM created_date) AS year,
    COUNT(*) AS complaints
FROM my_ducklake.main.clean_requests
GROUP BY 1
ORDER BY 1;

Also run this more targeted check:

SELECT *
FROM my_ducklake.main.clean_requests
WHERE unique_key = 90000001;

Why:
Aggregates are helpful,
but direct record validation is even better.

---

## Step 15 — Clean up safely

If you want to remove the demo table:

DROP TABLE my_ducklake.main.clean_requests;

Important:
Do this only after screenshots / testing.

Cleanup is good practice,
but do not destroy evidence before documenting the project 😄

---

## VERY IMPORTANT practical notes

1. Check column names carefully
   Your insert assumes the destination table has columns exactly matching those names.

2. Check data types carefully
   Especially:
   - created_date
   - closed_date
   - due_date
   - latitude / longitude
   - closed_in_days

3. Check source schema before insert
   Run:

DESCRIBE my_ducklake.main.clean_requests;

4. Check secret scope
   If your S3 secret scope is too narrow, writes may fail.

5. Keep region aligned
   Bucket region and secret region should match.

MotherDuck’s S3 docs note that the secret can be scoped and region must be set correctly for access to work. :contentReference[oaicite:4]{index=4}

---

## Mental Model

You now have:

raw / clean source
→ MotherDuck secret
→ S3-backed DuckLake database
→ copied analytical table
→ validation queries
→ insert test
→ cleanup

This is already lakehouse-style workflow.

---

## Common Mistakes

1. Using wrong source table name
   → CREATE TABLE AS SELECT fails

2. Wrong S3 secret config
   → database creation or writes fail

3. Region mismatch
   → access issues

4. Not validating row counts
   → silent bad loads

5. Inserting values that do not match column order
   → broken records

6. Dropping the table too early
   → lose demo evidence

---

## Pro Tip

For serious project screenshots, capture this sequence:

1. secret created or visible in UI
2. CREATE DATABASE my_ducklake
3. SHOW DATABASES
4. CREATE TABLE AS SELECT into DuckLake
5. row count validation
6. yearly complaints query
7. borough comparison
8. inserted record verification

This will look VERY strong.

---

## Suggested screenshot file names

36_create_s3_secret.png
37_create_ducklake_database.png
38_show_ducklake_database.png
39_copy_clean_requests_into_ducklake.png
40_ducklake_row_count_validation.png
41_ducklake_yearly_trend.png
42_ducklake_borough_comparison.png
43_ducklake_insert_verification.png

---

## Final project value

This section shows that you can work with:

- SQL
- DuckDB
- MotherDuck
- AWS S3
- secrets
- analytical storage
- validation
- insertion testing

That is not a toy exercise anymore.

That is a serious modern data workflow.

---

## Final recommendation from me

Before running the INSERT, do this first:

DESCRIBE my_ducklake.main.clean_requests;

Because if even one column name differs,
the insert script may fail.

This one check can save a lot of debugging.