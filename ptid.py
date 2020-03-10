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
def slope_check(observatory, sat, target_timeseries):
	# put under ptid?
	# TODO, check if precalcing sat is faster? shouldnt be tho
	observatory = observatory

	# left_sample = target_timeseries[0]
	# right_sample = target_timeseries[-1]
	
	time = datetime.datetime.now()#left_sample['ts']
	observatory.date = time
	sat.compute(observatory)
	tmp_time = observatory.date
	sat_bb = (sat.alt, sat.az)

	tmp = copy.copy(sat_bb)


	#dist_sat_to_left_sample = distance(a_coord=sat_aa, b_coord=(0,0))
	#obs = observatory.copy()
	#obs = Observatory('config.yaml')
	time += datetime.timedelta(minutes=20)#right_sample['ts']
	observatory.date= time

	sat.compute(observatory)
	sat_aa = (sat.alt, sat.az)
	#dist_sat_to_right_sample = distance(a_coord=sat_aa, b_coord=(0,0))
	print(time)
	print(tmp,sat_aa, sat_aa==tmp , "<-----")
	print(tmp_time, observatory.date, tmp_time == time)
	#print(dist_sat_to_left_sample, dist_sat_to_right_sample, dist_sat_to_right_sample-dist_sat_to_left_sample,dist_sat_to_left_sample < dist_sat_to_right_sample)
	return "xyz"
def is_increasing_slope(left_index, right_index, observatory, sat, target_timeseries):
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
 
	#print(left_sample['ts'], right_sample['ts'])
	#print(dist_sat_to_left_sample, dist_sat_to_right_sample, dist_sat_to_right_sample-dist_sat_to_left_sample,dist_sat_to_left_sample < dist_sat_to_right_sample)
	return dist_sat_to_left_sample < dist_sat_to_right_sample
def sanity_check(observatory, sat, target_body, target_timeseries, color='b--'):
	import matplotlib.pyplot as plt

	dist_list = []
	tar_list = []
	sat_list = []


	for target in target_timeseries:
		observatory.date = target['ts']
		
		sat.compute(observatory)
		sat_aa = (sat.alt, sat.az)
		
		tar_aa = (target['alt'], target['az'])
		d = distance(a_coord=sat_aa, b_coord=tar_aa, ts=target['ts'])
		dist_list.append(d)
		sat_list.append(sat_aa)

	plt.figure()
	plt.title(sat.name)
	plt.subplot(211)
	plt.ylabel('Sat alt, az')
	plt.plot([x[1] for x in sat_list], [x[0] for x in sat_list], 'r--')#, [x[0] for x in tar_list], [x[1] for x in tar_list], 'k-' )
	plt.subplot(212)
	plt.plot(dist_list, color)
	plt.ylabel('Distache to target')
	plt.show()

def ptid(observatory, sat, target_body, target_timeseries):


	start_positive_slope = is_increasing_slope( left_index=0, right_index=1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)
	end_positive_slope = is_increasing_slope(left_index = -2, right_index=-1, observatory=observatory, sat=sat, target_timeseries=target_timeseries)

	# #print(start_positive_slope, end_positive_slope)
	# if start_positive_slope != end_positive_slope:
	# 	print(start_positive_slope, end_positive_slope)
	# 	sanity_check(observatory, sat, target_body, target_timeseries)
	# 	#print(start_positive_slope, end_positive_slope)
	
	if start_positive_slope == True != end_positive_slope == False:
		print("Trough")
		sanity_check(observatory, sat, target_body, target_timeseries, color='g-')

	else:
		if start_positive_slope == False != end_positive_slope == True:
			print("Peak" )
			sanity_check(observatory, sat, target_body, target_timeseries, color='r-')
		elif start_positive_slope == True != end_positive_slope == True:
			print("Incline" )
			sanity_check(observatory, sat, target_body, target_timeseries, color='b-')
		else :
			print("Decline" )
			sanity_check(observatory, sat, target_body, target_timeseries, color='b-')


