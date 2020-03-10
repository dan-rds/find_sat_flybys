
import os
import requests
import time
import pycurl
from io import BytesIO 

def update_tles():
    # TODO , use package specific path
    file=open("tle.txt", 'w+')
    file.write("# Last updated: %s\n"%(time.time()))

    b_obj = BytesIO() 
    crl = pycurl.Curl() 

    # Set URL value
    crl.setopt(crl.URL, 'https://celestrak.com/NORAD/elements/active.txt')
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()
    file.write(get_body.decode('utf8')) 


def check_tles_current() -> bool:
    # TODO , use package specific path
    if not os.path.exists("tle.txt"):
        return False
    f = open("tle.txt", "r")
    first_line = f.readline()
    timestamp = float(first_line.strip().split(' ')[-1])
    sec_per_day = 86400
    now = float(time.time())
    if (now - timestamp) > sec_per_day: # if tles are more than a day old, update
        return False
    return True

def update_tles_if_needed():
    if not check_tles_current():
        update_tles
   
if __name__ == '__main__':
    update_tles_if_needed()