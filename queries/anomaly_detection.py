import sys
import json
import duckdb

station_id = sys.argv[1]

con = duckdb.connect()

query = f"""
WITH base AS (
    SELECT 
        station_id,
        timestamp,
        session_id
    FROM read_parquet('data/cold_storage/*/*/*.parquet')
    WHERE station_id = '{station_id}'
),
daily_sessions AS (
    SELECT
        station_id,
        DATE(timestamp) as day,
        COUNT(DISTINCT session_id) as sessions
    FROM base
    GROUP BY station_id, day
),
stats AS (
    SELECT
        AVG(sessions) as mean,
        STDDEV(sessions) as std
    FROM daily_sessions
)
SELECT day
FROM daily_sessions, stats
WHERE std > 0 AND ABS((sessions - mean) / std) > 2
ORDER BY day
"""

result = con.execute(query).fetchall()

dates = [str(r[0]) for r in result]

print(json.dumps({
    "station_id": station_id,
    "anomalous_dates": dates
}))