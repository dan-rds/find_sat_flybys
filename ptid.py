"""
ptid Peak-Trough-Incline-Decline algorithm

"""
import ephem
import datetime
import copy
import math
from math import pi
from pprint import pprint
import inspect
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
		print("WRAPPING AZMUTH")
		az_diff = (2*pi) - az_diff

	alt_diff = abs(a_alt - b_alt)
	#peek(ts)

	print(ephem.degrees(a_alt),ephem.degrees(a_az), ts)
	#return (alt_diff, az_diff)
	dist = math.sqrt(alt_diff**2 + az_diff**2)
	return dist

def is_increasing_slope(left_index, right_index, observer, sat, target_timeseries):
	# put under ptid?
	# TODO, check if precalcing sat is faster? shouldnt be tho
	left_sample = right_sample = None
	try:
		left_sample = target_timeseries[left_index]
		right_sample = target_timeseries[right_index]

	except ValueError:
		print("Bad indexes: ", left_index, right_index)
		raise ValueError("ValueError exception thrown")
	
	tmp_time = observer.date
	
	left_time = left_sample['ts']
	observer.time = left_time
	sat.compute(observer)
	sat_aa = (sat.alt, sat.az)
	left_aa = (left_sample['alt'],left_sample['az'])
	dist_sat_to_left_sample = distance(a_coord=sat_aa, b_coord=left_aa)

	
	right_time = right_sample['ts']
	observer.time = right_time
	sat.compute(observer)
	sat_aa = (sat.alt, sat.az)
	right_aa = (right_sample['alt'],right_sample['az'])
	dist_sat_to_right_sample = distance(a_coord=sat_aa, b_coord=right_aa)

	observer.date = tmp_time 
	#print(dist_sat_to_left_sample, dist_sat_to_right_sample)
	return dist_sat_to_left_sample < dist_sat_to_right_sample
def sanity_check(observer, sat, target_body, target_timeseries):
	import matplotlib.pyplot as plt

	dist_list = []
	tar_list = []
	sat_list = []


	m_alt = float("-inf")
	m_az = 0
	for target in target_timeseries:
		
		# print(t)
		observer.date = target['ts']
		
		sat.compute(observer)
		sat_aa = (sat.alt, sat.az)
		if sat_aa[1] > ephem.degrees(math.pi):
			sat_aa = (sat.alt, ephem.degrees(2*math.pi) -sat.az )
		m_alt = min(m_alt, sat_aa[0])
		m_az = max(m_az, sat_aa[1])
		# print(observer.date, sat.az, sat.alt, sat.range)
	
		#tar_aa = (target['alt'],target['az'])
		tar_aa = (3,3)
		d = distance(a_coord=sat_aa, b_coord=tar_aa, ts=target['ts'])
		dist_list.append(d)
		# tar_list.append(tar_aa)
		sat_list.append(sat_aa)
	#	dist_list.append(math.sqrt(sat_aa[0]**2 + sat_aa[1]**2))

		# if dt > 3:
		# 	return

	print("max alt: ",m_alt, "   max az: ",m_az)
	scale = 1
	#plt.plot(dist_list, 'bo')
	plt.figure()
	plt.subplot(211)
	plt.plot([x[1] for x in sat_list], [x[0] for x in sat_list], 'r--')#, [x[0] for x in tar_list], [x[1] for x in tar_list], 'k-' )
	plt.subplot(212)
	plt.plot(dist_list, 'b-')
	plt.ylabel('sanity??')
	plt.show()

def ptid(observatory, sat, target_body, target_timeseries):

	

	#start_positive_slope = is_increasing_slope(left_index = 0, right_index=1, observer=observatory, sat=sat, target_timeseries=target_timeseries)
	#end_positive_slope = is_increasing_slope(left_index = -1, right_index=-2, observer=observatory, sat=sat, target_timeseries=target_timeseries)

	#print(start_positive_slope, end_positive_slope)
	#if start_positive_slope == end_positive_slope:
	sanity_check(observatory, sat, target_body, target_timeseries)

