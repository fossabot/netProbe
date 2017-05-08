# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-30 16:53:29 alex>
#
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
 probe database for configuration and data
"""

import logging
import time
import json
import redis

# import pprint

class dbRedis(object):
    """
    database class based on redis (db=1)
    """

    def __init__(self, host=None):
        """
        constructor
        """
        self.backOff = 1
        self.db = None
        self.dbRedisId = 1

        self.connect(host)

    def connect(self, host=None):
        """
        connect to the redis server
        wait until it connects
        """

        while True:
            if host is None:
                host = "localhost"
                self.db = redis.Redis(db=self.dbRedisId, max_connections=1, socket_timeout=2)
            else:
                self.db = redis.Redis(db=self.dbRedisId, max_connections=1, socket_timeout=2, host=host)

            logging.info("connect to redis {}".format(host))

            try:
                self.db.ping()
                break

            except redis.ConnectionError, e:
                self.backOff *= 1.5
                if self.backOff > 30:
                    self.db = None
                    raise Exception('redis not running ? abort')
                logging.error("redis : {}, next try in {:.2f}".format(e.message, self.backOff))
                time.sleep(self.backOff)
         
        self.backOff = 1

    def checkDB(self):
        """check if db is set"""
        if self.db is None:
            raise Exception("redis not started")

    def cleanJob(self, jobName):
        """suppress the list from the database

        """
        self.checkDB()
        return self.db.delete(jobName)

    def addJob(self, jobName, job):
        """add a job in the job list

        """
        self.checkDB()
        self.db.rpush(jobName, json.dumps(job))

    def getJobs(self, jobName):
        """extracts all jobs and return an array

        """
        self.checkDB()

        a = []
        l = self.db.llen(jobName)
        if l > 0:
            for i in range(l):
                s = self.db.lindex(jobName, i)
                a.append(json.loads(s))

        return a

    def dumpJob(self, jobName):
        """dump the content of the db for jobname, return a generator

        """
        self.checkDB()

        l = self.db.llen(jobName)
        if l > 0:
            for i in range(l):
                yield self.db.lindex(jobName, i)

    def pushResult(self, result):
        """add a result in the queue for the main process
        result is a dict

        """
        if not isinstance(result, dict):
            raise Exception("pushResult not provided a dict")

        self.checkDB()

        self.db.rpush("results", json.dumps(result))

    def popResult(self):
        """pop a result from the queue
        return None if nothing in the queue
        """
        self.checkDB()
        return self.db.lpop("results")

    def lenResultQueue(self):
        """get queue size
        """
        self.checkDB()
        return self.db.llen("results")
