/*
--------------------------------------------------------------------------------
Show trip's fare vs. the next trip from the same vendor. Use LEAD().
--------------------------------------------------------------------------------
*/

SELECT
	VendorID
	, tpep_pickup_datetime
	, total_amount
	, LEAD(total_amount) OVER (PARTITION BY VendorID ORDER BY tpep_pickup_datetime) AS next_total_amount
FROM taxi.main.trips
ORDER BY VendorID, tpep_pickup_datetime