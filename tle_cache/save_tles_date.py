

import ephem
import os
import time
import datetime
from math import pi

def read_tle_file(filename) -> list:
    f = open(filename, 'r')
    f.readline()  # comment line including date
    tles = []
    line1 = f.readline().strip()
    line2 = f.readline().strip()
    line3 = f.readline().strip()
    while line1 and line2 and line3:
        tles.append(ephem.readtle(line1,line2, line3))
        line1 = f.readline().strip()
        line2 = f.readline().strip()
        line3 = f.readline().strip()


    return tles



def check_tles_current(filename) -> str:
    # TODO , use package specific path
    if not os.path.exists(filename):
        return False
    f = open(filename, "r")
    first_line = f.readline()
    timestamp = float(first_line.strip().split(' ')[-1])
    d = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return str(d)
 

old_tles = read_tle_file("tle.txt.bak")
new_tles = read_tle_file("tle.txt")
target = (2.0, 2.0)
obs = ephem.Observer()
obs.lon = '-111:32.1'
obs.lat = '35:05.8'
obs.elevation = 2198
#print(ephem.Date(datetime.datetime.now()))
for old, new in zip(old_tles, new_tles):
	obs.date = ephem.Date(datetime.datetime.now())
	old.compute(obs)
	obs.date = ephem.Date(datetime.datetime.now())
	new.compute(obs)
	alt_diff = (old.alt-new.alt)
	az_diff = (old.az-new.az) 
	print(alt_diff, az_diff)


#file #1 = 1582927619.788401 2020-02-28 14:06:59




