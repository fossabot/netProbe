# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-26 17:01:11 alex>
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

sys.path.append(os.getcwd())
import logging

from config import conf
from liveDB import lDB
import string

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results, upgrade
from netProbeSrv import job
from netProbeSrv import pushAction
from netProbeSrv import admin

# ---------------------------------------------
def insertConf():
    global app
    global lDB

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "True"    }  ],

        "global": {
            "firmware": {
                "current": "0.6.2",
                "prod": "0.6.2",
                "preprod" : "0.6.3",
                "test" : "0.7.0",
                "not_found" : "0.1.0"
            }
        },

        "probe" : 
        [
            {
                "id" : "7374edd8c5d8bc023f29abb8e3fffb95c5a87adb712a5ea6270292850761b33b",
                "probename" : "test01",
                "firmware" : "test"
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
def insertConf_woCurrent():
    global app
    global lDB

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "True"    }  ],

        "global": {
            "firmware": {
                "prod": "0.6.2",
                "preprod" : "0.6.3",
                "test" : "0.7.0",
                "not_found" : "0.1.0"
            }
        },

        "probe" : 
        [
            {
                "id" : "7374edd8c5d8bc023f29abb8e3fffb95c5a87adb712a5ea6270292850761b33b",
                "probename" : "test01",
                "firmware" : "test"
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
def insertOneHost(id, probename, jobs, ipv4, ipv6, version="1.0", fw="prod"):
    """check action ws with bad action

    """
    global app
    global conf

    conf.addHost( {"id" : id,
                   "probename": probename,
                   "firmware": fw,
                   "jobs" : jobs} )

    c = app.test_client()
    rv = c.post("/discover", data=dict(hostId=id,ipv4=ipv4,ipv6=ipv6,version=version))

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
def test_upgrade_1():
    """upgrade fw version with current 0.6.1 -> 0.6.2

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p1", "test_up1", aJobs, "127.2.0.1", ":2:1", "0.6.1", "current")

    rv = c.post("/upgrade", data=dict(uid=uid))

    s = rv.data
    s = s.strip()

    if s != '0.6.2':
        assert False, "bad version downloaded"

# ---------------------------------------------
def test_upgrade_2():
    """upgrade fw version with same 0.6.2 -> 0.6.2

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p2", "test_up2", aJobs, "127.2.0.2", ":2:2", "0.6.2", "current")

    rv = c.post("/upgrade", data=dict(uid=uid))

    j = json.loads(rv.data)
    if rv.status_code != 201 and j['reason'] != "no need for upgrade":
        assert False, "no need for upgrade"

# ---------------------------------------------
def test_upgrade_3():
    """upgrade fw version with prod 0.6.2 -> 0.6.2

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p3", "test_up3", aJobs, "127.2.0.3", ":2:3", "0.6.2", "prod")

    rv = c.post("/upgrade", data=dict(uid=uid))

    j = json.loads(rv.data)
    if rv.status_code != 201 and j['reason'] != "no need for upgrade":
        assert False, "no need for upgrade"

# ---------------------------------------------
def test_upgrade_4():
    """upgrade fw version with pprod 0.6.2 -> 0.6.3

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p4", "test_up4", aJobs, "127.2.0.4", ":2:4", "0.6.2", "preprod")

    rv = c.post("/upgrade", data=dict(uid=uid))

    s = rv.data
    s = s.strip()

    if s != '0.6.3':
        assert False, "bad version downloaded"

# ---------------------------------------------
def test_upgrade_5():
    """upgrade fw version with not found

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p5", "test_up5", aJobs, "127.2.0.5", ":2:5", "0.6.2", "not_found")

    rv = c.post("/upgrade", data=dict(uid=uid))

    if rv.status_code != 404:
        assert False, "file not found"

# ---------------------------------------------
def test_upgrade_6():
    """upgrade with unknown probe

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf()

    c = app.test_client()

    aJobs = [{"id" : 1,
             "job" : "health",
             "freq" : 10,
             "version" : 1,
             "data" : {}}]

    uid = insertOneHost("p6", "test_up6", aJobs, "127.2.0.6", ":2:6", "0.6.6")

    rv = c.post("/upgrade", data=dict(uid=123))

    j = json.loads(rv.data)
    if rv.status_code != 404 and j['reason'] != "probe not found":
        assert False, "probe not found"

# ---------------------------------------------
def test_upgrade_7():
    """configuration without current firmware

    """
    global app
    global conf
    global lDB

    lDB.cleanDB()

    insertConf_woCurrent()

    conf.getCurrentFWVersion()
    conf.getFWVersion('prod')
    conf.getFWVersion('unknown')

# ---------------------------------------------
def all(b=True):
    if b:
        test_upgrade_1()
        test_upgrade_2()
        test_upgrade_3()
        test_upgrade_4()
        test_upgrade_5()
        test_upgrade_6()
    test_upgrade_7()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(True)
    #all(False)

    logging.info("***** ok ******")
