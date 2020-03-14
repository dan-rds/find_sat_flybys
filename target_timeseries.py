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
        self.time_list = [x + int(start_time.timestamp()*1000) for x in range(0, int(duration_ms))]
        self.len = len(self.time_list)

    def get_target_aa_and_date(self, index=None):
        date = self.time_list[index]
      
        if date in self.hashmap:
            return self.hashmap[date]
        self.obs.date = date
        self.target_body.compute(self.obs)
        target_aa = (self.target_body.alt, self.target_body.az)
        self.hashmap[date] = target_aa
        return target_aa, date

    def __len__(self):
        return self.len


    def get_body(self):
        return self.target_body


'''import copy
import ephem
import yaml
import pyproj
from pprint import pprint
import inspect
import datetime
from observatory import Observatory
import sys
from typing import Tuple

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
        print(start_time, )
        start = start_time.timestamp()*1000
        self.start_time = datetime.datetime.fromtimestamp(start/1000)
        print(start_time, datetime.datetime.fromtimestamp(start/1000))
        #nt(duration_ms.timestamp*1000)
        self.time_list = [x*1000 + start for x in range(0, int(duration_ms)//1000)]
      #  print("_________first index__________", datetime.datetime.fromtimestamp(self.time_list[0]/1000))
      #  print("_________last index__________", datetime.datetime.fromtimestamp(self.time_list[-1]/1000))
        self.len = len(self.time_list)//1000    
       # print(self.len)

    def get_target_aa_and_date(self, index) -> Tuple[tuple, datetime.datetime]:
      #  print("---", index, self.len, self.len - index )
        index = self.len + index if index < -1 else index
        print(index)
        date = self.time_list[index]
       # print("___________________", datetime.datetime.fromtimestamp(date/1000))
      #  exit(1)
        if date in self.hashmap:
          #  print("FOUND:  =====", datetime.datetime.fromtimestamp(date/1000))
            return self.hashmap[date], datetime.datetime.fromtimestamp(date/1000)
        print("---", datetime.datetime.fromtimestamp(date/1000))
        tmp = self.obs.date

        ts=datetime.datetime.fromtimestamp(date/1000)
       # print("Index: ",index, "   date: ", date)
        self.obs.date = ts
        self.target_body.compute(self.obs)
        target_aa = (self.target_body.alt, self.target_body.az)
        self.hashmap[date] = target_aa
        self.obs.date = tmp
        print("---ts: ", ts, "\n")
        return target_aa, ts
    def __len__(self):
        return self.len


    def get_body(self):
        return self.target_body

'''