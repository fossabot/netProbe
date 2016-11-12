# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 16:32:08 alex>
#

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

    if conf.getConfigForHost("test-01")[0]['version'] != 1:
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

    if conf.getConfigForHost("test-01")[0]['version'] != 2:
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
