DROP TABLE IF EXISTS traintimings;

CREATE TABLE traintimings
(
	trip_id	text NOT NULL,
	service_id	text NOT NULL,
	trip_short_name	text NULL,
	stop_name	text NOT NULL,
	departure_time	gtfstime	NOT NULL,
	sequence	integer NOT NULL
);

\copy traintimings from 'mrts_sun_bvl_unpacked.csv' with csv header
\copy traintimings from 'mrts_sun_vlb_unpacked.csv' with csv header
\copy traintimings from 'mrts_wds_bvl_unpacked.csv' with csv header
\copy traintimings from 'mrts_wds_vlb_unpacked.csv' with csv header

ALTER TABLE traintimings ADD COLUMN direction_id	integer;
ALTER TABLE traintimings ADD COLUMN trip_headsign	text;

UPDATE traintimings SET direction_id = 1, trip_headsign = 'Towards Chennai Beach' where trip_id like 'VLB%';

UPDATE traintimings SET direction_id = 0, trip_headsign = 'Towards Velachery' where trip_id like 'BVL%';
