
import datetime
import copy
import math
import inspect
from math import pi
import ephem
from pprint import pprint
from typing import Tuple, Type
from observatory import Observatory
from target_timeseries import TargetTimeSeries

extrema_pt = None

def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))

def sanity_check(observatory, sat, target_timeseries,
                 color='b--', min_to_draw=None, extrema_pt=None):
    ''' Function to plot f(t) '''

    import matplotlib.pyplot as plt
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

    dist_list = []
    tar_list = []
    sat_list = []

    start = target_timeseries.start_datetime
    target = target_timeseries.target_body

    dt = None
    for i in range(target_timeseries.len()):
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

    if extrema_pt:
        #    print("MTD=", min_to_draw)
        #    plt.axhline(y=min_to_draw, color='r', linestyle='-')
        plt.axhline(y=extrema_pt[1], color='b', linestyle='--')
        plt.axvline(x=extrema_pt[0], color='b', linestyle='--')
        #plt.scatter(extrema_pt[0], extrema_pt[1], s=200)
    plt.plot(dist_list, color)
    plt.ylabel('Distache to target')
    plt.show()

