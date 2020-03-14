import copy
import ephem
import yaml
import pyproj
from pprint import pprint
import inspect
from observatory import Observatory
import sys
import datetime
from typing import Tuple, List, Type
def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))

        

class TargetTimeSeries(object):
    """
    A class to find and store the target's position for a given time.
    Only calculating said position when needed
    """
    def __init__(self, observatory: Type[Observatory], target_ra_dec: Tuple[float,float], start_datetime: Type[datetime.datetime], duration_ms: float):
        """
        TargetTimeSeries constructor
        Args:
            observarory (Observatory): Where observation is taking place
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
        target_body._ra= target_ra
        target_body._dec = target_dec 
        self.target_body = target_body
        self.cache_misses = 0
        self.cache_hits = 0

    def index_to_date(self, index) -> datetime.datetime:
        #every second for now
        if index < 0:
        #    tmp = index
            index = self.duration_ms//1000 + index
        #    print("old index: ", tmp, "   new index: ", index)
        after_start = datetime.timedelta(seconds=index)
        return self.start_datetime + after_start

    def get_target_aa(self, index: int) -> Tuple[Tuple[float, float], datetime.datetime]:
        if index in self.index_target_map:
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
        return self.duration_ms//1000

    def cache_hitrate(self):
        print("hits: ", self.cache_hits,"  misses: ", self.cache_misses)
















