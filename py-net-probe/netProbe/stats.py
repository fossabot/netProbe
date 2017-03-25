# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 14:50:08 alex>
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
"""

import re
import time

class stats(object):
    """class to gather stats"""
	
    def __init__(self):
        """ constructor """
        super(stats, self).__init__()
        self.sIPv4 = ""
        self.sIPv6 = ""
        self.aVal = {}

    # ---------------------------------------------------------
    def setIPv4(self, add):
        """ IP v4 """
        self.sIPv4 = add

    # ---------------------------------------------------------
    def setIPv6(self, add):
        """ IP v6 """
        self.sIPv6 = add

    # ---------------------------------------------------------
    def setVar(self, sVar, value):
        """ add a variable and value"""
        self.aVal[sVar] = value

    # ---------------------------------------------------------
    def getVar(self, sVar):
        """ get a variable value"""
        if self.aVal.__contains__(sVar):
            return self.aVal[sVar]
        else:
            raise Exception("stats: asked for unknown variable")

    # ---------------------------------------------------------
    def setJob(self, j):
        self.setVar("job-{}-version".format(j['job']), j['version'])
        self.setVar("job-{}-freq".format(j['job']), j['freq'])
        self.setVar("job-{}-id".format(j['job']), j['id'])

    # ---------------------------------------------------------
    def setLastRun(self, job, date):
        self.setVar("job-{}-last".format(job), date)
        
    # ---------------------------------------------------------
    def push(self, srv):
        data = {
            "IPv4" : str(self.sIPv4),
            "IPv6" : str(self.sIPv6)
        }

        for v in self.aVal:
            if re.match("job-.*-last", v):
                data[v] = int(time.time()-self.aVal[v])
            else:
                data[v] = self.aVal[v]

        r = {
            "data" : data,
            "name" : "STATS",
            "date" : time.time()
        }

        srv.pushResults([r])

    # ---------------------------------------------------------
    def debug(self):
        """
        function to print the whole internal object
        """
        print "** DEBUG **"
        print "IPv4 = {}".format(self.sIPv4)
        print "IPv6 = {}".format(self.sIPv6)

        for v in self.aVal:
            if re.match("job-.*-last", v):
                print "{} = {}".format(v, time.time()-self.aVal[v])
            else:
                print "{} = {}".format(v, self.aVal[v])

        print "**********"
