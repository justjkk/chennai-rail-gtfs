DROP TABLE IF EXISTS gtfs.calendar;

CREATE TABLE gtfs.calendar
(
		service_id	text PRIMARY KEY,
		monday	integer NOT NULL CHECK(monday IN (0,1)),
		tuesday integer NOT NULL CHECK(tuesday IN (0,1)),
		wednesday	integer NOT NULL CHECK(wednesday IN (0,1)),
		thursday	integer NOT NULL CHECK(thursday IN (0,1)),
		friday	integer NOT NULL CHECK(friday IN (0,1)),
		saturday	integer NOT NULL CHECK(saturday IN (0,1)),
		sunday	integer NOT NULL CHECK(sunday IN (0,1)),
		start_date	text NOT NULL,
		end_date	text NOT NULL
);
