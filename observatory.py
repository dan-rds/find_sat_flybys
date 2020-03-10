import copy
import ephem
import yaml
import pyproj
from pprint import pprint
import inspect
def peek(x):
    """ quick helper util to know wtf is happening with these ephem objects"""
    pprint(inspect.getmembers(x))


class Observatory(ephem.Observer):
    """
    Observatory is an extension of ephem.Observer so that
    it can hold extra fields and be built with a config file
    """
    def __init__(self, config_filename):
        """
        Observatory constructor

        Args:
            config_filename: file name, file must exist (checked in parser.py)

        Returns:
                Observatory
        """
        super().__init__()
        file_contents = {}
        with open(config_filename, "r+") as config:
            file_contents = dict(yaml.safe_load(config))

        self.name = file_contents['instrument_name']
        self.x = file_contents['x']
        self.y = file_contents['y']
        self.z = file_contents['z']

        self.beam_width_arcmin = file_contents["beam_width_arcmin"]

        # converting xyz -> lla
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        # Yes it returs lon, lat , alt not la, lon, alt
        lon, lat, alt = pyproj.transform(
            ecef, lla, self.x, self.y, self.z, radians=True)
        self.lat = lat
        self.lon = lon
        self.alt = alt

        self.config_filename = config_filename  # needed for copy override

    def __str__(self):
        """ Override for str casting so that print(observatory) is useful"""
        output = []
        output.append("--------- " + self.name)
        output.append("\tEECF coords: ")
        output.append("\t\tx: " + str(self.x))
        output.append("\t\ty: " + str(self.y))
        output.append("\t\tz: " + str(self.z))
        output.append("\tLLA coords: ")
        output.append("\t\tlat: " + str(self.lat))
        output.append("\t\tlon: " + str(self.lon))
        output.append("\t\talt: " + str(self.alt))
        output.append("beam width in arcmin: " + str(self.beam_width_arcmin))
        output.append("-----------")
        return '\n'.join(output)

    # sloppy override due to pyephems use of x.copy() not copy(x)
    def copy(self):
        ob = Observatory(self.config_filename)
        return ob
