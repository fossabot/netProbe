# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-01 21:17:41 alex>
#

"""
 config class
"""

import json
import logging
from output import outputer
import output

# import pprint

class config(object):
    """ class to manipulate the configuration """
    
    # ----------------------------------------------------------
    def __init__(self):
        """constructor

        """
        self.aHostTable = {}
        self.outputMethodName = "none"
        self.fileName = "none"

        return

    # ----------------------------------------------------------
    def checkHost(self, sId):
        """check if the host is in the database

        """

        if self.aHostTable.__contains__(sId):
            logging.info("checkHost OK {}".format(sId))
            return True
        else:
            logging.info("checkHost KO {}".format(sId))
            return False

    # ----------------------------------------------------------
    def addHost(self, hostData):
        """add a host to the database

        """

        sId = hostData['id']

        if hostData.__contains__('jobs'):
            jobs = hostData['jobs']
            # check if active present, or put it to True
            for j in jobs:
                if not j.__contains__('active'):
                    j['active'] = "True"
        else:
            jobs = {}

        if hostData.__contains__('probename'):
            probename = hostData['probename']

            for hkey in self.aHostTable:
                h = self.aHostTable[hkey]

                if h.__contains__('probename') and h['probename'] == probename:
                    self.aHostTable[hkey] = {"jobs" : jobs, "probename": probename}
                    logging.info("update probename {}".format(probename))
                    return

        else:
            probename = "unknown"

        if sId != "" and sId != None and sId != False:
            logging.info("add host {} to the DB".format(probename))
            self.aHostTable[sId] = {"jobs" : jobs, "probename": probename}

    # ----------------------------------------------------------
    def loadFile(self, sFile):
        """load host file and update configuraion

        """

        logging.info("load config file {}".format(sFile))

        try:
            f = file(sFile, 'r')
        except IOError:
            logging.error("cannot access config file {}".format(sFile))
            return False

        c = f.read()
        f.close()

        conf = json.loads(c)

        # probes
        if not conf.__contains__('probe'):
            logging.error("cannot find probe configuration, exiting")
            assert False, "no probe config"

        for p in conf['probe']:
            self.addHost(p)

        # clean outputer array before inserting new configuration
        while (len(outputer) > 0):
            outputer.pop()

        # create a fake object for checking method name
        o = output.output()

        if conf.__contains__('output'):
            for outputConf in conf['output']:
                if outputConf['active'] == "True":

                    if not o.checkMethodName(outputConf['engine']):
                        logging.error("unknown output method name, possible values are : {}. Exiting".format(o.getMethodName()))
                        assert False, "bad output name"
                    else:
                        if outputConf['engine'] == "debug":
                            outputer.append(output.debug())

                        if outputConf['engine'] == "elastic":
                            if outputConf.__contains__('parameters'):
                                outputer.append(output.elastic(outputConf['parameters'][0]))
                            else:
                                logging.error("elastic output without parameters, exiting")
                                assert False, "missing parameters for elastic output"

                        if outputConf['engine'] == "logstash":
                            if outputConf.__contains__('parameters'):
                                outputer.append(output.logstash(outputConf['parameters'][0]))
                            else:
                                logging.error("logstash output without parameters, exiting")
                                assert False, "missing parameters for logstash output"

        else:
            outputer.append(output.debug())

        self.fileName = sFile

        logging.info("config file loaded in DB {}".format(sFile))

    # ----------------------------------------------------------
    def reload(self):
        """reload the configuration

        """
        if self.fileName == "none":
            assert False, "no file loaded previously"

        self.loadFile(self.fileName)

    # ----------------------------------------------------------
    def getConfigForHost(self, sId):
        """return the configuration for the host

        """

        logging.info("get configuration for {}".format(sId))

        return self.aHostTable[sId]['jobs']

    # ----------------------------------------------------------
    def getNameForHost(self, sId):
        """return the probe name for the host

        """

        logging.info("get name for {}".format(sId))

        if self.aHostTable.__contains__(sId):
            return self.aHostTable[sId]['probename']
        else:
            return "unknown"

    # ----------------------------------------------------------
    def dump(self):
        """show the configuration host table

        """
        return self.aHostTable
