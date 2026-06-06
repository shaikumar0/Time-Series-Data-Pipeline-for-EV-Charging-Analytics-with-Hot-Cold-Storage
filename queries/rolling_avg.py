from sqlalchemy import create_engine, text
import sys, json

station_id = sys.argv[1]
timestamp = sys.argv[2]

engine = create_engine(
    "postgresql://postgres:postgres@hot-db:5432/telemetry"
)

query = text("""
SELECT AVG(power) as avg_power
FROM telemetry
WHERE station_id = :station_id
AND timestamp BETWEEN 
    (CAST(:ts AS TIMESTAMP) - INTERVAL '1 hour')
    AND CAST(:ts AS TIMESTAMP)
""")

with engine.connect() as conn:
    result = conn.execute(query, {
        "station_id": station_id,
        "ts": timestamp
    }).fetchone()

output = {
    "station_id": station_id,
    "timestamp": timestamp,
    "avg_power_1h": float(result[0]) if result[0] else 0
}

print(json.dumps(output))