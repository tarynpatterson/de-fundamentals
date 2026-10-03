# data/

Local dataset used for SQL optimization exercises in `sql-practice/`.

**Setup:**
1. `uv add duckdb` (from `de-fundamentals`)
2. Download one month of NYC TLC Yellow Taxi trip data from the TLC Trip Record Data page (nyc.gov/site/tlc/about/tlc-trip-record-data.page)
3. Save it here as `yellow_tripdata_<month>.parquet`
4. Run `uv run python data/load_taxi.py` to load it into `taxi.duckdb`

Both the Parquet file and the `.duckdb` file are gitignored — this folder is regenerable, not checked in.