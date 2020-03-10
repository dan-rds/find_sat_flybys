#Distance between alt az coords

import ephem
import math
from math import pi

def distance(a_coord, b_coord) -> float:
	# Don't adjust az

	a_alt, a_az = a_coord
	b_alt, b_az = b_coord

	if a_az < 0 or b_az < 0:
		raise ValueError
	if abs(a_alt) > pi or abs(b_alt) > pi:
		raise ValueError
	az_diff = abs(a_az - b_az)
	if az_diff > pi:
		az_diff = (2*pi) - az_diff

	alt_diff = abs(a_alt - b_alt)

	print(ephem.degrees(alt_diff),ephem.degrees(az_diff) )
	#return (alt_diff, az_diff)
	dist = math.sqrt(alt_diff**2 + az_diff**2)
	return dist

a = (3, 3)
b = (pi, pi)

print(distance(a,b))