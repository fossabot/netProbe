# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-13 15:58:52 alex>
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
import string


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
def installConfig():
    dConf = {
        "template" : 
        [
            { 
                "name": "T01",
                "jobs" : [
                    { 
                        "active": "True",
                        "job" : "health",
                        "freq" : 15,
                        "version" : 1,
                        "data" : {}
                    }
                ]
            }
        ],

        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "True"    }  ],
        "probe" : [
            { "id" : "__temp01",
              "probename" : "__temp01",
              "template" : [
                  "T01"
              ]
          }
        ]
    }

    sConf = string.replace(str(dConf), "'", '"')

    try:
        f = file("test_config.conf", 'w')
    except IOError:
        logging.error("accessing config file {}".format(sFile))
        return False
        
    f.write(sConf)
    f.close()

    global conf
    conf.loadFile('test_config.conf')

# ---------------------------------------------
def test_discover_get():
    """/discover GET

    """
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()
    rv = c.get("/discover")

    print rv.status

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

    installConfig()

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x1",ipv4="127.1.0.1",ipv6="::1",version="0.0"))

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

    installConfig()

    conf.addHost( {"id" : "x2",
                   "probename": "test_db2",
                   "jobs" : [{"id" : 1,
                              "job" : "health",
                              "freq" : 10,
                              "version" : 1,
                              "data" : {}}]})

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x2",ipv4="127.1.0.2",ipv6="::1",version="0.0"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

# ---------------------------------------------
def test_getProbes():
    """/admin/getProbes

    """
    global app
    global lDB

    # clean DB first
    lDB.cleanDB()

    c = app.test_client()
    rv = c.get("/admin/getProbes")

    j = json.loads(rv.data)
    if not j.__contains__('answer'):
        print(j)
        assert False, "no answer"

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
    rv = c.post("/discover", data=dict(hostId="x3",ipv4="127.1.0.3",ipv6="::3",version="0.0"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    rv = c.get("/admin/getProbes")

    j = json.loads(rv.data)
    if j['answer'] != "OK" or j['probes'][0]['ipv4'] != "127.1.0.3":
        assert False, "probe not found"

# ---------------------------------------------
def test_discover_4():
    """/discover 127.1.0.4 in probe list with good version
    check with ws getProbes

    """
    global app
    global conf
    global lDB
    lDB.cleanDB()

    conf.addHost( {"id" : "x4",
                   "probename": "test_db4",
                   "jobs" : [{"id" : 1,
                              "job" : "health",
                              "freq" : 10,
                              "version" : 1,
                              "data" : {}}]})

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId="x4",ipv4="127.1.0.4",ipv6="::4",version="1.3"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    rv = c.get("/admin/getProbes")

    j = json.loads(rv.data)
    if j['answer'] != "OK" or j['probes'][0]['version'] != "1.3":
        assert False, "probe not found with good version"

# ---------------------------------------------
def all(b=True):
    if b:
        test_discover_get()
        test_discover_empty()
        test_discover_1()
        test_discover_2()
        test_getProbes()
        test_discover_3()
        test_getProbes()
    test_discover_4()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(True)

    logging.info("***** ok ******")
