# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 client module for the probe system
"""

import time

import netProbe
import sched
import hostId

# check IP configuration of probe
# if no default route !
#
ip = netProbe.ipConf()

if ip.hasDefaultRoute() == False:
    print "no default route, abort"
    exit(1)
else:
    print "INFO : ip route OK"

# get hostId
#
hid = hostId.hostId(ip.getLinkAddr())

# connect to probe server
#

srv = netProbe.probeServer()

if srv.findServer():
    print "INFO : srv found"
else:
    print "ERROR : server not found"
    exit(2)

if srv.ping() == False:
    print "ERROR : service ping not working"
    exit(1)

# send identification to get certificate
#
srv.discover(hid.get(), ip.getIfIPv4(), ip.getIfIPv6())

#
# -----------------------------------------
def ping():
    """
    call the ping ws of the server
    called by the scheduler
    """
    if srv.ping():
        print "INFO delta time = {:0.2f}ms".format(srv.getLastCmdDeltaTime()*1000)

# -----------------------------------------
def showStatus():
    """
    called by the scheduler in order to print if the server is available
    """
    if srv.getStatus() == False:
        print "WARNING : server not available"
    else:
        print "INFO : server up and alive"

# create global scheduler
#
scheduler = sched.sched()

scheduler.add(5, ping)
scheduler.add(15, showStatus)

while True:
    f = scheduler.step()
    time.sleep(f)
