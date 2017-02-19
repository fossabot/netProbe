# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-02-19 22:10:36 alex>
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
import logging
import string
import json

sys.path.append(os.getcwd())

from config import conf
from liveDB import lDB
from netProbeSrv import app
from netProbeSrv import admin
from netProbeSrv import main, ping, version, discover, results, job

# ---------------------------------------------
def test_myjobs():
    """ try to apply a missing template to a host for job
    """
    global app
    global lDB
    lDB.cleanDB()

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
                        "active" : "False"    }  ],
        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01",
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

    c = app.test_client()

    # register the probe
    rv = c.post("/discover", data=dict(hostId="temp01",ipv4="127.1.0.5",ipv6="::1",version="0.0"))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get the configuration
    rv = c.post("/myjobs", data=dict(uid=str(j['uid'])))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get a config for unknown probe
    rv = c.post("/myjobs", data=dict(uid=str(99)))
    if rv.status_code != 404:
        assert False, "should not have found this host"

    # get a config for unknown probe
    rv = c.get("/myjobs")
    if rv.status_code != 400:
        assert False, "bad request not trapped"

# ---------------------------------------------
def all_jobs(b=True):
    if b:
        test_myjobs()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all_jobs(True)

