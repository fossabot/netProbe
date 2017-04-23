# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-23 13:40:55 alex>
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

import sys
import os
import nose
import json
import pprint
import time
from base64 import b64encode
import zlib

sys.path.append(os.getcwd())
import logging

from config import conf
from liveDB import lDB

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results
from netProbeSrv import job
from netProbeSrv import pushAction
from netProbeSrv import admin

# ---------------------------------------------
def insertOneHost(id, probename, jobs, ipv4, ipv6):
    """adds one host 

    """
    global app
    global conf

    conf.addHost( {"id" : id,
                   "probename": probename,
                   "jobs" : jobs} )

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId=id,ipv4=ipv4,ipv6=ipv6,version="0.0"))

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
def test_result_nob64():
    """check push result wo base64 data

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

    uid = insertOneHost("p1", "test_res", aJobs, "127.2.0.1", ":2:1")

    # without base64
    d = {}
    rv = c.post("/results", data=dict(uid=uid, data=json.dumps(d)))

    j = json.loads(rv.data)
    if j['answer'] != 'KO':
        assert False, "action error"


# ---------------------------------------------
def test_result_1():
    """check push result

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

    uid = insertOneHost("p1", "test_res", aJobs, "127.2.0.1", ":2:1")

    d = {}

    rv = c.post("/results", data=dict(uid=uid, data=b64encode(json.dumps(d))))
    d['timestamp'] = time.time()
    rv = c.post("/results", data=dict(uid=uid, data=b64encode(json.dumps(d))))

    d['probeuid'] = "aa"
    rv = c.post("/results", data=dict(uid=uid, data=b64encode(json.dumps(d))))

    d['probename'] = "test_res"
    rv = c.post("/results", data=dict(uid=uid, data=b64encode(json.dumps(d))))

    d['date'] = time.time()
    rv = c.post("/results", data=dict(uid=uid, data=b64encode(json.dumps(d))))

    j = json.loads(rv.data)
    if j['answer'] != 'OK':
        assert False, "action error"

# ---------------------------------------------
def test_result_2():
    """check push result with compression

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

    uid = insertOneHost("p1", "test_res", aJobs, "127.2.0.1", ":2:1")

    d = {}

    d['timestamp'] = time.time()
    d['probeuid'] = "aa"
    d['probename'] = "test_res"
    d['date'] = time.time()
    rv = c.post("/results", data=dict(uid=uid, compressed="yes", data=b64encode(zlib.compress(json.dumps([d])))))

    j = json.loads(rv.data)
    print j
    if j['answer'] != 'OK':
        assert False, "action error"

# ---------------------------------------------
def test_result_nodata():
    """check push result wo data

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

    uid = insertOneHost("p1", "test_res", aJobs, "127.2.0.1", ":2:1")

    # without data
    d = {}
    rv = c.post("/results", data=dict(uid=uid))

    j = json.loads(rv.data)
    if j['answer'] != 'KO':
        assert False, "action error"

# ---------------------------------------------
def test_result_badprobe():
    """check push result bad probe

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

    uid = insertOneHost("p1", "test_res", aJobs, "127.2.0.1", ":2:1")

    # without data
    rv = c.post("/results", data=dict(uid=uid+1, data=''))

    j = json.loads(rv.data)
    print j
    if j['answer'] != 'KO':
        assert False, "action error"

# ---------------------------------------------
def all(b=True):
    if b:
        test_result_1()
        test_result_nodata()
        test_result_nob64()
        test_result_badprobe()
    test_result_2()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.DEBUG)

    all(True)

    logging.info("***** ok ******")
