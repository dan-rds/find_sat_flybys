import ephem
import datetime
from pprint import pprint
import inspect

from observatory import Observatory

def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))

gatech = Observatory("config.yaml")
time = datetime.datetime.now()
gatech.date = time

a = 'ISS (ZARYA)'            
b = '1 25544U 98067A   20059.70568385  .00000674  00000-0  20303-4 0  9997'
c = '2 25544  51.6445 170.1681 0005128 328.4727 174.8122 15.49202061215047'

iss = ephem.readtle(a, b, c)
iss.compute(gatech)
iss_aa = (iss.alt, iss.az)
# peek(iss)
# n  = gatech.next_pass(iss)
# n  = gatech.next_rising(iss)
time += datetime.timedelta(minutes=1)
gatech.date = time

iss.compute(gatech)
iss_second_aa = (iss.alt, iss.az)

print(iss_aa, iss_second_aa, iss_aa == iss_second_aa)
