# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 16:54:50 alex>
#

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
def test_addHost():
    """ add host

    """
    global conf

    conf.addHost( {"id" : "xx1",
                   "probename": "test1",
                   "jobs" : []} )

    a = conf.dump()
    if not a.__contains__("xx1"):
        assert False, "add not working"

# ---------------------------------------------
def test_probename():
    """ check probename

    """
    global conf

    conf.addHost( {"id" : "xx2",
                   "probename": "test2",
                   "jobs" : []} )

    name = conf.getNameForHost("xx2")

    if name != "test2":
        assert False, "bad probename"

# ---------------------------------------------
def test_checkHost():
    """ check insertion in the db

    """
    global conf

    conf.addHost( {"id" : "xx3",
                   "probename": "test3",
                   "jobs" : []} )

    if not conf.checkHost("xx3"):
        assert False, "not found"

    if conf.checkHost("yy3"):
        assert False, "found"

# ---------------------------------------------
def test_duplicateProbeName():
    """ check duplicate probename in config

    """
    global conf

    conf.addHost( {"id" : "xx4",
                   "probename": "test3",
                   "jobs" : []} )

    if conf.checkHost("xx4"):
        assert False, "not found"

# ---------------------------------------------
def test_getConf():
    """get config for a host

    """
    global conf

    conf.addHost( {"id" : "xx5",
                   "probename": "test5",
                   "jobs" : [{"id" : 1,
                              "job" : "health",
                              "freq" : 10,
                              "version" : 1,
                              "data" : {}}]})

    a = conf.getConfigForHost("xx5")
    if a[0]['job'] != "health":
        assert False, "bad job returned"

# ---------------------------------------------
def test_active_flag():
    """ active flag on configuration
        if no flag, then active=True
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "False"    }  ],
        "probe" : [
            { "id" : "xx6",
              "probename" : "xx6",
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

    if conf.getConfigForHost("xx6")[0]['version'] != 1:
        assert False, "bad version at load"

    c = app.test_client()

    # register the probe
    rv = c.post("/discover", data=dict(hostId="xx6",ipv4="127.1.0.2",ipv6="::1",version="0.0"))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get the configuration
    rv = c.post("/myjobs", data=dict(uid=str(j['uid'])))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    if not j['jobs'][0].__contains__('active'):
        assert False, "active not present"

    if j['jobs'][0]['active'] != "True":
        assert False, "active present but not True"

    # -- change conf

    dConf = {
        "output" :  [ { "engine": "debug",
                        "parameters" : [],
                        "active" : "False"    }  ],
        "probe" : [
            { "id" : "xx6",
              "probename" : "xx6",
              "jobs" : [
                  { "id" : 1,
                    "active" : 'False',
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

    if conf.getConfigForHost("xx6")[0]['version'] != 2:
        assert False, "bad version at load"

    if conf.getConfigForHost("xx6")[0]['active'] != "False":
        assert False, "bad active status on reload"

# ---------------------------------------------
def all(b=True):
    if b:
        test_addHost()
        test_probename()
        test_checkHost()
        test_duplicateProbeName()
        test_getConf()

    test_active_flag()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(False)
