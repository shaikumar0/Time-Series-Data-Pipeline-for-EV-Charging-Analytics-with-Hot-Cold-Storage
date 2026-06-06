import sys
import json
import duckdb

region1 = sys.argv[1]
region2 = sys.argv[2]

con = duckdb.connect()

def get_peak(region):
    query = f"""
    SELECT
        EXTRACT(hour FROM timestamp) as hour,
        AVG(power) as avg_power
    FROM read_parquet('data/cold_storage/*/*/*.parquet')
    WHERE station_region = '{region}'
    GROUP BY hour
    HAVING COUNT(*) > 0
    ORDER BY avg_power DESC
    LIMIT 1
    """
    result = con.execute(query).fetchone()
    
    if result is None:
        return 0   # safer default
    
    return int(result[0])
output = {
    region1: {"peak_hour_utc": get_peak(region1)},
    region2: {"peak_hour_utc": get_peak(region2)}
}

print(json.dumps(output))