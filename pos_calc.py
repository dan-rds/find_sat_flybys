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

import ptid


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

# def create_target_position_series(observatory, start_time_utc, duration_ms, target_body) -> list:
#     series = []
#     # TODO, calc better time step size
#     start = start_time_utc
#     now = observatory.date
#     print(observatory.date)
#     # start += datetime.timedelta(minutes=230) #todo rm
#     interested_keys = ['_dec','_ra','a_dec','a_epoch','a_ra','alt','az','dec','elong','neverup','ra',
#     'radius','rise_az','rise_time','set_az','set_time','transit_alt','transit_time',]
#     # TODO, calc better time step size
#     for ms in range(0, int(duration_ms)): # change back, benn fucking with the step size
#         observatory.date = start + datetime.timedelta(seconds=ms)
#       #  observatory.date = start + datetime.timedelta(seconds=ms)
#         target_body.compute(observatory)
#       #  print(target_body.alt, target_body.az, ms)
#         d = {x: target_body.__getattribute__(x) for x in interested_keys}
#         d["ts"] = observatory.date

#         series.append(d)
#     observatory.date = start_time_utc #cant be too careful
#     print(observatory.date)
#     return series

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

    #start_time_utc = datetime.datetime.strptime('2020/3/12 17:37:15', "%Y/%m/%d %H:%M:%S")

    observatory.date = ephem.Date(start_time_utc)
    target_timeseries= TargetTimeSeries(observatory=observatory,  duration_ms=duration_ms,start_time=start_time_utc, target_ra_dec=(target_ra, target_dec))
    

   # end = start_time_utc + datetime.timedelta(milliseconds=10) # TODO ms=2 just for testing
    tles_dict = read_tle_file()

   # target_body.compute(observatory)
  #  target_series = create_target_position_series(observatory, start_time_utc, duration_ms, target_body)
   # print(target_series[0])
    tmp_time = copy.copy(observatory.date)
    never_up_count = 0

    # break_count = 50
    diatances = []
    l = 0
    for name, tle in tles_dict.items():
        # if break_count == 0:
        #     break
       # print(observatory.date == tmp_time, observatory.date, tmp_time)
        observatory.date = tmp_time
        print(observatory.date)
        sat = ephem.readtle(name, tle[0], tle[1])
        # CAUTION with observatory times and copies
        sat.compute(observatory)

        sat_ever_rises = False
        # try:  # Don't add satellites that are never up
            #o = observatory.copy()
           # print(observatory.date)
         #   start_val = observatory.next_pass(sat)
          #  print(start_val)
            
        closest_pass_dist = ptid.ptid(observatory=observatory, sat=sat, target_timeseries=target_timeseries)
        #     l += 1
        #     print(sat)
        #     diatances.append(closest_pass_dist)
        # except ValueError:
        #     never_up_count += 1

        
   # print(diatances)
    print(l, never_up_count)

