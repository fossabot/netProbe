# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-31 22:01:56 alex>
#

"""
 client module for the probe system
"""

__version__ = "1.2"
__date__ = "28/06/2016"
__author__ = "Alex Chauvin"

import time
import logging
import os
# import pprint
import signal

import netProbe
import sched
import hostId
import database
import json

from probe import restartProbe, stopAllProbes, checkProbe

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting probe")

# check wether the uid is root (for icmp)
if os.getuid() != 0:
    logging.error("not root")
    exit()

srv = {}
stats = netProbe.stats()
bConnected = False
bRunning = True
probeJobs = {}
db = database.database()
probeProcess = {}

stats.setVar("probe version", __version__)

# -----------------------------------------
def serverConnect():
    """
    connects to main server, if not available, wait and loop
    """

    global srv
    global stats
    global bConnected
    global bRunning

    # check IP configuration of probe
    # if no default route !
    #
    ip = netProbe.ipConf()

    if ip.hasDefaultRoute() == False:
        logging.error("no default route, abort")
        exit(1)
    else:
        logging.info("ip route OK")

    # get hostId
    #
    hid = hostId.hostId(ip.getLinkAddr()+ip.getIfIPv4())

    stats.setIPv4(ip.getIfIPv4())
    stats.setIPv6(ip.getIfIPv6())

    bConnected = False
    
    iSleepConnectDelay = 0

    while bConnected == False:
        if bRunning == False:
            logging.error("stop main probe")
            exit()

        logging.info("sleep for {:0.0f}s".format(iSleepConnectDelay))
        time.sleep(iSleepConnectDelay)

        if iSleepConnectDelay == 0:
            iSleepConnectDelay = 1
        else:
            if iSleepConnectDelay < 60:
                iSleepConnectDelay = iSleepConnectDelay * 1.5
            else:
                iSleepConnectDelay = 60

        # connect to probe server
        #
        srv = netProbe.probeServer()

        if srv.findServer():
            logging.info("srv IP found in tables")
        else:
            logging.error("server not found in DNS or host table")
            continue

        # send identification to get id & certificate
        #
        if srv.discover(hid.get(), ip.getIfIPv4(), ip.getIfIPv6()) == True:
            bConnected = True

        if bConnected and srv.ping() == False:
            logging.error("service ping not working")
            continue

#
# -----------------------------------------
def ping():
    """
    call the ping ws of the server
    called by the scheduler
    """

    global stats

    if srv.ping():
        logging.info("ping delta time = {:0.2f}ms".format(srv.getLastCmdDeltaTime()*1000))
        stats.setVar("ping server (ms)", srv.getLastCmdDeltaTime()*1000)

# -----------------------------------------
def showStatus():
    """called by the scheduler in order to print if the server is
    available

    """
    global bConnected

    if srv.getStatus() == False:
        logging.warning("server not available")
        bConnected = False
    else:
        logging.info("server up and alive")


# -----------------------------------------
def pushJobsToDB(jobName):
    """ change the job definition for the probe job in the db called only
    if the job config has been updated
    """
    global db
    global probeJobs
    global stats

    # suppress the old definition in db
    db.cleanJob(jobName)

    for i in probeJobs.keys():
        j = probeJobs[i]
        if j['job'] == jobName:
            del j['restart']
            db.addJob(jobName, j)
            stats.setJob(j)

# -----------------------------------------
def getConfig():
    """
    get my probe config from the server
    """
    global probeJobs
    global bConnected

    aModules = ['icmp', 'health', 'http', 'iperf']

    if bConnected == False:
        return

    logging.info("get configuration from server")

    # if we need to restart one job, we fill this dictionary
    restart = {}

    config = srv.getConfig()
    if config == None:
        logging.error("can't get my config")
        bConnected = False
        return None

    for c in config:
        # update job or create
        if probeJobs.__contains__(c['id']):
            a = probeJobs[c['id']]
            if c['version'] > a['version']:
                a['restart'] = 1
                a['version'] = c['version']
                a['data'] = c['data']
            else:
                a['restart'] = 0
        else:
            a = c
            a['restart'] = 1

        if a['restart'] == 1:
            probeJobs[c['id']] = a

            for m in aModules:
                if a['job'] == m:
                    restart[m] = 1

    if len(restart) == 0:
        return

    for m in aModules:
        if restart.__contains__(m):
            pushJobsToDB(m)
            restartProbe(m, probeProcess)

# -----------------------------------------
def checkProbes():
    """ check all started probes
    """
    global probeProcess

    for k in probeProcess.keys():
        if checkProbe(k, probeProcess) == False:
            restartProbe(k, probeProcess)
    
# -----------------------------------------
def mainLoop():
    """
    main scheduler loop
    """
    global scheduler
    global bConnected
    global stats

    while bConnected:
        f = scheduler.step()
        time.sleep(f)

# -----------------------------------------
def trap_signal(sig, heap):
    """ trap all signals for stop """

    global bRunning
    global bConnected
    global probeProcess

    logging.info("exit signal received, wait for next step")

    stopAllProbes(probeProcess)

    bRunning = False
    bConnected = False

# -----------------------------------------
def popResults(_db):
    """pop the results from the database queue and push these to the server

    """
    global stats

    a = []

    l = _db.lenResultQueue()
    logging.info("result queue len {}".format(l))

    if l < 5:
        nb = 3
    else:
        nb = int(l/2)

    for i in range(nb):
        r = _db.popResult()
        if r != None:
            j = json.loads(r)
            stats.setLastRun(j['name'].lower(), j['date'])
            a.append(j)

    if len(a) > 0:
        srv.pushResults(a)

# -----------------------------------------

signal.signal(signal.SIGTERM, trap_signal)
signal.signal(signal.SIGINT, trap_signal)

# create global scheduler
#
scheduler = sched.sched()

while bRunning:
    scheduler.clean()

    serverConnect()

    getConfig()
    scheduler.add("get configuration", 60, getConfig, None, 2)

    scheduler.add("push results", 8, popResults, db, 2)
    scheduler.add("ping server", 15, ping, None, 2)
    # scheduler.add("show status", 300, showStatus, None, 2)
    scheduler.add("check probe", 10, checkProbes)
    scheduler.add("stats", 60, stats.push, srv, 2)

    mainLoop()
