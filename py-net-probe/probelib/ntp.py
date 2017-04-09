# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 17:47:48 alex>
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
 probe for the ntp statistics of the probe
"""

import logging
#import time
import subprocess
#import json
import re

from .probemain import probemain

class probe_ntp(probemain):
    """ ntp class for probe
    """

    # -----------------------------------------
    def __init__(self):
        """constructor

        """
        probemain.__init__(self, "NTP")

        self.checkNet()
        self.getConfig("ntp", self.job_ntp)
        self.mainLoop()

    # -----------------------------------------
    def getConfig(self, name, f, testf=None):
        """get the configuration from the database

        """
        jobs = super(probe_ntp, self).getConfig(name, f, self.f_testOK)
        for j in jobs:
            logging.info("add job to scheduler each {} sec".format(j['freq']))

    # -----------------------------------------
    def job_ntp(self, _config):
        """ntp job

        """

        aParams = ["ntpdc", "-c", "sysinfo"]
        try:
            p = subprocess.Popen(aParams, stdout=subprocess.PIPE)
            o = p.communicate()[0]
        except Exception as ex:
            logging.error("launching ntpdc {}".format(", ".join(ex.args)))
            return

        if p.returncode != 0:
            logging.error("communication with ntpdc")
            return

        # print(o)
        result = {}

        r = re.search('^stratum:\\s*(\d*)', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, stratum not found in ntpdc -c sysinfo")
            return
        result["ntp-stratum"] = int(r.group(1).strip())

        r = re.search('^system peer:\\s*(.*)', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, system peer not found in ntpdc -c sysinfo")
            return
        result["ntp-peer"] = r.group(1).strip()

        r = re.search('^jitter:\\s*(.*) s', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, jitter not found in ntpdc -c sysinfo")
            return
        result["ntp-jitter"] = float(r.group(1).strip())*1000

        r = re.search('^root distance:\\s*(.*) s', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, distance not found in ntpdc -c sysinfo")
            return
        result["ntp-distance"] = float(r.group(1).strip())*1000

        r = re.search('^root dispersion:\\s*(.*) s', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, dispersion not found in ntpdc -c sysinfo")
            return
        result["ntp-dispersion"] = float(r.group(1).strip())*1000

        # more information
        aParams = ["ntpdc", "-c", "showpeer {}".format(result['ntp-peer'])]
        try:
            p = subprocess.Popen(aParams, stdout=subprocess.PIPE)
            o = p.communicate()[0]
        except Exception as ex:
            logging.error("launching ntpdc showpeer {}".format(", ".join(ex.args)))
            return

        if p.returncode != 0:
            logging.error("communication with ntpdc showpeer")
            return

        # print(o)

        r = re.search('^offset (.*), delay (.*), error', o, re.MULTILINE)
        if r==None:
            logging.info("ntp error, stratum not found in ntpdc -c sysinfo")
            return
        result["ntp-offset"] = float(r.group(1).strip())*1000
        result["ntp-delay"] = float(r.group(2).strip())*1000

        logging.info("ntp result : {}".format(result))
        self.pushResult(result)
