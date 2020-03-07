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

def kludge_ra_to_aa(observatory, target):
    ra, dec = target
    from astropy.coordinates import EarthLocation,SkyCoord
    from astropy.time import Time
    from astropy import units as u
    from astropy.coordinates import AltAz

    observing_location = EarthLocation(lat=str(observatory.lat), lon=str(observatory.lon), height=observatory.elevation)
    observing_time = Time(datetime.datetime.now())  
    aa = AltAz(location=observing_location, obstime=observing_time)

    coord = SkyCoord(ra=ra, dec=dec,  unit=(u.radian, u.radian))
    coord.transform_to(aa)
    
    return coord


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

    # start_time_utc = datetime.datetime.fromtimestamp(1583555291.286727)
    verbose = v_flag
    observatory = Observatory(config_filename)
    verbose_conditional_print(observatory)

    target = (target_ra, target_dec) # TODO convert to azalt
    target_body = ephem.FixedBody()
    target_body._ra= target_ra
    target_body._dec = target_dec 
    

    observatory.date = ephem.Date(start_time_utc)
    print(ephem.Date(start_time_utc), "_________________________________")
    #end = start_time_utc + datetime.timedelta(milliseconds=duration_ms)
    end = start_time_utc + datetime.timedelta(milliseconds=10) # TODO ms=2 just for testing
    tles_dict = read_tle_file()
    # tles_to_search = []
    target_body.compute(observatory)
    peek(target_body)
    never_up_count = 0
    #means = []

    for name, tle in tles_dict.items():
        sat = ephem.readtle(name, tle[0], tle[1])
        # CAUTION with observatory times and copies
        sat.compute(observatory)

        sat_ever_rises = False
        try:  # Don't add satellites that are never up
            start_val = observatory.next_pass(sat)
            ptid.ptid(observatory, sat, target, start_time_utc, end, target_aa)
        except ValueError:
            never_up_count += 1
        break

    #print(never_up_count, " of the ", len(tles),
     #     " satellites never come into view")
