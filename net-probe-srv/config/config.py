# -*- Mode: Python; python-indent-offset: 4 -*-
#

"""
 config class
"""

import json
import logging
# import pprint

class config(object):
    """ class to manipulate the configuration """
    
    # ----------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        self.aHostTable = {}
        return

    # ----------------------------------------------------------
    def checkHost(self, sId):
        """
        check if the host is in the database
        """
        if self.aHostTable.__contains__(sId):
            logging.info("checkHost OK {}".format(sId))
            return True
        else:
            logging.info("checkHost KO {}".format(sId))
            return False

    # ----------------------------------------------------------
    def addHost(self, sId):
        """
        add a host to the database
        """
        if sId != "" and sId != None and sId != False:
            logging.info("add host to the DB")
            self.aHostTable[sId] = {}

    # ----------------------------------------------------------
    def getHostByUid(self, uid):
        """ return HostId by uid """

        for hkey in self.aHostTable:
            h = self.aHostTable[hkey]

            if h.__contains__('uid') and h['uid'] == uid:
                return hkey

        return None

    # ----------------------------------------------------------
    def loadFile(self, sFile):
        """
        load host file and update configuraion
        """

        try:
            f = file(sFile, 'r')
        except IOError:
            logging.error("accessing config file {}".format(sFile))
            return False

        c = f.read()
        f.close()

        conf = json.loads(c)
        for p in conf['probe']:
            self.addHost(p['id'])

        logging.info("config file loaded in DB {}".format(sFile))

    def dump(self):
        """ show the configuration host table """
        return self.aHostTable
