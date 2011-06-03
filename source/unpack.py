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
        trip_id = row["Train Nos."].strip() + service_id
        if trip_id in trips:
            existing_route_id = trips[trip_id]["route_id"]
            adding_route_id = route_id
            er0, er1 = existing_route_id.split('-')
            ar0, ar1 = adding_route_id.split('-')
            both_forwards = (trips[trip_id]["direction_id"] == 0 and direction_id == 0)
            both_backwards = (trips[trip_id]["direction_id"] == 1 and direction_id == 1)
            if (er1 == ar0 and both_forwards):
                merged_route_id = er0 + '-' + ar1
            elif (er0 == ar1 and both_backwards):
                merged_route_id = ar0 + '-' + er1
            else:
                raise Exception("Failed to merge routes %s and %s - Duplicate trip id with non-merging routes" % (existing_route_id, adding_route_id))
            print "Overwriting trip %s having route id %s with route id %s" % (trip_id, existing_route_id, merged_route_id)
            stop_count = trips[trip_id]["stop_count"]
        else:
            merged_route_id = route_id
            stop_count = 0

        trips[trip_id] = {
            "route_id": merged_route_id,
            "service_id": service_id,
            "trip_id": trip_id,
            "trip_headsign": "To " + [x for x in stop_names if row[x] != ""][-1],
            "trip_short_name": row["Train Nos."],
            "direction_id": direction_id,
            "block_id": None,
            "shape_id" : None,
            "stop_count": stop_count
        }

        for stop_name in stop_names:
            trips[trip_id]["stop_count"] += 1
            if row[stop_name] == "":
                continue
            stop_time = fmttime(row[stop_name])
            stop_time_hash = trip_id + '#' + stop_name
            if stop_time_hash in stop_times:
                if stop_time != stop_times[stop_time_hash]["departure_time"]:
                    print "Overwriting stop_time of trip_id %s stop_name %s" % (trip_id, stop_name)
            stop_times[stop_time_hash] = {
                "trip_id": trip_id,
                "arrival_time": stop_time,
                "departure_time": stop_time,
                "stop_name": stop_name,
                "stop_sequence": trips[trip_id]["stop_count"]
            }

if __name__ == "__main__":
    trips = {}
    stop_times = {}

    stcols = [
        "trip_id", "arrival_time", "departure_time", "stop_name", "stop_sequence"
    ]

    tripcols = [
        "route_id", "service_id", "trip_id", "trip_headsign", "trip_short_name", "direction_id", "block_id", "shape_id"
    ]

    stcsv = csv.DictWriter(open('stoptimes2.csv', 'w'), stcols)
    stcsv.writerow(dict([(x,x) for x in stcols])) # workaround for DictWriter.writeheader() function
    tripcsv = csv.DictWriter(open('trips.csv', 'w'), tripcols, extrasaction = 'ignore')
    tripcsv.writerow(dict([(x,x) for x in tripcols]))

    # Chennai Beach - Velachery
    unpack('msb-vlcy_sun_0')
    unpack('msb-vlcy_wds_0')
    unpack('msb-vlcy_sun_1')
    unpack('msb-vlcy_wds_1')

    # Chennai Beach - Tambaram - Chengalpet - Thirumalpur
    unpack('msb-tbm_all_0')
    unpack('msb-tbm_sun_0')
    unpack('msb-tbm_wds_0')
    unpack('tbm-cgl_all_0')
    unpack('tbm-cgl_sun_0')
    unpack('tbm-cgl_wds_0')
    #FIXME: Commented some data sources here
    #unpack('cgl-tmlp_all_0')
    # --- (Reverse direction)
    #FIXME: Commented some data sources here
    #unpack('cgl-tmlp_all_1')
    unpack('tbm-cgl_all_1')
    unpack('tbm-cgl_sun_1')
    unpack('tbm-cgl_wds_1')
    unpack('msb-tbm_all_1')
    unpack('msb-tbm_sun_1')
    unpack('msb-tbm_wds_1')

    tripcsv.writerows(trips.values())
    stcsv.writerows(stop_times.values())
