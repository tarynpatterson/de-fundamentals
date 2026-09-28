/*
--------------------------------------------------------------------------------
Show each trip's fare vs. the previous trip from the same vendor. For each VendorID,
show the current trip's total_amount and the previous trip's total_amount 
(ordered by pickup time). Use LAG()
--------------------------------------------------------------------------------
*/

SELECT
	VendorID
	, tpep_pickup_datetime
	, total_amount
	, LAG(total_amount) OVER (PARTITION BY VendorID ORDER BY tpep_pickup_datetime) AS previous_total_amount
FROM taxi.main.trips
ORDER BY VendorID, tpep_pickup_datetime 