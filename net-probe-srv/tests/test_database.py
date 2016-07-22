# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-22 19:45:40 alex>
#

import sys
import os
import nose

sys.path.append(os.getcwd())

import logging

from liveDB import lDB

def test_getUniqueId():
    """ test unique id

    """
    global lDB
    lDB.cleanDB()

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id"

    print lDB.dump()

def test_getUniqueId_2():
    """

    """
    global lDB

    lDB.cleanDB()

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id : {}".format(_id)

    lDB.updateHost("test", {'uid' : _id})

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id"

def test_getHost():
    """ getHostByUid

    """
    global lDB

    lDB.cleanDB()

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id"

    lDB.updateHost("test", {'uid' : _id})

    _sHost = lDB.getHostByUid(1)

    if _sHost != "test":
        assert False, "should return name of the host"

def test_getHost_not():
    """ getHostByUid return false on unknown host

    """
    global lDB

    lDB.cleanDB()

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id"

    lDB.updateHost("test", {'uid' : _id})

    _sHost = lDB.getHostByUid(2)

    if _sHost != None:
        assert False, "should return None"

def test_getHostContent():
    """ getHostContentByUid

    """
    global lDB

    lDB.cleanDB()

    _id = lDB.getUniqueId("test")

    if _id != 1:
        assert False, "should return 1 as first id"

    lDB.updateHost("test", {'uid' : _id, "a":1, "b":2})

    _sHost = lDB.getHostContentByUid(1)

    if _sHost['b'] != 2:
        assert False, "should return 2 as content of the b part"

if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)
    test_getUniqueId()
    test_getUniqueId_2()
    test_getHost()
    test_getHost_not()
    test_getHostContent()
