# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-21 15:57:30 alex>
#

"""
 probe for the icmp protocol
"""

import time
import logging
import psutil
# import pprint

from .probemain import probemain

class probe_health(probemain):
    """health class for probe

    """

    # -----------------------------------------
    def __init__(self, bTest=False):
        """constructor

        """
        probemain.__init__(self, "HEALTH")

        self.checkNet()

        if not bTest:
            self.getConfig("health", self.job_health)
            self.mainLoop()
        
    # -----------------------------------------
    def getConfig(self, name, f):
        """get the configuration from the database if f_testv4 passed

        """
        jobs = super(probe_health, self).getConfig(name, f, self.fTestNone)
        for j in jobs:
            logging.info("add health job to scheduler")

    # -----------------------------------------
    def job_health(self, _config=None):
        """health job

        """

        result = {}

        # -------- PIDS  --------------
        result['health-pids'] = len(psutil.pids())

        # -------- CPU  --------------
        a = psutil.cpu_percent(interval=2, percpu=False)
        result['health-cpu'] = a

        a = psutil.cpu_times(percpu=False)
        result['health-cputimes_user'] = a[0]
        result['health-cputimes_system'] = a[1]
        result['health-cputimes_idle'] = a[2]
        result['health-uptime'] = int(time.time() - int(psutil.boot_time()))

        # -------- MEMORY  --------------
        a = psutil.virtual_memory()
        result['health-vmem_total'] = int(a[0]/1024/1024)
        result['health-vmem_available'] = int(a[1]/1024/1024)
        result['health-vmem_percent'] = int(a[2])
        result['health-vmem_used'] = int(a[3]/1024/1024)
        result['health-vmem_zeroed'] = int(a[4]/1024/1024)

        a = psutil.swap_memory()
        result['health-swap_total'] = int(a[0]/1024/1024)
        result['health-swap_used'] = int(a[1]/1024/1024)
        result['health-swap_free'] = int(a[2]/1024/1024)
        result['health-swap_percent'] = int(a[3])

        # -------- DISK /  --------------
        b = psutil.disk_usage('/')
        result['health-disk_total'] = int(b[0]/1024/1024)
        result['health-disk_used'] = int(b[1]/1024/1024)
        result['health-disk_free'] = int(b[2]/1024/1024)
        result['health-disk_percent'] = int(b[3])

        # -------- NET  --------------
        ifName = self.getEthName()

        a = psutil.net_io_counters(pernic=True)
        result['health-netio_bytes_sent'] = a[ifName][0]
        result['health-netio_bytes_recv'] = a[ifName][1]
        result['health-netio_pkts_sent'] = a[ifName][2]
        result['health-netio_pkts_recv'] = a[ifName][3]

        # pprint.pprint(result)

        logging.info("health results : {}".format(result))

        self.pushResult(result)