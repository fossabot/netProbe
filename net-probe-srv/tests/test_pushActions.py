# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-10-22 12:34:34 alex>
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
def insertOneHost(id, probename, jobs, ipv4, ipv6):
    """check action ws with bad action

    """
    global app
    global conf

    conf.addHost( {"id" : id,
                   "probename": probename,
                   "jobs" : jobs} )

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId=id,ipv4=ipv4,ipv6=ipv6))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    rv = c.get("/admin/getProbes")

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "error in getProbes"

    uid = -1

    for p in j['probes']:
        if p['ipv4'] == ipv4:
            uid = p['uid']

    if uid == -1:
        assert False, "bad uid for {}".format(probename)
    
    return uid

# ---------------------------------------------
def test_push_1():
    """check action ws with bad action

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p1", "test_push1", aJobs, "127.2.0.1", ":2:1")

    rv = c.post("/pushAction", data=dict(uid=uid, action="no action"))

    j = json.loads(rv.data)
    if j['answer'] != 'KO':
        assert False, "action error"

# ---------------------------------------------
def test_push_2():
    """check action ws : restart all

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p2", "test_push2", aJobs, "127.2.0.2", ":2:2")

    rv = c.post("/pushAction", data=dict(uid=uid, action="restart", module="all"))

    j = json.loads(rv.data)
    if j['answer'] != 'OK':
        assert False, "action error {}".format(j)

    # ping the server and check the return
    rv = c.post("/ping", data=dict(uid=uid))

    j = json.loads(rv.data)

    if j['answer'] != "OK":
        assert False, "ping known host"
    a = j['action']
    if a['name'] != "restart" or type(a['args']) != dict:
        assert False, "action not in ping reply"

# ---------------------------------------------
def test_push_3():
    """check action ws : restart job health

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p3", "test_push3", aJobs, "127.2.0.3", ":2:3")

    rv = c.post("/pushAction", data=dict(uid=uid, action="restart", module="job", job="health"))

    j = json.loads(rv.data)
    if j['answer'] != 'OK':
        assert False, "action error {}".format(j)

    # ping the server and check the return
    rv = c.post("/ping", data=dict(uid=uid))

    j = json.loads(rv.data)

    if j['answer'] != "OK":
        assert False, "ping known host"
    a = j['action']
    if a['name'] != "restart" or type(a['args']) != dict:
        assert False, "action not in ping reply"

    args = a['args']
    if args['module'] != "job" or args['job'] != "health":
        assert False, "bad job to restart"

# ---------------------------------------------
def all(b=True):
    if b:
        test_push_1()
        test_push_2()
    test_push_3()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(True)

    logging.info("***** ok ******")
