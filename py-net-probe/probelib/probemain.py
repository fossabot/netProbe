# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-15 18:27:17 alex>
#

"""
probemain is the minima probe library class to help creating probes
"""

import os
import sys
import logging
import signal
import time

sys.path.insert(0, os.getcwd())
from netProbe import ipConf
import sched
import database

__version__ = "1.2"
__date__ = "15/05/2016"
__author__ = "Alex Chauvin"

class probemain(object):
    """
    minimal probe class
    """

    # -----------------------------------------
    def __init__(self, name):
        """
        constructor
        """
        self.ip = None

        self.name = name
        _logFormat = '%(asctime)-15s '+str(name)+' [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
        logging.basicConfig(format=_logFormat,
                            level=logging.INFO)

        logging.info("starting probe")

        self.db = database.database()

        # create global scheduler
        self.scheduler = sched.sched()
        self.scheduler.clean()

        self.bRunning = True

        signal.signal(signal.SIGTERM, self.trap_signal)
        signal.signal(signal.SIGINT, self.trap_signal)

    # -----------------------------------------
    def checkNet(self):
        """check IP configuration of probe if no default route !
        """

        logging.info("check if default route is present")
        self.ip = ipConf()
        
        if self.ip.hasDefaultRoute() == False:
            assert False, "no default route, abort"

    # -----------------------------------------
    def getIP(self):
        """returns the ip module

        """
        return self.ip

    # -----------------------------------------
    def mainLoop(self):
        """main scheduler loop

        """

        while self.bRunning:
            f = self.scheduler.step()
            time.sleep(f)

        logging.info("end probe {}".format(self.name))

    # -----------------------------------------
    def trap_signal(self, sig, heap):
        """catch the signals to handle the restart of the probe module

        """
        logging.info("exiting after signal received")
        
        self.bRunning = False

    # -----------------------------------------
    def addJob(self, freq, f, data):
        """add a job in the scheduler

        """
        self.scheduler.add(freq, f, data)

    # -----------------------------------------
    def getConfig(self, name, f, testf):
        """get config in database and extract 'name' jobs

        """
        config = self.db.getJobs(name)

        for c in config:
            if c['job'] == name:
                data = c['data']
                if testf(data):
                    self.addJob(int(c['freq']), f, data)
                    yield c

    # -----------------------------------------
    def getConfig(self, name, f):
        """get config in database and extract 'name' jobs

        """
        config = self.db.getJobs(name)

        for c in config:
            if c['job'] == name:
                data = c['data']
                self.addJob(int(c['freq']), f, data)
                yield c

    # -----------------------------------------
    def pushResult(self, result):
        """push a result back to the database for main process to handle

        """
        if not isinstance(result, dict):
            raise Exception("pushResult not provided a dict")

        r = {"data" : result,
             "name" : self.name,
             "date" : time.time()
        }

        self.db.pushResult(r)
