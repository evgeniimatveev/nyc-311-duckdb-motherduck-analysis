# 🧠 NYC 311 Complaints Analysis — DuckDB + MotherDuck + SQL + Python

![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-orange)
![MotherDuck](https://img.shields.io/badge/MotherDuck-Cloud-blue)
![Python](https://img.shields.io/badge/Python-ETL-yellow?logo=python&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-Analysis-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

This project is a **data analysis + lightweight ETL pipeline** built using DuckDB and MotherDuck.  
It focuses on **NYC 311 Elevator Service Requests**, transforming raw data into **insight-driven storytelling**.

Perfect for showcasing:
- SQL analytics skills  
- Data storytelling  
- ETL automation  
- Modern analytics stack (DuckDB + cloud)

---

## 📊 Project Overview

This project explores complaint patterns across NYC boroughs.

It answers key questions:
- Do complaints follow seasonal patterns?
- Which boroughs generate the most requests?
- When do complaint peaks occur?

---

## 🔧 Tech Stack

- 🐤 **DuckDB** – in-process analytics engine  
- ☁️ **MotherDuck** – cloud analytics layer  
- 🐍 **Python** – ETL and export automation  
- 🧠 **SQL** – data transformation and aggregation  
- 🐳 **Docker** – reproducible environment  
- 🧑‍💻 **VS Code** – development environment  

---

## 📁 Project Structure

```bash
MotherDuck-DuckDB-Course/
│
├── data/
│   └── 311_Elevator_Service_Requests_.csv
│
├── exports/
│   ├── clean_requests.csv
│   └── clean_requests.parquet
│
├── screenshots/
│   ├── DBeaver/
│   ├── DuckDB(CLI)/
│   └── Storytelling/
│
├── scripts/
│   ├── 4_1_duckdb_test.py
│   ├── 4_2_elt.py
│   └── 4_3_export.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── elt.duckdb
├── my_duckdb.duckdb
└── README.md

```

---

## 🧠 Key Insights

- 📈 Complaint volume shows **clear seasonal spikes (summer peak)**
- 🏙️ Bronx consistently generates the **highest number of complaints**
- 🔧 Majority of issues are related to **non-working elevators and lack of backup systems**
- ⚠️ Infrastructure reliability remains a **system-wide issue across boroughs**
- 📊 Demand is **not evenly distributed**, correlating with urban density

---

## 📸 Storytelling (Visual Analysis)

<details>
<summary>📈 Monthly Trend by Borough</summary>

![Monthly Trend](screenshots/Storytelling/Monthly%20trend%20by%20borough_ui.jpg)

</details>

<details>
<summary>🌿 Total Complaints by Borough</summary>

![Total Complaints](screenshots/Storytelling/%20top%20complaint%20descriptors_ui.jpg)

</details>

<details>
<summary>🔝 Top Complaint Types</summary>

![Top Complaints](screenshots/Storytelling/%20top%20complaint%20descriptors_ui.jpg)

</details>

<details>
<summary>📊 Peak Month Detection</summary>

![Peak Months](screenshots/Storytelling/Peak%20months%20detection_ui.jpg)

</details>

<details>
<summary>🔍 Multi-Borough Comparison</summary>

![Comparison](screenshots/Storytelling/Multi-borough%20comparison%20(PORTFOLIO%20GOLD)_ui.jpg)

</details>

<details>
<summary>🧠 Advanced Analysis (EXPLAIN ANALYZE)</summary>

![Explain](screenshots/Storytelling/EXPLAIN%20ANALYZE%20%E2%80%94%20Real%20Execution_ui.jpg)

</details>

<details>
<summary>⚙️ Query Optimization</summary>

![Optimization](screenshots/Storytelling/Improve%20the%20query%20(VERY%20IMPORTANT)_ui.jpg)

</details>

<details>
<summary>🧩 Schema Inspection</summary>

![Schema](screenshots/Storytelling/Inspect%20schema_ui.jpg)

</details>


---

👤 Author

Evgenii Matveev
Data Analyst | MLOps | Automation
