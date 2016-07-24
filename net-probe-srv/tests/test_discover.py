# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-24 21:19:34 alex>
#

import sys
import os
import nose
import json
import pprint
import time

sys.path.append(os.getcwd())
import logging

from config import conf
from liveDB import lDB

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results
from netProbeSrv import job
from netProbeSrv import dbGetProbes, pushAction

# ---------------------------------------------
def test_discover_get():
    """/discover GET

    """
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()
    rv = c.get("/discover")

    if rv.status != "405 METHOD NOT ALLOWED":
        assert False, "discover GET should not be allowed"

# ---------------------------------------------
def test_discover_empty():
    """/discover empty

    """
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()
    rv = c.post("/discover", data=dict())

    j = json.loads(rv.data)
    if j['answer'] != "missing argument":
        assert False, "discover empty not detected"

# ---------------------------------------------
def test_discover_1():
    """/discover 127.1.0.1 not in db

    """
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x1",ipv4="127.1.0.1",ipv6="::1"))

    j = json.loads(rv.data)
    if j['answer'] != "KO" and j['reason'] != "not found":
        assert False, "should not found this host"


# ---------------------------------------------
def test_discover_2():
    """/discover 127.1.0.2 in db

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    conf.addHost( {"id" : "x2",
                   "probename": "test_db2",
                   "jobs" : [{"id" : 1,
                              "job" : "health",
                              "freq" : 10,
                              "version" : 1,
                              "data" : {}}]})

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x2",ipv4="127.1.0.2",ipv6="::1"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

# ---------------------------------------------
def test_getProbes():
    """/db/getProbes

    """
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()
    rv = c.get("/db/getProbes")

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "db should be browsable"

# ---------------------------------------------
def test_discover_3():
    """/discover 127.1.0.3 in probe list
    check with ws getProbes

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    conf.addHost( {"id" : "x3",
                   "probename": "test_db3",
                   "jobs" : [{"id" : 1,
                              "job" : "health",
                              "freq" : 10,
                              "version" : 1,
                              "data" : {}}]})

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x3",ipv4="127.1.0.3",ipv6="::3"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    rv = c.get("/db/getProbes")

    j = json.loads(rv.data)
    if j['answer'] != "OK" or j['probes'][0]['ipv4'] != "127.1.0.3":
        assert False, "probe not found"

# ---------------------------------------------
def all(b=True):
    if b:
        test_discover_get()
        test_discover_empty()
        test_discover_1()
        test_discover_2()
        test_getProbes()
    test_discover_3()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(False)

    logging.info("***** ok ******")
