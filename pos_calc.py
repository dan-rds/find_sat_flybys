#!/usr/bin/env python3
'''-------------------------------------
pos_calc.py
messin_with_tles


    by Daniel Richards (github.com/dan-rds)
    Copyright 2020 Daniel Richards. All rights reserved.
--------------------------------------
'''
import datetime
# TODO use from blimpy.ephemeris import Observatory
from pprint import pprint
import inspect
import ephem
from observatory import Observatory

import ptid


verbose = False


def verbose_conditional_print(s):
    """ The ultimate example of 'self documenting code' """
    global verbose
    if verbose:
        print(s)


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




def run(config_filename, start_time_utc,
        duration_ms, target_ra, target_dec, v_flag):
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
    verbose_conditional_print(observatory)
    peek(observatory)
    target = (target_ra, target_dec)

    observatory.date = ephem.Date(start_time_utc)

    #end = start_time_utc + datetime.timedelta(milliseconds=duration_ms)
    end = start_time_utc + datetime.timedelta(milliseconds=2)
    tles_dict = read_tle_file()
    # tles_to_search = []
    never_up_count = 0
    #means = []

    for name, tle in tles_dict.items():
        sat = ephem.readtle(name, tle[0], tle[1])
        # CAUTION with observatory times and copies
        sat.compute(observatory)

        sat_ever_rises = False
        try:  # Don't add satellites that are never up
            start_val = observatory.next_pass(sat)
            ptid.ptid(observatory, sat, target, start_time_utc, end)
            #m=calc_min_dist_to_beam_in_window(start_time_utc, end, sat, observatory, target)
        except ValueError:
            never_up_count += 1
        break

    print(never_up_count, " of the ", len(tles),
          " satellites never come into view")
