# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-22 21:48:03 alex>
#

"""
 config liveDB
 used to store the current status of probes
"""

import json
import logging

from config import conf
# import pprint

class liveDB(object):
    """ class to manipulate the liveDB """
    
    # ----------------------------------------------------------
    def __init__(self):
        """constructor

        """
        self.aProbeTable = {}
        self.uid = 0
        return

    # ----------------------------------------------------------
    def getUniqueId(self, sId):
        """ returns a unique id for the probe. If the probe is already
        registered returns the associated uid

        """
        if self.aProbeTable.__contains__(sId):
            host = self.aProbeTable[sId]
            if host.__contains__('uid'):
                return host['uid']

        self.uid = self.uid+1
        return self.uid

    # ----------------------------------------------------------
    def addHost(self, sId):
        """
        add a host to the database
        """
        if sId != "" and sId != None and sId != False:
            logging.info("add host to the live DB")
            self.aProbeTable[sId] = {}

    # ----------------------------------------------------------
    def updateHost(self, sId, o):
        """ update host by its identifier """

        if self.aProbeTable.__contains__(sId) == False:
            self.addHost(sId)

        new = self.aProbeTable[sId].copy()
        new.update(o)

        self.aProbeTable.update({sId : new})
        logging.info("update host in live DB {}".format(sId))

    # ----------------------------------------------------------
    def getHostByUid(self, uid):
        """ return HostId by uid """

        for hkey in self.aProbeTable:
            h = self.aProbeTable[hkey]

            if h.__contains__('uid') and h['uid'] == uid:
                return hkey

        return None

    # ----------------------------------------------------------
    def getHostContentByUid(self, uid):
        """return Host content by uid

        """

        for hkey in self.aProbeTable:
            h = self.aProbeTable[hkey]

            if h.__contains__('uid') and h['uid'] == uid:
                return h

        return None

    # ----------------------------------------------------------
    def getConfigForHost(self, host):
        """ return the probe config """

        return conf.getConfigForHost(host)

    # ----------------------------------------------------------
    def getNameForHost(self, host):
        """ return the probe name """

        return conf.getNameForHost(host)

    # ----------------------------------------------------------
    def dump(self):
        """ show the configuration host table """
        return self.aProbeTable

    # ----------------------------------------------------------
    def cleanDB(self):
        """clean the whole database

        """
        self.aProbeTable = {}
        self.uid = 0

    
