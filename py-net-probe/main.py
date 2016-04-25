# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-24 22:46:20 alex>
#

"""
 client module for the probe system
"""

import time
import logging
import os
import pprint
import signal

import netProbe
import sched
import hostId
import database

from probe import restartProbe, stopAllProbes

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting probe")

# check wether the uid is root (form icmp)
if (os.getuid() != 0):
    logging.error("not root")
    exit()

srv = {}
bConnected = False
bRunning = True
probeJobs = {}
db = database.database()
probeProcess = {}

# -----------------------------------------
def serverConnect():
    """
    connects to main server, if not available, wait and loop
    """

    global srv
    global bConnected

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
    hid = hostId.hostId(ip.getLinkAddr())

    bConnected = False
    
    iSleepConnectDelay = 1

    while bConnected == False:
        logging.info("sleep for {:0.0f}s".format(iSleepConnectDelay))
        time.sleep(iSleepConnectDelay)

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
    if srv.ping():
        logging.info("ping delta time = {:0.2f}ms".format(srv.getLastCmdDeltaTime()*1000))

# -----------------------------------------
def showStatus():
    """
    called by the scheduler in order to print if the server is available
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

    # suppress the old definition in db
    db.cleanJob(jobName)

    # pprint.pprint(probeJobs)

    for id in probeJobs.keys():
        j = probeJobs[id]
        if j['job'] == jobName:
            del j['restart']
            db.addJob(jobName, j)
            
            j['version'] = 0

    # db.dumpJob(jobName)

# -----------------------------------------
def getConfig():
    """
    get my probe config from the server
    """
    global probeJobs
    global bConnected

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
        # pprint.pprint(c)
        # update job or create
        if probeJobs.__contains__(c['id']):
            a = probeJobs[c['id']]

            if c['version'] > a['version']:
                a['restart'] = 1
                a['version'] = c['version']
                a['data'] = c['data']
        else:
            a = c
            a['restart'] = 1

        if a['restart'] == 1:
            probeJobs[c['id']] = a
            # check for each job type
            if a['job'] == "icmp":
                restart['icmp'] = 1
    
    if len(restart) == 0:
        return

    if restart.__contains__('icmp'):
        pushJobsToDB("icmp")
        restartProbe("icmp", probeProcess)

# -----------------------------------------
def mainLoop():
    """
    main scheduler loop
    """
    global scheduler
    global bConnected

    while bConnected:
        f = scheduler.step()
        time.sleep(f)

# -----------------------------------------
def trap_signal(sig, heap):
    """
    """

    global bRunning
    global bConnected
    global probeProcess

    logging.info("exit signal received, wait for next step")

    stopAllProbes(probeProcess)

    bRunning = False
    bConnected = False


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

    scheduler.add(30, getConfig)
    # scheduler.add(15, ping)
    # scheduler.add(60, showStatus)

    mainLoop()
