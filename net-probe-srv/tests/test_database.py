# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:05:46 alex>
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

    # print lDB.dump()
    lDB.cleanDB()

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
    lDB.cleanDB()

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
    lDB.cleanDB()

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
    lDB.cleanDB()

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

    lDB.cleanDB()

if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)
    test_getUniqueId()
    test_getUniqueId_2()
    test_getHost()
    test_getHost_not()
    test_getHostContent()
