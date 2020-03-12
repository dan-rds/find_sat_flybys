import copy
import ephem
import yaml
import pyproj
from pprint import pprint
import inspect
from observatory import Observatory
import sys

def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))

        

class TargetTimeSeries(object):
    """
    A class to find and store the target's position for a given time.
    Only calculating said position when needed
    """
    def __init__(self, observatory, target_ra_dec, start_time, duration_ms):
        """
        TargetTimeSeries constructor

        Args:
            observarory (Observatory): Where observation is taking place
            target_ra_dec (tuple): ra and dec of the target of the observation

        Returns:
            TargetTimeSeries
        """
        super().__init__()
       
        self.obs = observatory 
        self.hashmap = {}
        target_ra, target_dec = target_ra_dec 
        self.target_body = ephem.FixedBody()
        self.target_body._ra= target_ra
        self.target_body._dec = target_dec 
        self.time_list = [x + int(start_time) for x in range(0, int(duration_ms))]

    def get_target_aa(self, index=None):
        date = self.timelist[index]
      
        if date in self.hashmap:
            return self.hashmap[date]
        self.obs.date = date
        self.target_body.compute(obs)
        target_aa = (self.target_body.alt, self.target_body.az)
        self.hashmap[date] = target_aa
        return target_aa

