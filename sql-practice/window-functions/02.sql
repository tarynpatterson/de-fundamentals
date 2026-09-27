/*
---------------------------------------------------------------------
Row number per pickup location - assign a sequential number to 
trips at each PULocationID, ordered by tpep_pickup_datetime. 
Use ROW_NUMBER().
---------------------------------------------------------------------
*/

SELECT *
FROM (
	SELECT
		PULocationID
		, tpep_pickup_datetime
		, ROW_NUMBER() OVER (PARTITION BY PULocationID ORDER BY tpep_pickup_datetime) AS trip_number
	FROM taxi.main.trips
) s
ORDER BY PULocationID, trip_number