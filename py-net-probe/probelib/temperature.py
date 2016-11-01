# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-01 18:28:44 alex>
#

"""
 probe for the temperature of the PI
"""

import time
import logging
# import pprint

from .probemain import probemain

class probe_temp(probemain):
    """temperature class for probe

    """

    # -----------------------------------------
    def __init__(self, bTest=False):
        """constructor

        """
        probemain.__init__(self, "TEMP")

        self.checkNet()

        if not bTest:
            self.getConfig("temp", self.job_temp)
            self.mainLoop()
        
    # -----------------------------------------
    def getConfig(self, name, f):
        """get the configuration from the database if f_testv4 passed

        """
        jobs = super(probe_temp, self).getConfig(name, f, self.fTestNone)
        for j in jobs:
            logging.info("add temperature job to scheduler")

    # -----------------------------------------
    def job_temp(self, _config=None):
        """temperature job

        """

        result = {}

        # -------- Termperature from PI thermal sensor  --------------
        tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
        result['temp-pi-celsius'] = tempC
        result['temp-pi-fahrenheit'] = tempC*9/5+32

        logging.info("temperature results : {}".format(result))

        self.pushResult(result)
