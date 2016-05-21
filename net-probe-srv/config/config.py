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
    def addHost(self, hostData):
        """
        add a host to the database
        """

        sId = hostData['id']

        if hostData.__contains__('jobs'):
            jobs = hostData['jobs']
        else:
            jobs = {}

        if hostData.__contains__('probename'):
            probename = hostData['probename']
        else:
            probename = "unknown"

        if sId != "" and sId != None and sId != False:
            logging.info("add host {} to the DB".format(probename))
            self.aHostTable[sId] = {"jobs" : jobs, "probename": probename}

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
            self.addHost(p)

        logging.info("config file loaded in DB {}".format(sFile))


    # ----------------------------------------------------------
    def getConfigForHost(self, sId):
        """ return the configuration for the host """

        logging.info("get configuration for {}".format(sId))

        return self.aHostTable[sId]['jobs']

    # ----------------------------------------------------------
    def getNameForHost(self, sId):
        """ return the probe name for the host """

        logging.info("get name for {}".format(sId))

        if self.aHostTable.__contains__(sId):
            return self.aHostTable[sId]['probename']
        else:
            return "unknown"

    # ----------------------------------------------------------
    def dump(self):
        """ show the configuration host table """
        return self.aHostTable
