# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 14:49:57 alex>
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
>>> import netProbe
>>> ip = netProbe.ipConf()
>>> ip.hasDefaultRoute()
True
>>> ip.getLinkAddr()
'08:00:27:f8:80:e7'
>>> ip.getIfIPv4()
'10.0.2.15'
>>> ip.getIfIPv6()
'fe90::a00:...'
"""

__version__ = "1.0"
__date__ = "08/04/2016"
__author__ = "Alex Chauvin"

import netifaces
import re

class ipConf(object):
    """class to gather and store ip configuration of host"""

    def __init__(self):
        """ constructor """
        self.iGotDefault = False
        self.sInterface = ""
        self.aIfv4 = {}
        self.aIfv6 = {}
        self.aLink = {}

        # check wether we have a default gateways
        self.gws = netifaces.gateways()
        
        if 'default' in self.gws and netifaces.AF_INET in self.gws['default']:
            self.iGotDefault = True

            # get interface name
            self.sInterface = self.gws['default'][netifaces.AF_INET][1]
		
            ifs = netifaces.ifaddresses(self.sInterface)
            
            if netifaces.AF_INET in ifs:
                self.aIfv4 = ifs[netifaces.AF_INET][0]
                self.aLink = ifs[netifaces.AF_LINK][0]
                # print(ifs[netifaces.AF_LINK])
			
            if netifaces.AF_INET6 in ifs:
                self.aIfv6 = ifs[netifaces.AF_INET6][0]

            super(ipConf, self).__init__()
		
    def hasDefaultRoute(self):
        """ 
        does the ip stack has a default route
        return boolean
        """
        return self.iGotDefault

    def getLinkAddr(self):
        """
        returns the mac address of the interface with the default route
        """
        if 'addr' in self.aLink:
            return self.aLink['addr']
        else:
            return False

    def getIfName(self):
        """
        return the interface name with the default route
        """
        return self.sInterface
	
    def getIfIPv4(self):
        """
        return the IP version 4 address of the interface
        with the default route
        """
        if 'addr' in self.aIfv4:
            return self.aIfv4['addr']
        else:
            return False

    def getIfIPv6(self):
        """
        return the IP version 6 address of the interface
        with the default route
        """
        if 'addr' in self.aIfv6:
            return re.match('([^%]+)', self.aIfv6['addr']).group(1)
        else:
            return False
	
    def debug(self):
        """
        function to print the whole internal object
        """
        print "** DEBUG **"
        print " got default route : good"
        print "  Interface : {}".format(self.sInterface)
        if 'addr' in self.aIfv4:
            print "  IPv4 : addr {}/{}".format(self.aIfv4['addr'],
                                               self.aIfv4['netmask'])
        if 'addr' in self.aIfv6:
            print "  IPv6 : addr {}/{}".format(self.aIfv6['addr'],
                                               self.aIfv6['netmask'])
        print "**********"
