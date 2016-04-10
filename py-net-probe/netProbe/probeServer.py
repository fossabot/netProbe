# -*- Mode: Python; python-indent-offset: 4 -*-
#

"""
Manages communication with the central server

>>> import netProbe
>>> srv = netProbe.probeServer()
>>> srv.findServer()
True
>>> srv.ping()
True
"""

__version__ = "1.1"
__date__ = "10/04/2016"
__author__ = "Alex Chauvin"

import socket
import requests
import time

class probeServer(object):
    """class to talk to the probe server"""
	
    def __init__(self):
        """
        constructor
        """
        self.sServerName = ""
        self.iServerPort = 5000
        self.sPingURL = ""
        self.sSrvBaseURL = ""
        self.bServerAvail = False
        self.lastCmdRespTime = 0

    # -----------------------------------------------------------------
    def findServer(self):
        """
        check which server host to contact
        based on server names
           net-probe-srv-prod
           net-probe-srv
           probe-srv
        """
        for server in ['net-probe-srv-prod',
                       'net-probe-srv',
                       'probe-srv']:
            try:
                socket.getaddrinfo(server, 80)
                self.sServerName = server
                break
            except socket.gaierror:
                print "WARNING cannot find servername {}".format(server)

        if self.sServerName == "":
            print "ERROR no suitable server to talk to"
            return False

        self.sSrvBaseURL = "http://{}:{}".format(self.sServerName,
                                                 self.iServerPort)

        return True

    # -----------------------------------------------------------------
    def ping(self):
        """
        calls the ping web service on the selected server in order
        to know if it is available for other transaction
        gather the response time and store the server status

        returns boolean
        """
        if self.sServerName == "":
            return False

        if self.sPingURL == "":
            self.sPingURL = self.sSrvBaseURL+'/ping'

        try:
            now = time.time()
            requests.get(self.sPingURL)
            delta = time.time() - now
            self.lastCmdRespTime = delta
            self.bServerAvail = True
        except requests.ConnectionError, e:
            print "ERROR reaching srv : {}".format(e.message)
            self.bServerAvail = False
            return False

        return True

    # -----------------------------------------------------------------
    def getLastCmdDeltaTime(self):
        """
        returns last command response time in seconds
        """
        return self.lastCmdRespTime

    # -----------------------------------------------------------------
    def getStatus(self):
        """
        returns communication with server status
        """
        return self.bServerAvail

    # -----------------------------------------------------------------
    def discover(self, sHostId, sIpV4, sIpV6):
        """
        calls the discover web service on the server in order to
        announce the probe itself
        if the probe is known... TODO
        :param sHostId: hostid string to uniquely identify the probe
        :param sIpV4: IP v4 address of the probe
        :param sIpV6: IP v6 address of the probe
        """

        data = {
            'hostId':sHostId,
            'ipv4':sIpV4,
            'ipv6':sIpV6
        }

        req = self.sSrvBaseURL+'/discover'
        r = requests.post(req, data)
        print r
