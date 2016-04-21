# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-21 20:29:01 alex>
#
# pylint --rcfile=~/.pylint main.py

"""
 client module for the probe system
"""

import time
import logging

import netProbe
import sched
import hostId

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting probe")

# logging.warning("warning")
# logging.error("error")
# logging.critical("critical")
# logging.exception("in exception only")

srv = {}
bConnected = False

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
        logging.info("sleep for {:0.0f}".format(iSleepConnectDelay))
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

# create global scheduler
#
scheduler = sched.sched()

while True:
    scheduler.clean()

    serverConnect()

    scheduler.add(5, ping)
    scheduler.add(15, showStatus)

    mainLoop()
