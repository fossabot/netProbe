# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-22 20:32:41 alex>
#

import sys
import os
import nose

sys.path.append(os.getcwd())

from config import conf

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

def test_duplicateProbeName():
    """ check duplicate probename in config

    """
    global conf

    conf.addHost( {"id" : "xx4",
                   "probename": "test3",
                   "jobs" : []} )

    if conf.checkHost("xx4"):
        assert False, "not found"

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
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)
    test_addHost()
    test_probename()
    test_checkHost()
    test_duplicateProbeName()
    test_getConf()
