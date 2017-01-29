# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:00:54 alex>
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

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
            raise Exception('ERROR accessing cpuinfo')

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
                sCPU = str(sCPU)+'@'+str(r.group(1))

        self.id = hashlib.md5(sCPU).hexdigest()

    def get(self):
        """
        returns the id in an md5 format
        """
        return self.id
