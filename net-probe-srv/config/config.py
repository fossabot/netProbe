# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 15:04:38 alex>
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
        self.aTemplates = {}
        # self.outputMethodName = "none"
        self.fileName = "none"
        self.iTemplateJobsId = 1000

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
    def applyTemplateToHost(self, hostData, tName):
        """apply the template tName to the hostData

        """

        if not self.aTemplates.__contains__(tName):
            logging.warning("add a template non existant {} {}".format(hostData['id'], tName))
            return

        logging.info("applyTemplateToHost {} {}".format(hostData['probename'], tName))

        hjs = None

        t = self.aTemplates[tName]
        if t.__contains__('jobs'):

            # already some jobs on the probe ? maybe an update only
            if hostData.__contains__('probename'):
                probename = hostData['probename']

                for hkey in self.aHostTable:
                    h = self.aHostTable[hkey]
                    
                    if h.__contains__('probename') and h['probename'] == probename:
                        if h.__contains__('jobs'):
                            hjs = h['jobs']
                            break

            for j in t['jobs']:
                newJob = j.copy()
                newJob['id'] = 0

                if hjs != None:
                    for hj in hjs:
                        if hj.__contains__('template'):
                            if hj['template'] == tName and hj['data'] == newJob['data']:
                                newJob['id'] = hj['id']

                if newJob['id'] == 0:
                    newJob['id'] = self.iTemplateJobsId
                    self.iTemplateJobsId += 1

                newJob['template'] = tName

                if hostData.__contains__('jobs'):
                    hostData['jobs'].append(newJob)
                else:
                    hostData['jobs'] = [ newJob ]

    # ----------------------------------------------------------
    def addHost(self, hostData):
        """add a host to the database, if template specified, apply
           first the template
        """

        sId = str(hostData['id'])

        if hostData.__contains__('template'):
            for t in hostData['template']:
                self.applyTemplateToHost(hostData, t)

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
                    # if same name but different id, insert a new key
                    if (hkey != sId):
                        del(self.aHostTable[hkey])
                        hkey = sId
                    self.aHostTable[hkey] = {"jobs" : jobs, "probename": probename}
                    logging.info("update probename {}".format(probename))
                    return

        else:
            probename = "unknown"

        if sId != "" and sId != None and sId != False:
            logging.info("add host {} to the DB".format(probename))
            self.aHostTable[sId] = {"jobs" : jobs, "probename": probename}

    # ----------------------------------------------------------
    def addTemplate(self, templateData):
        """add a template from the configuration file to the database

        """

        if not templateData.__contains__('name'):
            assert False, "no name section in template"

        sName = templateData['name']
        logging.info(sName)

        if templateData.__contains__('jobs'):
            jobs = templateData['jobs']
        else:
            jobs = {}

        self.aTemplates[sName] = {"jobs" : jobs}
        
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

        conf = ''
        try:
            conf = json.loads(c)
        except Exception as ex:
            assert False, "configuration file load exception : {}".format(", ".join(ex.args))

        # template
        if conf.__contains__('template'):
            for t in conf['template']:
                self.addTemplate(t)

        # group

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
                        logging.error("unknown output method name '{}', possible values are : {}".format(outputConf['engine'], ", ".join(o.getMethodName())))
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
    def getJobsForHost(self, sId):
        """return the jobs configuration for the host

        """

        logging.info("get jobs for {}".format(sId))

        if self.aHostTable.__contains__(sId):
            return self.aHostTable[sId]['jobs']
        else:
            logging.error("should not ask for unknown host in the configuration")
            return None

    # ----------------------------------------------------------
    def getConfigForHost(self, sId):
        """return the configuration for the host

        """

        logging.info("get configuration for {}".format(sId))

        if self.aHostTable.__contains__(sId):
            return self.aHostTable[sId]
        else:
            logging.error("should not ask for unknown host in the configuration")
            return None

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
    def getListTemplate(self):
        """return the templates name

        """
        for t in self.aTemplates.keys():
            yield t

    # ----------------------------------------------------------
    def getListProbes(self):
        """return the probes name

        """
        for p in self.aHostTable.keys():
            templates = ""
            for j in self.aHostTable[p]['jobs']:
                if j.__contains__('template'):
                    templates += j['template']+", "
            yield [ self.aHostTable[p]['probename'],
                    p[-8:],
                    len(self.aHostTable[p]['jobs']),
                    templates[:-2]]

    # ----------------------------------------------------------
    def dump(self):
        """show the configuration host table

        """
        return self.aHostTable
