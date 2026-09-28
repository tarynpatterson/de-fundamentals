/*
--------------------------------------------------------------------------------
Find the longest streak of the same payment type (gaps and islands)
For each VendorID, ordered by pickup time, find the longest run of consecutive 
trips with the same payment_type. Return the vendor, payment type, streak length,
and the start and end pickup times of that streak. This is the classic "gaps and
islands" pattern: the trick is subtracting two ROW_NUMBER() calls (one partitioned
by vendor, one by vendor and payment type) to label each island, then aggregating
by that label. Because of the tied-timestamp issue you found earlier, add a
tiebreaker to your ORDER BY. DuckDB has a built-in rowid pseudo-column you can use
for that.
--------------------------------------------------------------------------------
*/

WITH trips_filtered AS (
	SELECT
		VendorID
		, rowid
		, tpep_pickup_datetime AS pickup
		, tpep_dropoff_datetime AS dropoff
		, payment_type
	FROM taxi.main.trips
	WHERE fare_amount > 0 -- cleaning bad data
		AND trip_distance > 0 -- cleaning bad data
		AND DATE_TRUNC('month', tpep_pickup_datetime) = '2026-06-01' -- cleaning bad data
)

, trips_numbered AS (
	SELECT
		rowid
		, VendorID
		, pickup
		, dropoff
		, payment_type
		, ROW_NUMBER() OVER (PARTITION BY VendorID ORDER BY pickup, rowid) AS row_num_trip
		, ROW_NUMBER() OVER (PARTITION BY VendorID, payment_type ORDER BY pickup, rowid) AS row_num_payment
	FROM trips_filtered
)

, islands AS (
	SELECT
		VendorID
		, payment_type
		, row_num_trip - row_num_payment AS island_id
		, COUNT(*) AS streak_length
		, MIN(pickup) AS streak_start
		, MAX(pickup) AS streak_end
	FROM trips_numbered
	GROUP BY
		VendorID
		, payment_type
		, row_num_trip - row_num_payment
)

SELECT
	VendorID
	, payment_type
	, streak_length
	, streak_start
	, streak_end
FROM islands
QUALIFY ROW_NUMBER() OVER (
	PARTITION BY VendorID
	ORDER BY streak_length DESC, streak_start
) = 1
ORDER BY VendorID