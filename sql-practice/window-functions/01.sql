/*
---------------------------------------------------------------------
Rank trips by fare within each vendor - for each VendorID, 
rank all trips by total_amount descending. Use RANK()
---------------------------------------------------------------------
*/

SELECT *
FROM (
	SELECT
		VendorID
		, total_amount
		, RANK() OVER (PARTITION BY VendorID ORDER BY total_amount DESC) AS trip_rank
	FROM taxi.main.trips
) s
ORDER BY VendorID, trip_rank