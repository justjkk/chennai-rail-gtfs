#!/usr/bin/env python

import csv
import sys

def fmttime(uftime):
    """
    >>> fmttime(10.2)
    '10:20:00'
    >>> fmttime(7.23)
    '07:23:00'
    >>> fmttime("10.2")
    '10:20:00'
    >>> fmttime("07:23")
    '07:23:00'
    >>> fmttime("8")
    '08:00:00'

    To avoid Time travels, time less than 3AM are considered second day's
    >>> fmttime("0:54")
    '24:54:00'
    >>> fmttime("2.59")
    '26:59:00'
    """
    timestr = str(uftime)
    try:
        if ":" in timestr:
            hour, minute = [int(x) for x in timestr.split(":")]
        elif "." in timestr:
            hour, minute = timestr.split(".")
            hour = int(hour)
            if len(minute) == 1:
                minute = int(minute) * 10
            else:
                minute = int(minute)
        else:
            hour, minute = (int(timestr), 0)
    except Exception, e:
        sys.stderr.write("Unrecognised time format: '%s'\n" % timestr)
        sys.stderr.write("Error was: '%s'\n" % e)
        raise
    if hour < 3:
        hour += 24
    return "%02d:%02d:00" % (hour, minute)

def unpack(filename):
    """
    Unpack [ Stop name x Trip short name ] Timetable into Relational table format
    Output: trip csv and stop_times csv
    """

    with open(filename + '.csv', 'r') as f:
        fr = csv.reader(f)
        for row in fr:
            stop_names = [x for x in row[1:] if x != None and x != ""]
            break

    incsv = csv.DictReader(open(filename + '.csv', 'r'))

    route_id, service_id, direction_id  = filename.split('.')[0].split('_') #Eg: filename = 'msb-vlcy_sun_0'
    route_id = route_id.upper()
    service_id = service_id.upper()
    direction_id = int(direction_id)

    for row in incsv:
        trips.append({
            "route_id": route_id,
            "service_id": service_id,
            "trip_id": row["Train Nos."] + service_id,
            "trip_headsign": "To " + [x for x in stop_names if row[x] != ""][-1],
            "trip_short_name": row["Train Nos."],
            "direction_id": direction_id,
            "block_id": None,
            "shape_id" : None
        })

        sequence = 0
        for stop_name in stop_names:
            sequence += 1
            if row[stop_name] == "":
                continue
            stop_times.append({
                "trip_id": row["Train Nos."] + service_id,
                "arrival_time": fmttime(row[stop_name]),
                "departure_time": fmttime(row[stop_name]),
                "stop_name": stop_name,
                "stop_sequence": sequence
            })

if __name__ == "__main__":
    trips = []
    stop_times = []

    stcols = [
        "trip_id", "arrival_time", "departure_time", "stop_name", "stop_sequence"
    ]

    tripcols = [
        "route_id", "service_id", "trip_id", "trip_headsign", "trip_short_name", "direction_id", "block_id", "shape_id"
    ]

    stcsv = csv.DictWriter(open('stoptimes2.csv', 'w'), stcols)
    stcsv.writerow(dict([(x,x) for x in stcols])) # workaround for DictWriter.writeheader() function
    tripcsv = csv.DictWriter(open('trips.csv', 'w'), tripcols)
    tripcsv.writerow(dict([(x,x) for x in tripcols]))
    unpack('msb-vlcy_sun_0')
    unpack('msb-vlcy_sun_1')
    unpack('msb-vlcy_wds_0')
    unpack('msb-vlcy_wds_1')
    unpack('msb-tbm_sun_0')
    unpack('msb-tbm_sun_1')
    unpack('msb-tbm_wds_0')
    unpack('msb-tbm_wds_1')
    tripcsv.writerows(trips)
    stcsv.writerows(stop_times)
