# 🚗 EV Charging Time-Series Data Pipeline

## 📌 Overview

This project implements a **time-series data pipeline** for EV (Electric Vehicle) charging analytics using a **Hot/Cold storage architecture**.

The system simulates telemetry data from EV charging stations and enables:

* ⚡ Real-time monitoring (Hot Storage)
* 📊 Historical analytics (Cold Storage)
* 🧠 Data lifecycle management (Compaction)

---

## 🏗️ Architecture

```
Data Generator (Python)
        │
        ▼
Ingestion Script (Dual Write)
        │
        ├── Hot Storage → TimescaleDB (Last 72 hours)
        │
        └── Cold Storage → Parquet Files (30 days)
                │
                ▼
        Analytical Queries (DuckDB / SQL)
                │
                ▼
        Data Compaction (Hourly Aggregates)
```

---

## 🧰 Tech Stack

* **Python** (Pandas, NumPy)
* **Docker & Docker Compose**
* **TimescaleDB (PostgreSQL)** → Hot Storage
* **Parquet + PyArrow** → Cold Storage
* **DuckDB** → Analytical queries
* **SQLAlchemy** → DB connectivity

---

## 📂 Project Structure

```
ev-charging-data-pipeline/
│
├── data/
│   ├── source/
│   ├── cold_storage/
│   └── cold_storage_summary/
│
├── scripts/
│   ├── generate_data.py
│   ├── ingest_data.py
│   └── compact_data.py
│
├── queries/
│   ├── rolling_avg.py
│   ├── anomaly_detection.py
│   └── peak_load.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── README.md
└── SCALABILITY.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Start Docker Services

```bash
docker compose up --build -d
```

---

### 2️⃣ Generate Data

```bash
python scripts/generate_data.py
```

* Generates **432,000 rows**
* Stored at:

  ```
  data/source/telemetry.parquet
  ```

---

### 3️⃣ Run Ingestion (Dual Write)

```bash
docker exec -it data-tools bash
python scripts/ingest_data.py
```

✔ Writes:

* **Hot Storage** → Last 72 hours
* **Cold Storage** → Full dataset (partitioned)

---

## 📊 Analytical Queries

Run inside Docker container:

```bash
docker exec -it data-tools bash
```

---

### 🔹 1. Rolling Average (Hot Storage)

```bash
python queries/rolling_avg.py st-001 2023-01-30T10:00:00
```

Output:

```json
{
  "station_id": "st-001",
  "timestamp": "2023-01-30T10:00:00",
  "avg_power_1h": 3638.41
}
```

---

### 🔹 2. Anomaly Detection (Cold Storage)

```bash
python queries/anomaly_detection.py st-007
```

Output:

```json
{
  "station_id": "st-007",
  "anomalous_dates": ["2023-01-18", "2023-01-19"]
}
```

✔ Detects **session drop anomaly**

---

### 🔹 3. Peak Load Analysis (Cold Storage)

```bash
python queries/peak_load.py north south
```

Output:

```json
{
  "north": {"peak_hour_utc": 3},
  "south": {"peak_hour_utc": 17}
}
```

---

## 🧊 Cold Storage Design

* Format: **Parquet (columnar)**
* Partitioning:

  ```
  station_region=<region>/day=<YYYY-MM-DD>/
  ```

✔ Improves query performance
✔ Enables partition pruning

---

## 🔥 Hot Storage Design

* Database: **TimescaleDB**
* Stores:

  * Only **last 72 hours**
* Optimized for:

  * Fast inserts
  * Real-time queries

---

## 🔄 Data Compaction

Run:

```bash
python scripts/compact_data.py
```

✔ Converts old raw data (>7 days) into **hourly aggregates**

### Output:

```
data/cold_storage_summary/
```

### Schema:

* station_region
* day
* hour
* avg_power
* max_voltage
* session_count

---

## 🚨 Anomaly Injection

The dataset includes:

* ⚡ **Voltage Spike**

  * Station: `st-003`
  * Voltage > 300

* 📉 **Session Drop**

  * Station: `st-007`
  * Two consecutive days

---

## 📈 Key Features

* Dual-write architecture (Hot + Cold)
* Time-series data modeling
* Partitioned data lake design
* SQL-based analytics
* Data lifecycle management

---

## 🧠 Learning Outcomes

* Designing scalable data pipelines
* Working with time-series databases
* Optimizing analytical queries
* Implementing data compaction strategies
* Understanding trade-offs in storage systems

---

## 📌 How to Run Complete Pipeline

```bash
docker compose up --build -d

python scripts/generate_data.py

docker exec -it data-tools bash
python scripts/ingest_data.py

python queries/rolling_avg.py st-001 2023-01-30T10:00:00
python queries/anomaly_detection.py st-007
python queries/peak_load.py north south

python scripts/compact_data.py
```

---

## ✅ Conclusion

This project demonstrates a **production-style data engineering pipeline** combining:

* Real-time processing
* Historical analytics
* Efficient storage design

It can be extended to large-scale systems using distributed technologies like Kafka, Spark, and cloud data lakes.

---
"# EV-Charging-Analytics" 
