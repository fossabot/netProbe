# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-15 18:25:30 alex>
#

"""
 probe for the icmp protocol
"""

import time
import logging

from .probemain import probemain

class probe_health(probemain):
    """health class for probe

    """

    # -----------------------------------------
    def __init__(self):
        """constructor

        """
        probemain.__init__(self, "HEALTH")

        self.getConfig("health", self.job_health)
        self.mainLoop()

    # -----------------------------------------
    def getConfig(self, name, f):
        """get the configuration from the database if f_testv4 passed

        """
        jobs = super(probe_health, self).getConfig(name, f)
        for j in jobs:
            logging.info("todo")

    # -----------------------------------------
    def job_health(self, _config):
        """health job

        """
        result = {
        }

        logging.info("health results : {}".format(result))
        self.pushResult(result)
