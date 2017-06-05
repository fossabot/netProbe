# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-06-05 20:48:42 alex>
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
 probe database template
"""

import logging
import json
import sys

# import pprint

class db(object):
    """
    database class for basic functions
    """

    def __init__(self):
        """
        constructor
        """
        self.db = None

    def connect(self):
        """ simulate the connection to the database """
        self.db = True

    @classmethod
    def cleanJob(cls, jobName):
        """suppress the list from the database

        """
        logging.debug("delete {}".format(jobName))


    @classmethod
    def addJob(cls, jobName, job):
        """add a job in the job list

        """
        logging.info("add job {} {}".format(jobName, json.dumps(job)))

    @classmethod
    def getJobs(cls, _):
        """extracts all jobs and return an array

        """
        logging.debug("getJobs")

        return json.loads(sys.stdin.read())
        # return True

    @classmethod
    def dumpJob(cls, jobName):
        """dump the content of the db for jobname, return a generator

        """
        logging.debug("dumpJob {}".format(jobName))

    @classmethod
    def pushResult(cls, result):
        """add a result in the queue for the main process
        result is a dict

        """
        if not isinstance(result, dict):
            raise Exception("pushResult not provided a dict")

        logging.info("push result {}".format(result))

    @classmethod
    def popResult(cls):
        """pop a result from the queue
        return None if nothing in the queue
        """
        logging.debug("pop result")

    @classmethod
    def lenResultQueue(cls):
        """get queue size
        """
        logging.debug("lenResultQueue")
        return 0

    # -----------------------------------------
    @classmethod
    def setLock(cls, sModule, sType):
        """add a lock in the local database

        """
        logging.debug("setLock {} {}".format(sModule, sType))

    # -----------------------------------------
    @classmethod
    def releaseLock(cls, sType):
        """ release the lock template

        """

        logging.debug("releaseLock {}".format(sType))

    # -----------------------------------------
    @classmethod
    def checkLock(cls, sType="none", sModule="none"):
        """checks if a lock is in the queue

        returns True if a local lock is present
        """

        logging.debug("checkLock")
        return False

    # -----------------------------------------
    @classmethod
    def incrRunningProbe(cls):
        """incr probe num template

        """
        logging.debug("incrRunningProbe")


    # -----------------------------------------
    @classmethod
    def decrRunningProbe(cls):
        """ decr probe num template

        """

        logging.debug("decrRunningProbe")

    # -----------------------------------------
    @classmethod
    def isProbeRunning(cls):
        """ probe running template

        """
        return False

    # -----------------------------------------
    @classmethod
    def cleanLock(cls):
        """ clean the lock template
        
        """
        logging.debug("cleanLock from database")
