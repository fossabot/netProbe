# -*- Mode: Python; python-indent-offset: 4 -*-
#

"""
 probe database for configuration and data
"""

__version__ = "1.0"
__date__ = "24/04/2016"
__author__ = "Alex Chauvin"

import redis
import logging
import time

import pprint

class database(object):
    """
    database class based on redis (db=1)
    """

    def __init__(self):
        """
        constructor
        """
        self.backOff = 1
        self.dbRedisId = 1
        self.connect()

    def connect(self):
        """
        connect to the redis server
        wait until it connects
        """

        while(True):
            logging.info("connect to redis")
            self.db = redis.Redis(db=self.dbRedisId, max_connections=1, socket_timeout=2)
            try:
                self.db.ping()
                break

            except redis.ConnectionError, e:
                logging.error("redis : {}, next try in {:.2f}".format(e.message, self.backOff))
                time.sleep(self.backOff)
                self.backOff = backOff*1.5
         
        self.backOff = 1

    def cleanJob(self, jobName):
        """ suppress the list from the database """
        self.db.delete(jobName)

    def addJob(self, jobName, job):
        """ add a job in the job list """
        self.db.rpush(jobName, job)

    def dumpJob(self, jobName):
        l = self.db.llen(jobName)
        if l > 0:
            for i in range(l):
                pprint.pprint(self.db.lindex(jobName, i))

