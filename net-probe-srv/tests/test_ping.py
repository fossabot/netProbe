# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-13 16:23:30 alex>
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

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results
from netProbeSrv import job

# ---------------------------------------------
def test_ping_get():
    """/ping GET

    """
    global app
    c = app.test_client()
    rv = c.get("/ping")

    if rv.status_code != 500:
        assert False, "ping GET working"

# ---------------------------------------------
def test_ping_put_empty():
    """/ping POST empty

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict())

    j = json.loads(rv.data)
    if j['answer'] != "missing uid":
        assert False, "missing uid not working"

# ---------------------------------------------
def test_ping_put_ukn():
    """/ping POST unknown

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="12", hostId="test"))

    j = json.loads(rv.data)
    if rv.status_code != 404 and j['answer'] != "host not found":
        assert False, "ping POST ukn not working"


# ---------------------------------------------
def test_ping_no_host():
    """/ping without host parameter

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="12"))

    j = json.loads(rv.data)
    # print j, rv.status_code
    if rv.status_code != 400 and j['answer'] != "missing hostId":
        assert False, "ping missing host id not working"

# ---------------------------------------------
def test_pingHost_ok():
    """/ping host ok

    """

    global conf
    conf.addHost( {"id" : "xx1",
                   "probename": "test",
                   "jobs" : []} )
    global lDB

    lDB.cleanDB()

    lDB.updateHost("xx1", {'uid' : 1})

    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="1", hostId="xx1"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "ping known host"

# ---------------------------------------------
def test_pingHost_ukn():
    """/ping host ukn

    """
    global lDB

    lDB.cleanDB()
    lDB.updateHost("xx1", {'uid' : 1})

    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="1", hostId="xx2"))

    j = json.loads(rv.data)
    if j['answer'] != "bad probe matching id and hostid":
        assert False, "ping known ukn id"

# ---------------------------------------------
def test_ping_bad_hostid():
    """/ping with bad hostid

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="1", hostId="xx2"))

    j = json.loads(rv.data)
    if j['answer'] != "bad probe matching id and hostid":
        assert False, "ping with bad hostid"

# ---------------------------------------------
def test_pingUpdate():
    """/ping check update

    """
    test_pingHost_ok()
    
    global lDB
    a = lDB.dump()

    if a['xx1']['last'] - time.time() < -0.1:
        assert False, "not updated"

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    # test_ping_get()
    test_ping_put_empty()
    test_ping_put_ukn()
    test_pingHost_ok()
    test_pingHost_ukn()
    test_pingUpdate()
    test_ping_bad_hostid()
    test_ping_no_host()
    test_ping_get()
