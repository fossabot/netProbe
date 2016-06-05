# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-05 17:24:54 alex>
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
        else:
            jobs = {}

        if hostData.__contains__('probename'):
            probename = hostData['probename']

            for hkey in self.aHostTable:
                h = self.aHostTable[hkey]

                if h.__contains__('probename') and h['probename'] == probename:
                    logging.error("this probename is already registered: {}".format(probename))
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

        try:
            f = file(sFile, 'r')
        except IOError:
            logging.error("accessing config file {}".format(sFile))
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

        # output
        if conf.__contains__('output'):
            iOutput = 0
            for outputConf in conf['output']:
                o = outputer[iOutput]

                if outputConf['active'] == "True":

                    if not o.checkMethodName(outputConf['engine']):
                        logging.error("unknown output method name, possible values are : {}. Exiting".format(o.getMethodName()))
                        assert False, "bad output name"
                    else:
                        if outputConf['engine'] == "debug":
                            outputer[iOutput] = output.debug()

                        if outputConf['engine'] == "elastic":
                            if outputConf.__contains__('parameters'):
                                outputer[iOutput] = output.elastic(outputConf['parameters'][0])
                            else:
                                logging.error("elastic output without parameters, exiting")
                                assert False, "missing parameters for elastic output"

                        iOutput += 1
                        outputer.append(output.output())

        else:
            outputer[0] = output.debug()

        logging.info("config file loaded in DB {}".format(sFile))

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
