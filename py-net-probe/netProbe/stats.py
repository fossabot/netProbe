# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-27 22:32:39 alex>
#

"""
"""

import re
import time

__version__ = "1.0"
__date__ = "27/06/2016"
__author__ = "Alex Chauvin"

class stats(object):
    """class to gather stats"""
	
    def __init__(self):
        """ constructor """
        super(stats, self).__init__()
        self.sIPv4 = ""
        self.sIPv6 = ""
        self.aVal = {}

    def setIPv4(self, add):
        """ IP v4 """
        self.sIPv4 = add

    def setIPv6(self, add):
        """ IP v6 """
        self.sIPv6 = add

    def setVar(self, sVar, value):
        """ add a variable and value"""
        self.aVal[sVar] = value

    def setJob(self, j):
        self.setVar("job-{}-version".format(j['job']), j['version'])
        self.setVar("job-{}-freq".format(j['job']), j['freq'])
        self.setVar("job-{}-id".format(j['job']), j['id'])

    def setLastRun(self, job, date):
        self.setVar("job-{}-last".format(job), date)
        
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

        print r
        srv.pushResults([r])

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
