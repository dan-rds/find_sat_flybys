"""
ptid Peak-Trough-Incline-Decline algorithm

"""
import ephem
import datetime
import copy
import math
from math import pi

from observatory import Observatory
from pprint import pprint
import inspect

extrema = None
def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))

def distance(a_coord, b_coord, ts=None) -> float:
	a_alt, a_az = a_coord
	b_alt, b_az = b_coord

	if a_az < 0 or b_az < 0: 
		raise ValueError
	if abs(a_alt) > pi or abs(b_alt) > pi:
		raise ValueError
	az_diff = abs(a_az - b_az)
	if az_diff > pi:
		#print("WRAPPING AZMUTH")
		az_diff = (2*pi) - az_diff

	alt_diff = abs(a_alt - b_alt)

#	print(ephem.degrees(a_alt),ephem.degrees(a_az), ts)
	#return (alt_diff, az_diff)
	dist = math.sqrt(alt_diff**2 + az_diff**2)
	return dist

def is_increasing_slope(left_index, right_index, observatory, sat, target_timeseries) -> (bool, float):
	
	left_aa, left_sampletime = target_timeseries.get_target_aa_and_date(left_index)
	right_aa, right_sampletime = target_timeseries.get_target_aa_and_date(right_index)
#	print(type(left_sampletime))
	observatory.date = left_sampletime
#	print("OBS DATE: ", observatory.date)
	sat.compute(observatory)
	sat_aa = (sat.alt, sat.az)
	dist_sat_to_left_sample = distance(a_coord=sat_aa, b_coord=left_aa)

	
	observatory.date = right_sampletime
	sat.compute(observatory)
	sat_aa = (sat.alt, sat.az)
	dist_sat_to_right_sample = distance(a_coord=sat_aa, b_coord=right_aa)


	return dist_sat_to_left_sample < dist_sat_to_right_sample, min(dist_sat_to_left_sample, dist_sat_to_right_sample)


def sanity_check(observatory, sat, target_timeseries, color='b--', min_to_draw=None):
	import matplotlib.pyplot as plt
	global extrema

	dist_list = []
	tar_list = []
	sat_list = []

	start = target_timeseries.start_time
	target = target_timeseries.target_body

	dt = None
	for i in range(len(target_timeseries)):
		dt = datetime.timedelta(seconds=i)
		observatory.date = start + dt
		
		sat.compute(observatory)
		target.compute(observatory)
		sat_aa = (sat.alt, sat.az)
		
		tar_aa = (target.alt, target.az)
		d = distance(a_coord=sat_aa, b_coord=tar_aa)
		dist_list.append(d)

		sat_list.append(sat_aa)

	plt.figure()
	plt.title(sat.name)
	print(dt)


	if min_to_draw:
		print("MTD=", min_to_draw)
		plt.axhline(y=min_to_draw, color='r', linestyle='-')

	#plt.scatter(extrema_pt[0], extrema_pt[1], s=200)
	plt.plot(dist_list, color)
	plt.ylabel('Distache to target')
	plt.show()

def is_minima_index(mid_index, observatory, sat, target_timeseries) -> (bool, float):
	#todo speedup with returning slope
	left_slope, left_val = is_increasing_slope(left_index = mid_index-1, right_index=mid_index, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	right_slope, right_val = is_increasing_slope(left_index = mid_index, right_index=mid_index+1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	return (left_slope == False and right_slope == True), min(left_val, right_val)

def ptid_rec(lo, hi, observatory, sat, target_timeseries) -> float:
	global extrema

	mid_index = lo + (hi - lo)//2


	break_cond, distance = is_minima_index(mid_index, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	if break_cond or mid_index == hi or mid_index == lo:
		print("MINIMA dist = ", distance)
		extrema = mid_index

		return distance

	mid_positive_slope, val = is_increasing_slope(left_index=mid_index, right_index=mid_index+1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	if mid_positive_slope:
		rec_val =  ptid_rec(lo, mid_index, observatory, sat, target_timeseries)
	else:
		rec_val = ptid_rec(mid_index+1, hi, observatory, sat, target_timeseries) #todo rm +1??
#	print(min(rec_val, val), rec_val, val,  type(min(rec_val, val)))
	return min(rec_val, val)
def ptid(observatory, sat, target_timeseries):
	observatory = Observatory('config.yaml')

	start_positive_slope, start_min = is_increasing_slope(left_index=0, right_index=1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	end_positive_slope, end_min = is_increasing_slope(left_index = -2, right_index=-1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
# start_positive_slope, start_min = is_increasing_slope(left_index=0, right_index=1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
# 	end_positive_slope, end_min = is_increasing_slope(left_index = -2, right_index=-1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)

	peak_val = float('inf')

	if start_positive_slope == False != end_positive_slope == True:

		print("Peak" )
		peak_val = ptid_rec(0, len(target_timeseries)-1, observatory, sat, target_timeseries)
		#if peak_val < min(end_min, start_min):
		#sanity_check(observatory=observatory, sat=sat, target_timeseries=target_timeseries, min_to_draw=min(peak_val, end_min, start_min), color='g-')
	
	#sanity_check(observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	return min(peak_val, end_min, start_min)
		


