# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-22 23:35:50 alex>
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

def test_discover_get():
    """/discover GET

    """
    global app
    c = app.test_client()
    rv = c.get("/discover")

    if rv.status != "405 METHOD NOT ALLOWED":
        assert False, "discover GET should not be allowed"

def test_discover_empty():
    """/discover empty

    """
    global app
    c = app.test_client()
    rv = c.post("/discover", data=dict())

    j = json.loads(rv.data)
    if j['answer'] != "missing argument":
        assert False, "discover empty not detected"

if False:
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)
    # test_discover_get()
    # test_discover_empty()
