import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from datetime import timedelta

# ----------------------------
# 1. Load full cold storage
# ----------------------------
df = pd.read_parquet("data/cold_storage")

print("Loaded rows:", len(df))

# ----------------------------
# 2. Find cutoff (latest - 7 days)
# ----------------------------
max_time = df["timestamp"].max()
cutoff = max_time - pd.Timedelta(days=7)

print("Max timestamp:", max_time)
print("Cutoff:", cutoff)

# ----------------------------
# 3. Filter OLD data (>7 days old)
# ----------------------------
old_data = df[df["timestamp"] < cutoff]

print("Old rows:", len(old_data))

# ----------------------------
# 4. Create time columns
# ----------------------------
old_data["day"] = old_data["timestamp"].dt.date
old_data["hour"] = old_data["timestamp"].dt.hour

# ----------------------------
# 5. Aggregate (hourly)
# ----------------------------
summary = old_data.groupby(
    ["station_region", "day", "hour"]
).agg(
    avg_power=("power", "mean"),
    max_voltage=("voltage", "max"),
    session_count=("session_id", "nunique")
).reset_index()

print("Summary rows:", len(summary))

# ----------------------------
# 6. Save to summary storage
# ----------------------------
os.makedirs("data/cold_storage_summary", exist_ok=True)

table = pa.Table.from_pandas(summary)

pq.write_to_dataset(
    table,
    root_path="data/cold_storage_summary",
    partition_cols=["station_region", "day"]
)

print("✅ Summary data written")

# ----------------------------
# 7. (Optional) Delete old raw data
# ----------------------------
# Commented for safety
"""
import shutil

for root, dirs, files in os.walk("data/cold_storage"):
    for d in dirs:
        if "day=" in d:
            day_str = d.split("=")[1]
            day_date = pd.to_datetime(day_str)

            if day_date < cutoff:
                shutil.rmtree(os.path.join(root, d))
"""