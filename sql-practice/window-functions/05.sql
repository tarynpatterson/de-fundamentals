/*
--------------------------------------------------------------------------------
Running total of fares per vendor, ordered by pickup time - cumulative sum of
total_amount per VendorID. Use SUM() OVER (... ORDER BY ...).

--------------------------------------------------------------------------------
*/

SELECT
	VendorID
	, tpep_pickup_datetime
	, total_amount
	, SUM(total_amount) OVER (
		PARTITION BY VendorID 
		ORDER BY tpep_pickup_datetime
		ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total_amount
FROM taxi.main.trips
ORDER BY VendorID, tpep_pickup_datetime
