"""
ptid Peak-Trough-Incline-Decline algorithm

"""
import ephem
import datetime
import copy
import math

def dist(alt_a=None, az_a=None, alt_b=None, az_b=None, a=None, b=None):
	# TODO, check crossing meridian!!
	if a:
		alt_a, az_a = a
	if b:
		alt_b, az_b = b
	dist = math.sqrt((alt_a-alt_b)**2+ (az_a-alt_b)**2)
	return dist

class PtidSample(object):
	"""docstring for PtidSample"""
	def __init__(self, observatory, sat, time, target_altaz):
		super(PtidSample, self).__init__()
		tmp_time = copy.copy(observatory.date)
		observatory.date = time
		sat.compute(observatory)
		self.pt_a = (sat.alt, sat.az)
		self.dist_a_target = dist(a=self.pt_a, b=target_altaz)
		

		observatory.date = (time+datetime.timedelta(milliseconds=5))
		sat.compute(observatory)

		self.pt_b = (sat.alt, sat.az)
		self.dist_b_target = dist(a=self.pt_b, b=target_altaz)

		observatory.date = tmp_time


	def positive_slope(self):
		print(self.dist_b_target, self.dist_a_target)
		return self.dist_b_target > self.dist_a_target



def check_oribit_gt_obs_window(obs_duration_ms, sat):
	""" """
	# TODO
	return 

def get_points(observatory, sat, time, time_delta_ms):
	observatory.date = time
	sat.compute(observatory)
	pt_a = (sat.ra, sat.dec)

	observatory.date = (time+datetime.timedelta(milliseconds=time_delta_ms))
	sat.compute(observatory)



	sat.compute(observatory)
	pt_b = (sat.ra, sat.dec)

	return pt_a, pt_b


def ptid(observatory, sat, target, start_time, end_time, target_altaz):
	observatory.date = ephem.Date(start_time)
	start_sample = PtidSample(observatory, sat, start_time, target_altaz)
	print(start_sample.positive_slope())
	

