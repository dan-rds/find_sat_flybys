'''
-------------------------------------
ptid.py
find_sat_flybys

    ptid Peak-Trough-Incline-Decline algorithm. 
    Ptid finds the basic characteristics of the polynomial 
    f(t) =: distance between target's (alt, az) and the sat's (alt, az) at time t.
    It does thi_indexs in log(n) time by sampling the the beginning and end of the polynomial to 
    determine the slope of the polynomial at those points. If the polynimoal represents a 
    trough, PTID will run the sampling recursivly until a minima is found.

    See PTID_proof.pdf for the proof

    by Daniel Richards (github.com/dan-rds)
    Copyright 2020 Daniel Richards. All rights reserved.
--------------------------------------
''' 

import datetime
import copy
import math
import inspect

import ephem
from pprint import pprint
from typing import Tuple, Type
from observatory import Observatory
from target_timeseries import TargetTimeSeries
from dev_utils import sanity_check, peek

from math import pi
import math
def distance(a_coord, b_coord) -> float:
    ''' Angular distance between two points '''
    a_alt, a_az = a_coord
    b_alt, b_az = b_coord

    if a_az < 0 or b_az < 0: # 
        raise ValueError
    if abs(a_alt) > pi or abs(b_alt) > pi: 
        raise ValueError
    az_diff = abs(a_az - b_az)
    if az_diff > pi:
        az_diff = (2 * pi) - az_diff

    alt_diff = abs(a_alt - b_alt)

    dist = math.sqrt(alt_diff**2 + az_diff**2)
    return dist
extrema_pt = None



def ptid(observatory: Type[Observatory], sat: Type[ephem.Body], target_timeseries: Type[TargetTimeSeries]):
    ''' 
    ptid Peak-Trough-Incline-Decline algorithm.
    See PTID_proof.pdf for details on the algorithm
    Args:
        observarory (Observatory): Where observation is taking place
        sat (ephem.Body): A satellite's orbital body made from tle 
        target_timeseries (TargetTimeSeries): target alt, az lookup
    Returns:
        # TODO
    '''
    extrema_pt = None # used for plotting

    def is_minima_index(mid_index: int) -> (bool, float):
        ''' Checks points to right and left of mid_index to see if it is a local minima '''

        left_slope, left_val = is_increasing_slope(left_index=mid_index - 1, right_index=mid_index)
        right_slope, right_val = is_increasing_slope(left_index=mid_index, right_index=mid_index + 1)
        found_minima = (left_slope == False and right_slope == True)
        return found_minima, min(left_val, right_val)

    def is_increasing_slope(left_index: int, right_index: int) -> Tuple[bool, float]:
        ''' 
            Calculates if slope is increasing between left_index and right_index where 
            f(t) =: distance between target's (alt, az) and the sat's (alt, az) at time t.
            See readme for details on the algorithm
            Args:
                left_index (int): First index to lookup in the timeseries 
                right_index (int): Second index to lookup in the timeseries 
            Returns:
                is_increasing (bool): If f(t) is increasing
                min_value (float): The minimum value of the two points
                
        '''
  

        left_aa, left_sampletime = target_timeseries.get_target_aa(left_index)
        right_aa, right_sampletime = target_timeseries.get_target_aa(right_index)

        observatory.date = left_sampletime

        sat.compute(observatory)
        sat_aa = (sat.alt, sat.az)
        dist_sat_to_left_sample = distance(a_coord=sat_aa, b_coord=left_aa)

        observatory.date = right_sampletime
        sat.compute(observatory)
        sat_aa = (sat.alt, sat.az)
        dist_sat_to_right_sample = distance(a_coord=sat_aa, b_coord=right_aa)

        is_increasing = dist_sat_to_left_sample < dist_sat_to_right_sample
        min_value = min(dist_sat_to_left_sample, dist_sat_to_right_sample)
        return is_increasing, min_value


    def ptid_recursive(lo_index, hi_index) -> float:
        ''' 
            Recursive part of the ptid algorithm. See Ptid_Proof.latex for more info
            Args:
                lo_index (int): The lower bound to check 
                hi_index (int): The higher bound to check 
            Returns:
                (float): minimim value of f(t)[lo_index:hi_index]
        '''
        

        mid_index = lo_index + (hi_index - lo_index) // 2

        break_cond, distance = is_minima_index(mid_index=mid_index)
        if break_cond or mid_index == hi_index or mid_index == lo_index:
            extrema_pt = (mid_index, distance)
            return distance

        mid_positive_slope, val = is_increasing_slope(left_index=mid_index, right_index=mid_index + 1)
        if mid_positive_slope:
            rec_val = ptid_recursive(lo_index, mid_index)
        else:
            rec_val = ptid_recursive(mid_index + 1,hi_index)
        return min(rec_val, val)

    #Resume PTID algorithm funcion

    start_positive_slope, start_min = is_increasing_slope(left_index=0, right_index=1)
    end_positive_slope, end_min = is_increasing_slope(left_index=-2, right_index=-1)

    peak_val = float('inf')

    if start_positive_slope == False != end_positive_slope == True:
        peak_val = ptid_recursive(0,(target_timeseries.len() - 1))
        print("Trough", sat.name, peak_val)
       # sanity_check(observatory=observatory, 
                    # sat=sat, 
                    # target_timeseries=target_timeseries, 
                    # extrema_pt=extrema_pt)
    return min(peak_val, end_min, start_min)
