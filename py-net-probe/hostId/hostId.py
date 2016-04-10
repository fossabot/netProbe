# -*- Mode: Python; python-indent-offset: 4 -*-
#

"""
unique identifier for the probe
"""

__version__ = "1.0"
__date__ = "08/04/2016"
__author__ = "Alex Chauvin"

import hashlib
import re
# import pprint

class hostId(object):
    """ class to manipulate host id and get unique identifier
        for the probe """

    id = "none"

    def __init__(self, sUniqueId):
        """
        constructor
        calculate this host id based on the cpuinfo and unique id provided

        :param sUniqueId: unique id string (ie Mac Address)
        """

        try:
            f = file('/proc/cpuinfo', 'r')
        except IOError, e:
            print "ERROR accessing cpuinfo {}".format(e)
            return

        sCPU = sUniqueId
        
        aLines = f.readlines()
        f.close()

        for l in aLines:
            r = re.match("flags[^:]+: (.*)", l)
            if r != None:
                sCPU = sCPU+'@'+r.group(1)

            r = re.match("bogomips[^:]+: (.*)", l)
            if r != None:
                sCPU = sCPU+'@'+r.group(1)

            r = re.match("model[^:]+: (.*)", l)
            if r != None:
                sCPU = sCPU+'@'+r.group(1)

        self.id = hashlib.md5(sCPU).hexdigest()

    def get(self):
        """
        returns the id in an md5 format
        """
        return self.id
