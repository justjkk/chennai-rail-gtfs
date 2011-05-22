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
    """
    timestr = str(uftime)
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
    return "%02d:%02d:00" % (hour, minute)

def unpack(filename):
    """
    Unpack Stop x Train Time matrix into Relational table format
    input: service id, train number, stop time matrix...
    output: trip id, service id, trip short name, stop name, time, sequence
    """

    incsv = csv.DictReader(open(filename + '.csv', 'r'))

    outcols = [
        "trip_id", "service_id", "trip_short_name",
        "stop_name", "time", "sequence"
    ]

    outcsv = csv.DictWriter(open(filename + '_unpacked.csv', 'w'), outcols)
    outcsv.writerow(dict([(x,x) for x in outcols])) # workaround for DictWriter.writeheader() function

    for trip in incsv:
        sequence = 1
        stop_names = list(set(trip.iterkeys()) - set(["Train Nos.", "Service Id"]))
        for stop_name in sorted(stop_names, key=lambda x: fmttime(trip[x])):
            outcsv.writerows([{
                "trip_id":trip["Train Nos."] + trip["Service Id"],
                "service_id":trip["Service Id"],
                "trip_short_name": trip["Train Nos."],
                "stop_name": stop_name,
                "sequence": sequence,
                "time": fmttime(trip[stop_name])
            }])
            sequence += 1

if __name__ == "__main__":
    unpack('mrts_sun_bvl')
    unpack('mrts_sun_vlb')
    unpack('mrts_wds_bvl')
    unpack('mrts_wds_vlb')
