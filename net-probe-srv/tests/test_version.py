# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-22 23:26:16 alex>
#

import sys
import os
import nose
import json
import pprint
import time

sys.path.append(os.getcwd())
import logging

from netProbeSrv import app
from netProbeSrv import version

def test_version():
    """/version GET

    """
    global app
    c = app.test_client()
    rv = c.get("/version")

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "version GET not working"

if False:
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    test_version()
