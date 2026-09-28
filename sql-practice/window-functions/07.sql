/*
--------------------------------------------------------------------------------
Busy-ness in the previous 15 minutes (time-based RANGE frame)
For each trip, count how many other trips started at the same PULocationID in 
the 15 minutes before it. This needs a RANGE BETWEEN INTERVAL ... PRECEDING AND 
CURRENT ROW frame on a timestamp, not a row-count frame. Also decide how to 
exclude the current trip from its own count.
--------------------------------------------------------------------------------
*/

SELECT
	rowid
	, VendorID
	, tpep_pickup_datetime AS pickup
	, tpep_dropoff_datetime AS dropoff
	, PULocationID
	, COUNT(tpep_pickup_datetime) OVER (
		PARTITION BY PULocationID
		ORDER BY tpep_pickup_datetime
		RANGE BETWEEN INTERVAL '15 minutes' PRECEDING AND CURRENT ROW
		EXCLUDE CURRENT ROW
	) AS total_trips_15_min
FROM taxi.main.trips
WHERE fare_amount > 0 -- cleaning bad data
	AND trip_distance > 0 -- cleaning bad data
	AND DATE_TRUNC('month', tpep_pickup_datetime) = '2026-06-01' -- cleaning bad data
ORDER BY PULocationID, tpep_pickup_datetime 