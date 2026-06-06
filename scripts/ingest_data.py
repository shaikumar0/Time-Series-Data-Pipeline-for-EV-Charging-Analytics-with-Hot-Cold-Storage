import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from sqlalchemy import create_engine

# ------------------------
# 1. Load source data
# ------------------------
df = pd.read_parquet("data/source/telemetry.parquet")

print("Loaded rows:", len(df))

# ------------------------
# 2. Prepare partition column
# ------------------------
df["day"] = df["timestamp"].dt.date

# ------------------------
# 3. WRITE TO COLD STORAGE
# ------------------------
os.makedirs("data/cold_storage", exist_ok=True)

table = pa.Table.from_pandas(df)

pq.write_to_dataset(
    table,
    root_path="data/cold_storage",
    partition_cols=["station_region", "day"]
)

print("✅ Cold storage written")

# ------------------------
# 4. FILTER LAST 72 HOURS
# ------------------------
max_time = df["timestamp"].max()
cutoff = max_time - pd.Timedelta(hours=72)

df_hot = df[df["timestamp"] >= cutoff]

print("Hot rows:", len(df_hot))

# ------------------------
# 5. WRITE TO TIMESCALEDB
# ------------------------
engine = create_engine(
    "postgresql://postgres:postgres@hot-db:5432/telemetry"
)

# Create table
df_hot.head(0).to_sql("telemetry", engine, if_exists="replace", index=False)

# Insert data
df_hot.to_sql("telemetry", engine, if_exists="append", index=False)

print("✅ Hot storage written")