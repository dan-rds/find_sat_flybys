
'''
-------------------------------------
target_timeseries
find_sat_flybys

    TargetTimeSeries functions as a cache for the target's
    position (alt , az) so that the position doesn't need to
    be frequently recalculated.

    by Daniel Richards (github.com/dan-rds)
    Copyright 2020 Daniel Richards. All rights reserved.
--------------------------------------
'''

from pprint import pprint
import inspect
import datetime
import ephem
from observatory import Observatory

from typing import Tuple, Type


def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))


class TargetTimeSeries():
    """
    A class to find and store the target's position for a given time.
    Only calculating said position when needed
    """

    def __init__(self, observatory: Type[Observatory],
                 target_ra_dec: Tuple[float, float],
                 start_datetime: Type[datetime.datetime],
                 duration_ms: float):
        """
        TargetTimeSeries constructor
        Args:
            observarory (Observatory): Where observation is taking place
            start_datetime (datetime.datetime): start of the observation
            duration_ms: (float): how long the observation will last
            target_ra_dec (tuple): ra and dec of the target of the observation
        Returns:
            TargetTimeSeries
        """
        super().__init__()
        '''
        print("observatory  [" ,type(observatory).__name__, "]   :", observatory)
        print("target_ra_dec  [" ,type(target_ra_dec).__name__, "]   :", target_ra_dec)
        print("start_time  [" ,type(start_time).__name__, "]   :", start_time)
        print("duration_ms  [" ,type(duration_ms).__name__, "]   :", duration_ms)
        '''
        self.index_target_map = {}
        self.start_datetime = start_datetime
        self.duration_ms = int(duration_ms)
        self.observatory = observatory
        target_ra, target_dec = target_ra_dec
        target_body = ephem.FixedBody()
        target_body._ra = target_ra
        target_body._dec = target_dec
        self.target_body = target_body
        self.cache_misses = 0
        self.cache_hits = 0

    def index_to_date(self, index: int) -> datetime.datetime:
        '''
            Converts a timeseries index to a datetime object of when
            that index in the timeseries was calculated.
            e.g.
            index=1 would rturn the datetime of one second ofthe the observation started
            index=-1 would rturn the datetime of the last second of the observation

        '''
        if index < 0:
            index = self.duration_ms // 1000 + index
        after_start = datetime.timedelta(seconds=index)
        return self.start_datetime + after_start

    def get_target_aa(self, index: int) -> Tuple[Tuple[float, float], datetime.datetime]:
        '''
            Get the index-th sample in the timeseries. THis fuctions as a
            query and insert for the central cache for the timeseries.
        '''
        if index in self.index_target_map:  # cache hit
            self.cache_hits += 1
            return self.index_target_map[index], self.index_to_date(index)
        self.cache_misses += 1
        date_for_calc = self.index_to_date(index)
        self.observatory.date = date_for_calc
        self.target_body.compute(self.observatory)
        target_aa = (self.target_body.alt, self.target_body.az)
        self.index_target_map[index] = target_aa
        return target_aa, self.index_to_date(index)

    def len(self):
        ''' len() safer than an override '''
        return self.duration_ms // 1000

    def cache_hitrate(self):
        ''' Reports cache hit rates '''
        print("hits: ", self.cache_hits, "  misses: ", self.cache_misses)
