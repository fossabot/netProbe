# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-26 16:57:15 alex>
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

    if conf.getNameForHost("xx2_ukn") != "unknown":
        assert False, "bad probename ukn"

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
                   "probename": "test4.0",
                   "jobs" : []} )

    conf.addHost( {"id" : "xx4",
                   "probename": "test4.1",
                   "jobs" : []} )

    name = conf.getNameForHost("xx4")

    if name != "test4.1":
        assert False, "bad probename for duplicate"

# ---------------------------------------------
def test_duplicateProbeId():
    """ check duplicate id in config

    """
    global conf

    conf.addHost( {"id" : "xx5",
                   "probename": "test5.0",
                   "jobs" : []} )

    conf.addHost( {"id" : "xx5.1",
                   "probename": "test5.0",
                   "jobs" : []} )

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

    a = conf.getJobsForHost("xx5")
    if a[0]['job'] != "health":
        assert False, "bad job returned"

    if conf.getJobsForHost("xx5_ukn") != None:
        assert False, "should not return jobs"

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
                        "active" : "True"    }  ],
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

    if conf.getJobsForHost("xx6")[0]['version'] != 1:
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

    if conf.getJobsForHost("xx6")[0]['version'] != 2:
        assert False, "bad version at load"

    if conf.getJobsForHost("xx6")[0]['active'] != "False":
        assert False, "bad active status on reload"

# ---------------------------------------------
def test_template01():
    """ apply a template to a host for job
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

    print("templates: {}".format(", ".join(conf.getListTemplate())))    

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

    job = j['jobs'][0]

    if not job.__contains__('active'):
        assert False, "active not present"

    if job['active'] != "True":
        assert False, "active present but not True"

    if job['job'] != "health":
        assert False, "job should be health"

    if job['freq'] != 15:
        assert False, "job frequency should be 15"

    if job['id'] != 1000:
        assert False, "job id should be 1000"

# ---------------------------------------------
def test_template02():
    """ multiple templates, 3 hosts with one, another or both
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
                        "freq" : 101,
                        "version" : 1,
                        "data" : {}
                    }
                ]
            },
            { 
                "name": "T02",
                "jobs" : [
                    { 
                        "active": "True",
                        "job" : "health",
                        "freq" : 102,
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
          }, 
            {
                "id" : "temp02",
                "probename" : "temp02",
                "template" : [
                    "T02"
                ]
            },
            
            {
                "id" : "temp03",
                "probename" : "temp03",
                "template" : [
                    "T01", "T02"
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
    rv = c.post("/discover", data=dict(hostId="temp01",ipv4="127.1.0.6",ipv6="::1",version="0.0"))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get the configuration
    rv = c.post("/myjobs", data=dict(uid=str(j['uid'])))
    j = json.loads(rv.data)

    if j['answer'] != "OK":
        assert False, "should have found this host"

    job = j['jobs'][0]

    if job['freq'] != 101:
        assert False, "job for temp01 should have freq 101"

    if job['id'] != 1000:
        assert False, "job for temp01 id != 1000"

    # register the probe
    rv = c.post("/discover", data=dict(hostId="temp02",ipv4="127.1.0.7",ipv6="::1",version="0.0"))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get the configuration
    rv = c.post("/myjobs", data=dict(uid=str(j['uid'])))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    job = j['jobs'][0]

    if job['freq'] != 102:
        assert False, "job for temp02 should have freq 102"

    if job['id'] != 1001:
        assert False, "job for temp02 id != 1001"

    # register the probe
    rv = c.post("/discover", data=dict(hostId="temp03",ipv4="127.1.0.8",ipv6="::1",version="0.0"))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    # get the configuration
    rv = c.post("/myjobs", data=dict(uid=str(j['uid'])))
    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "should have found this host"

    job = j['jobs'][0]

    if j['jobs'][0]['freq'] != 101:
        assert False, "job #1 for temp03 should have freq 101"

    if j['jobs'][1]['freq'] != 102:
        assert False, "job #2 for temp03 should have freq 101"

    if j['jobs'][0]['id'] != 1002:
        assert False, "job #1 for temp03 id != 1002"
    if j['jobs'][1]['id'] != 1003:
        assert False, "job #2 for temp03 id != 1003"

    # for coverage
    list(conf.getListProbes()) 

# ---------------------------------------------
def test_template_missing():
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
                  "T_missing"
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

    if j['jobs'] != {}:
        assert False, "should not have template set {}".format(j['jobs'])

# ---------------------------------------------
def test_template_noname():
    """ template without name
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "template" : 
        [
            { 
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
    try:
        conf.loadFile('test_config.conf')
    except:
        return

    assert False, "should have a name in a template section"

# ---------------------------------------------
def test_template_empty():
    """ try to create an empty template configuration
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "template" : [],

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

# ---------------------------------------------
def test_noprobe():
    """ no probe in the configuration
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
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

    try:
        conf.loadFile('test_config.conf')
    except:
        return

    assert False, "test for no probe"

# ---------------------------------------------
def test_probeNoName():
    """ coverage test for probe without name section

    """
    global conf

    conf.addHost( {"id" : "xx7",
                   "jobs" : []} )

# ---------------------------------------------
def test_noConfig():
    """ coverage test for host not in config

    """
    global conf

    conf.addHost( {"id" : "xx8",
                   "probename": "test8",
                   "jobs" : []} )

    if conf.getConfigForHost("xx9_unknonw") != None:
        assert False, "should not have found host"

# ---------------------------------------------
def test_noFile():
    """ try to load a non missing file

    """
    global conf

    try:
        conf.reload()
    except:
        None

    if conf.loadFile('test_config_no.conf') != False:
        assert False, "should not have loaded config file"

# ---------------------------------------------
def test_template_2loads():
    """ load twice the conf
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
                        "active" : "True"    }  ],
        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01",
              "hostname" : "host",
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
    conf.loadFile('test_config.conf')

# ---------------------------------------------
def test_engine_ukn():
    """ unknown engine in conf
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "output" :  [ { "engine": "ukn",
                        "parameters" : [],
                        "active" : "True"    }  ],
        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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
    try:
        conf.loadFile('test_config.conf')
    except:
        return

    assert False, "unknown output"

# ---------------------------------------------
def test_template_nojobs():
    """ template without job def
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "template" : 
        [
            { 
                "name": "T01"
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

# ---------------------------------------------
def test_outputers():
    """ coverage for outputers
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "output" :  [
            { "engine": "debug",
              "parameters" : [],
              "active" : "True" },

            { "engine" : "logstash",
              "parameters" : [
                  {
                      "server" : "127.0.0.1",
                      "port" : 55514,
                      "transport" : "udp",
                      "fields" : [
                          {
                              "ES_environnement" : "PROD"
                          }
                      ]
                  }
              ],
              "active" : "True"
          }

        ],

        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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
    try:
        conf.loadFile('test_config.conf')
    except:
        None

    dConf = {
        "output" :  [
            { "engine": "elastic",
              "parameters" : [
                {
                    "server" : "127.0.0.1",
                    "index" : "pyprobe",
                    "shard" : 5,
                    "replica" : 0
                } 
              ],
              "active" : "True"
            }

        ],

        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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

    try:
        conf.loadFile('test_config.conf')
    except:
        return

# ---------------------------------------------
def test_outputers_empty():
    """ coverage for outputers without parameters
    """
    global app
    global lDB
    lDB.cleanDB()

    dConf = {
        "output" :  [
            { "engine": "debug",
              "parameters" : [],
              "active" : "True" },

            { "engine": "elastic",
              "active" : "True"
            },

            { "engine" : "logstash",
              "active" : "True"
          }

        ],

        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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

    try:
        conf.loadFile('test_config.conf')
    except:
        None

    dConf = {
        "output" :  [
            { "engine" : "logstash",
              "active" : "True"
          }

        ],

        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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

    try:
        conf.loadFile('test_config.conf')
    except:
        None

    dConf = {
        "probe" : [
            { "id" : "temp01",
              "probename" : "temp01"
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

    try:
        conf.loadFile('test_config.conf')
    except:
        return

# ---------------------------------------------
def test_template_syntaxerror():
    """ check template syntax error trap
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
    sConf = string.replace(sConf, "],", ']')

    try:
        f = file("test_config.conf", 'w')
    except IOError:
        logging.error("accessing config file {}".format(sFile))
        return False
        
    f.write(sConf)
    f.close()

    global conf

    try:
        conf.loadFile('test_config.conf')
    except Exception as ex:
        return

    assert False, "configuration syntax error not trapped"

# ---------------------------------------------
def all_config(b=True):
    if b:
        test_noFile()
        test_addHost()
        test_probename()
        test_checkHost()
        test_getConf()
        test_active_flag()
        test_template01()
        test_template02()
        test_duplicateProbeName()
        test_template_missing()
        test_template_noname()
        test_template_empty()
        test_noprobe()
        test_duplicateProbeId()
        test_probeNoName()
        test_noConfig()
        test_template_nojobs()
        test_template_2loads()
        test_engine_ukn()
        test_outputers()
        test_outputers_empty()
    test_template_syntaxerror()


# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all_config(True)
    #all_config(False)


""" coverage result

config/config.py            150     13    91%   229-233, 236-243, 255, 270-271, 298

"""
