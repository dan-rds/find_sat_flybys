#!/usr/bin/env python3
'''-------------------------------------
pos_calc.py
find_sat_flybys


    by Daniel Richards (github.com/dan-rds)
    Copyright 2020 Daniel Richards. All rights reserved.
--------------------------------------
'''
import datetime
# TODO use from blimpy.ephemeris import Observatory
from pprint import pprint
import inspect
import copy
import ephem
from observatory import Observatory
from target_timeseries import TargetTimeSeries
import update_tles
import ptid
from termcolor import colored


verbose = False


def verbose_conditional_print(s):
    """ The ultimate example of 'self documenting code' """
    global verbose
    if verbose:
        print(s)

def vcp(s):
    """ I'm exceptionally lazy """
    verbose_conditional_print(s)


def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))


def read_tle_file() -> dict:
    f = open("tle.txt", 'r')
    f.readline()  # comment line including date
    tles_dict = {}
    line1 = f.readline().strip()
    line2 = f.readline().strip()
    line3 = f.readline().strip()
    while line1 and line2 and line3:
        tles_dict[line1] = [line2, line3]
        line1 = f.readline().strip()
        line2 = f.readline().strip()
        line3 = f.readline().strip()

    return tles_dict

#TODO where should I put beam width??
def run(config_filename, start_time_utc,
        duration_ms, target_ra, target_dec, beam_radius, v_flag):
    global verbose
    """
    Function find if a satellite comes in between telescope and target during planned observation

    Args: (all arguments should be checked in parser)
        config_filename (str): config file name (yaml)
        start_time_utc (datetime.datetime): start of observation or target
        duration_ms (float): how long target will be observed
        target_ra (float): Right ascension of target (radians)
        target_dec float): Declination of target (radians)
        v_flag (bool): verbosity flag
    """
    verbose = v_flag
    observatory = Observatory(config_filename)
    update_tles.update_tles_if_needed()
    #start_time_utc = datetime.datetime.strptime('2020/3/12 17:37:15', "%Y/%m/%d %H:%M:%S")


    observatory.date = ephem.Date(start_time_utc)
    target_timeseries= TargetTimeSeries(observatory=observatory,  duration_ms=duration_ms,start_datetime=start_time_utc, target_ra_dec=(target_ra, target_dec))
    
    
   # end = start_time_utc + datetime.timedelta(milliseconds=10) # TODO ms=2 just for testing
    tles_dict = read_tle_file()

    flybys = []
    in_beam = []

    tmp_time = copy.copy(observatory.date)
 
    for name, tle in tles_dict.items():
        observatory.date = tmp_time
       # print(observatory.date)
        sat = ephem.readtle(name, tle[0], tle[1])
        # CAUTION with observatory times and copies
        sat.compute(observatory)

        closest_pass_dist = ptid.ptid(observatory=observatory, sat=sat, target_timeseries=target_timeseries)
        if closest_pass_dist <= observatory.beam_proximity_buffer_radians:
            if closest_pass_dist <= observatory.beam_width_radians:
                in_beam.append((sat.name, closest_pass_dist))
            else:
                flybys.append((sat.name, closest_pass_dist))

    print("Sats in beams: ", len(in_beam))
    for sat, dist in in_beam:
        print("\t", sat, "   minimum distance:",colored(dist, 'red'))
    print("Sats in proximity: ", len(flybys))
    for sat, dist in flybys:
        print("\t", sat, "   minimum distance:",colored(dist, 'yellow'))


