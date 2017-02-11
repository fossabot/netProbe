# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 15:12:36 alex>
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
from netProbeSrv import pushAction, admin

# ---------------------------------------------
def test_admin_reload():
    """/admin/reload

    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "False"    }  ],
        "probe" : [
            { "id" : "test-01",
              "probename" : "test-01",
              "jobs" : [
                  { "id" : 1,
                    "job" : "health",
                    "freq" : 15,
                    "version" : 1,
                    "data" : {}
                }
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

    if conf.getJobsForHost("test-01")[0]['version'] != 1:
        assert False, "bad version at load"

    c = app.test_client()

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "False"    }  ],
        "probe" : [
            { "id" : "test-01",
              "probename" : "test-01",
              "jobs" : [
                  { "id" : 1,
                    "job" : "health",
                    "freq" : 15,
                    "version" : 2,
                    "data" : {}
                }
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

    rv = c.post("/admin/reload", data=dict())

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "reload not working"

    print conf.dump()

    if conf.getJobsForHost("test-01")[0]['version'] != 2:
        assert False, "bad version at load"

# ---------------------------------------------
def all(b=True):
    if b:
        None
    test_admin_reload()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(False)

    logging.info("***** ok ******")
