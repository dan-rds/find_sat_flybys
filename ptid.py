"""
ptid Peak-Trough-Incline-Decline algorithm

"""
import ephem
import datetime
import copy

def check_oribit_gt_obs_window(obs_duration_ms, sat):
	""" """
	# TODO
	return 

def get_points(observatory, sat_tle, time, time_delta_ms):
	sat = sat_tle.copy()
	obs_a = observatory.copy()
	obs_a.date = time
	obs_b = observatory.copy()
	dt_delta = datetime.timedelta(milliseconds=time_delta_ms)
	time2 = time + dt_delta
	obs_b.date = time2

	sat.compute(obs_a)
	pt_a = (sat.ra, sat.dec)

	sat.compute(obs_b)
	pt_b = (sat.ra, sat.dec)

	return pt_a, pt_b


def ptid(observatory, sat, target, start_time, end_time):
	observatory.date = ephem.Date(start_time)
	start_pts = get_points(observatory, sat, start_time, 1) 
	print(start_pts)
	end_pts = get_points(observatory, sat, end_time, -1) 
	print(end_pts)

