#!/usr/bin/env python3
'''-------------------------------------
pos_calc.py
messin_with_tles


    by Daniel Richards (github.com/dan-rds)
    Copyright © 2020 Daniel Richards. All rights reserved.
-------------------------------------- 
'''
import ephem
import yaml
import time
import datetime
import pyproj
# TODO use from blimpy.ephemeris import Observatory 
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

def read_config_file(config_filename) -> ephem.Observer:
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
	return ret_obs


observatory = read_config_file('config.yaml')
tles = read_tle_file()

obs_window_ms = 720000 #TODO, not hardcoded, 12 minutes
iss_tle = tles["ISS (ZARYA)"]
iss = ephem.readtle("ISS (ZARYA)", iss_tle[0], iss_tle[1])
print(iss._n, type(iss))
t = int(time.time())

for i in range(obs_window_ms//1000):
	d = datetime.datetime.utcfromtimestamp(t+i)
	ephem_date = ephem.Date(d)
	observatory.date = ephem_date

	iss.compute(observatory)
	print(iss.ra, iss.dec)


# mean_motions = []
# for k, v in tles.items():
# 	sat = ephem.readtle(k, v[0], v[1])
# 	mean_motions.append(sat._e)
# mean_motions.sort()
# print(mean_motions)