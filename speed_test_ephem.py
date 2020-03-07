#!/usr/bin/env python3
'''-------------------------------------
speed_test_ephem.py
messin_with_tles


    by Daniel Richards (github.com/dan-rds)
    Copyright © 2020 Daniel Richards. All rights reserved.
-------------------------------------- 
'''
import ephem
import datetime
import math
import time

tle_str = ["CALSPHERE 4A","1 01520U 65065H   20058.86916325  .00000035  00000-0  49354-4 0  9992","2 01520  90.0403 128.7439 0072289 113.7399 336.8322 13.35807489655439"]
sat = ephem.readtle(tle_str[0], tle_str[1], tle_str[2])
target = (2.0, 2.0)
obs = ephem.Observer()
obs.lon = '-111:32.1'
obs.lat = '35:05.8'
obs.elevation = 2198
d = datetime.datetime.now()
dt = datetime.timedelta(seconds=1)
l = []
t = time.time()
for i in range(0, 100000):
	obs.date = d
	sat.compute(obs)
	az = sat.az
	alt = sat.alt

	az_ang = ephem.degrees(az-target[1])
	alt_ang = ephem.degrees(alt-target[0])


	dist = math.sqrt(alt_ang**2+ az_ang**2) 
	l.append(dist)
		#print(dist)

	# if i == 0:
	# 	dist = math.sqrt((alt-target[0])**2+ (az-target[1])**2) # 3.912561706231643
	# 	print(dist)
	d = d + dt
t = time.time()-t
#print(l)
print(t)

# manual(x100000) = 0.7041010856628418, 0.7246699333190918