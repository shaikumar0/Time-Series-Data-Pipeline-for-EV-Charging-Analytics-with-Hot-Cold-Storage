import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ----------------------------
# Setup
# ----------------------------
stations = [f"st-{i:03d}" for i in range(1,11)]
regions = ["north","south","east","west"]

start = datetime(2023,1,1)
minutes = 30*24*60

timestamps = [start + timedelta(minutes=i) for i in range(minutes)]

data = []

# ----------------------------
# Generate Data
# ----------------------------
for i, station in enumerate(stations):

    # Ensure all regions appear
    region = regions[i % 4]

    for ts in timestamps:

        voltage = np.random.normal(240,5)
        current = np.random.normal(15,2)

        # ----------------------------
        # Voltage Spike (st-003)
        # ----------------------------
        if station == "st-003" and ts.date() == datetime(2023,1,15).date():
            voltage = np.random.uniform(310,330)

        power = voltage * current

        # ----------------------------
        # Session Drop (st-007)
        # ----------------------------
        if station == "st-007" and ts.date() in [
            datetime(2023,1,18).date(),
            datetime(2023,1,19).date()
        ]:
            session_id = np.random.randint(1,10)   # very low sessions
        else:
            session_id = np.random.randint(1,500)

        data.append([
            ts, station, region,
            voltage, current, power, session_id
        ])

# ----------------------------
# Create DataFrame
# ----------------------------
df = pd.DataFrame(data, columns=[
    "timestamp","station_id","station_region",
    "voltage","current","power","session_id"
])

# ----------------------------
# Save File
# ----------------------------
os.makedirs("data/source", exist_ok=True)

df.to_parquet("data/source/telemetry.parquet")

print("Generated:", len(df))