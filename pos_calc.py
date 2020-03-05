#!/usr/bin/env python3
'''-------------------------------------
pos_calc.py
messin_with_tles


    by Daniel Richards (github.com/dan-rds)
    Copyright 2020 Daniel Richards. All rights reserved.
-------------------------------------- 
'''
import ephem
import yaml
import time
import datetime
import pyproj
import math


# TODO use from blimpy.ephemeris import Observatory 

from pprint import pprint
import inspect

def peek(x):
	pprint(inspect.getmembers(x))


def read_tle_file() -> dict:
	f = open("tle.txt", 'r')
	f.readline() #comment line including date
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

def read_config_file(config_filename) -> (ephem.Observer, dict):
	d = {}
	with open(config_filename, "r+") as config:
		d = dict(yaml.safe_load(config))
	# converting xyz -> lla
	ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
	lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
	lon, lat, alt = pyproj.transform(ecef, lla, d['x'], d['y'], d['z'], radians=True) # Yes it returs lon, lat not la, lon
	ret_obs = ephem.Observer()
	ret_obs.lat = lat
	ret_obs.lon = lon
	ret_obs.elevation = alt

	d[lon] = lon
	d[lat] = lat
	d[alt] = alt
	return ret_obs, d

def calc_ms_to_transit_beam(observatory, obs_settings, sat_tle):

	# peek(sat_tle)
	t = datetime.datetime.utcnow()
	observatory.date  = ephem.Date(t)
	sat_tle.compute(observatory)

	ra1 = sat_tle.ra
	dec1 = sat_tle.dec
	range1 = sat_tle.range

	t = t + datetime.timedelta(0,1) # adding one ms
	observatory.date  = ephem.Date(t)
	sat_tle.compute(observatory)

	ra2 = sat_tle.ra
	dec2 = sat_tle.dec
	range2 = sat_tle.range

	ra_delta = ra1-ra2
	dec_delta = dec1-dec2

	angular_speed_radians = math.sqrt(ra_delta**2+dec_delta**2) 
	
	degrees_per_ms = angular_speed_radians*180/math.pi
	arcmin_per_ms = degrees*60
	return arcmin_per_ms

def calc_min_dist_to_beam_in_window(start_date, end_date, sat, observatory, obs_settings) -> (float, datetime.datetime):
	obs = observatory.copy()
	t = start_date
	dt = datetime.timedelta(seconds=1) 
	min_dist = (float("inf"), None)
	# try:
	# 	sat.compute(observatory)
	# 	end_date = min(end_date, observatory.next_setting())
	# except ValueError
	while t < end_date:
		observatory.date = t
		sat.compute(observatory)
		
		sat_ra = sat.ra
		sat_dec = sat.dec


		target_ra = obs_settings['target_ra']
		target_dec= obs_settings['target_dec']

		ra_diff = sat_ra - target_ra
		dec_diff = sat_dec - target_dec
		#print(ra_diff, dec_diff, type(ra_diff))
		angular_dist = math.sqrt(ra_diff**2+dec_diff**2)
	
		min_dist = (angular_dist, t) if angular_dist < min_dist[0] else min_dist

		t = t+dt
	return min_dist






def run(config_filename, start_time_utc, duration_ms, target_ra, target_dec, verbose):
	observatory, settings_dict = read_config_file(config_filename)
	print(config_filename, start_time_utc, duration_ms, target_ra, target_dec, verbose)

	settings_dict['target_ra'] = target_ra
	settings_dict['target_dec'] = target_dec


	# peek(observatory)
	
	observatory.date =  ephem.Date(start_time_utc)

	end = start_time_utc + datetime.timedelta(milliseconds=duration_ms) 
	#calc_min_dist_to_beam_in_window(d, end, iss, observatory, settings_dict)
	tles = read_tle_file()


	tles_to_search = []
	never_up_count = 0
	means = []
	i = 0
	for name, tle in tles.items():
		sat = ephem.readtle(name, tle[0], tle[1])
		sat.compute(observatory)
		i  += 1
		if not i%100:
			print(i)
		

		try: # Don't add satellites that are never up 
			start_val = observatory.next_pass(sat)
			#print(datetime.datetime.(start_val[0]))
			min_dist  = calc_min_dist_to_beam_in_window(start_time_utc, end, sat, observatory, settings_dict)
			means.append(min_dist)
			# tles_to_search.append(sat)
		except ValueError:
			never_up_count += 1
			
	print(never_up_count, " of the ", len(tles), " satellites never come into view")
	means.sort(key = lambda x: x[0])
	print(means)


# print(mean_motions)