CREATE TEMPORARY TABLE stop_times2
(
		trip_id	text NOT NULL,
		arrival_time	gtfstime NOT NULL,
		departure_time	gtfstime NOT NULL,
		stop_name	text NOT NULL, 
		stop_sequence	integer NOT NULL
);

DELETE FROM gtfs.stop_times;
DELETE FROM gtfs.trips;

\copy gtfs.trips FROM 'trips.csv' WITH CSV HEADER

\copy stop_times2 FROM 'stoptimes2.csv' WITH CSV HEADER

INSERT INTO gtfs.stop_times(trip_id, arrival_time, departure_time, stop_id, stop_sequence)
SELECT st.trip_id, st.arrival_time, st.departure_time, s.stop_id, st.stop_sequence FROM stop_times2 st, gtfs.stops s where st.stop_name = s.stop_name;
