import duckdb

con = duckdb.connect('data/taxi.duckdb')
con.sql("CREATE TABLE trips AS SELECT * FROM read_parquet('data/yellow_tripdata_2026-06.parquet')")
print(con.sql('SELECT COUNT(*) FROM trips').fetchall())