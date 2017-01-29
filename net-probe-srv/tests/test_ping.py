# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:05:53 alex>
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

def test_ping_get():
    """/ping GET

    """
    global app
    c = app.test_client()
    rv = c.get("/ping")

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "ping GET not working"

def test_ping_put_empty():
    """/ping POST empty

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict())

    j = json.loads(rv.data)
    if j['answer'] != "missing uid":
        assert False, "missing uid not working"

def test_ping_put_ukn():
    """/ping POST unknown

    """
    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="12"))

    j = json.loads(rv.data)
    if j['answer'] != "host not found":
        assert False, "ping GET not working"

def test_pingHost_ok():
    """/ping host ok

    """
    global lDB

    lDB.cleanDB()

    lDB.updateHost("test", {'uid' : 1})

    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="1"))

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "ping known host"

def test_pingHost_ukn():
    """/ping host ukn

    """
    global lDB

    lDB.cleanDB()

    lDB.updateHost("test", {'uid' : 1})

    global app
    c = app.test_client()
    rv = c.post("/ping", data=dict(uid="2"))

    j = json.loads(rv.data)
    if j['answer'] != "host not found":
        assert False, "ping known ukn"

def test_pingUpdate():
    """/ping check update

    """
    test_pingHost_ok()
    
    global lDB
    a = lDB.dump()

    if a['test']['last'] - time.time() < -0.1:
        assert False, "not updated"

if False:
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)
    test_ping_get()
    test_ping_put_empty()
    test_ping_put_ukn()
    test_pingHost_ok()
    test_pingHost_ukn()
    test_pingUpdate()
