# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-15 15:47:49 alex>
#

"""
 probe database for configuration and data
"""

__version__ = "1.1"
__date__ = "01/05/2016"
__author__ = "Alex Chauvin"

import redis
import logging
import time
import json

# import pprint

class database(object):
    """
    database class based on redis (db=1)
    """

    def __init__(self):
        """
        constructor
        """
        self.backOff = 1
        self.db = None
        self.dbRedisId = 1
        self.connect()

    def connect(self):
        """
        connect to the redis server
        wait until it connects
        """

        while True:
            logging.info("connect to redis")
            self.db = redis.Redis(db=self.dbRedisId, max_connections=1, socket_timeout=2)
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

    def cleanJob(self, jobName):
        """suppress the list from the database

        """
        if self.db == None:
            raise Exception("redis not started")
        return self.db.delete(jobName)

    def addJob(self, jobName, job):
        """add a job in the job list

        """
        if self.db == None:
            raise Exception("redis not started")
        self.db.rpush(jobName, json.dumps(job))

    def getJobs(self, jobName):
        """extracts all jobs and return an array

        """
        if self.db == None:
            raise Exception("redis not started")

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
        if self.db == None:
            raise Exception("redis not started")

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

        if self.db == None:
            raise Exception("redis not started")

        self.db.rpush("results", json.dumps(result))

    def popResult(self):
        """pop a result from the queue
        return None if nothing in the queue
        """
        return self.db.lpop("results")

    def lenResultQueue(self):
        return self.db.llen("results")
