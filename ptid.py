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
	# put under ptid?
	# TODO, check if precalcing sat is faster? shouldnt be tho
	left_sample = right_sample = None
	try:
		left_sample = target_timeseries[left_index]
		right_sample = target_timeseries[right_index]
	except ValueError:
		print("Bad indexes: ", left_index, right_index)
		raise ValueError("ValueError exception thrown")
		return

	
	left_time = left_sample['ts']
	observatory.date = left_time
	sat.compute(observatory)
	sat_aa = (sat.alt, sat.az)
	left_aa = (left_sample['alt'],left_sample['az'])

	dist_sat_to_left_sample = distance(a_coord=sat_aa, b_coord=left_aa)

	
	right_time = right_sample['ts']
	observatory.date = right_time
	sat.compute(observatory)
	sat_aa = (sat.alt, sat.az)
	right_aa = (right_sample['alt'],right_sample['az'])
	dist_sat_to_right_sample = distance(a_coord=sat_aa, b_coord=right_aa)
 
	
	return dist_sat_to_left_sample < dist_sat_to_right_sample, min(dist_sat_to_left_sample, dist_sat_to_right_sample)


def sanity_check(observatory, sat, target_body, target_timeseries, color='b--', min_to_draw=None):
	import matplotlib.pyplot as plt
	global extrema

	dist_list = []
	tar_list = []
	sat_list = []

	extrema_pt = (extrema, 0.3)
	for index, target in enumerate(target_timeseries):
		observatory.date = target['ts']
		
		sat.compute(observatory)
		sat_aa = (sat.alt, sat.az)
		
		tar_aa = (target['alt'], target['az'])
		d = distance(a_coord=sat_aa, b_coord=tar_aa, ts=target['ts'])
		dist_list.append(d)
		if index == extrema:
			extrema_pt = (index,d)
		sat_list.append(sat_aa)

	plt.figure()
	plt.title(sat.name)
	plt.subplot(211)
	plt.ylabel('Sat alt, az')
	plt.plot([x[1] for x in sat_list], [x[0] for x in sat_list], 'r--')#, [x[0] for x in tar_list], [x[1] for x in tar_list], 'k-' )

	plt.subplot(212)
	if min_to_draw:
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
	# if mid_index == hi or mid_index == lo:
	# 	print(lo, mid_index, hi, "_________________ shouldnt happen")
	# 	extrema = mid_index
	# 	return 

	break_cond, distance = is_minima_index(mid_index, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	if break_cond or mid_index == hi or mid_index == lo:
#		print("MINIMA INDEX = ", mid_index)
		extrema = mid_index

		return distance

	mid_positive_slope, val = is_increasing_slope(left_index=mid_index, right_index=mid_index+1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	if mid_positive_slope:
		rec_val =  ptid_rec(lo, mid_index, observatory, sat, target_timeseries)
	else:
		rec_val = ptid_rec(mid_index+1, hi, observatory, sat, target_timeseries) #todo rm +1??
#	print(min(rec_val, val), rec_val, val,  type(min(rec_val, val)))
	return min(rec_val, val)
def ptid(observatory, sat, target_body, target_timeseries):

	start_positive_slope, start_min = is_increasing_slope(left_index=0, right_index=1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	end_positive_slope, end_min = is_increasing_slope(left_index = -2, right_index=-1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)

	peak_val = float('inf')
	
	# if start_positive_slope == True != end_positive_slope == False:
	# 	print("Trough")

	if start_positive_slope == False != end_positive_slope == True:
		#	print("Peak" )
			peak_val = ptid_rec(0, len(target_timeseries)-1, observatory, sat, target_timeseries)

	# else:
	# 	if start_positive_slope == False != end_positive_slope == True:
	# 		print("Peak" )
	# 		peak_val = ptid_rec(0, len(target_timeseries)-1, observatory, sat, target_timeseries)

	# 		#sanity_check(observatory, sat, target_body, target_timeseries, color='r-')
	# 		#sanity_check(observatory, sat, target_body, target_timeseries, color='r-')
	# 	elif start_positive_slope == True != end_positive_slope == True:
	# 		print("Incline" )
	# 		#sanity_check(observatory, sat, target_body, target_timeseries, color='b-')
	# 	else :
	# 		print("Decline" )
	# if peak_val == None or peak_val < 1000000:
	# 	print("start_min  [" ,type(start_min).__name__, "]   :", start_min)
	# 	print("end_min  [" ,type(end_min).__name__, "]   :", end_min)
	# 	print("peak_val  [" ,type(peak_val).__name__, "]   :", peak_val)
	# 	print(min_dist)
	# 	sanity_check(observatory, sat, target_body, target_timeseries, color='b-', min_to_draw=min_dist)
	
	return min(peak_val, end_min, start_min)
		


