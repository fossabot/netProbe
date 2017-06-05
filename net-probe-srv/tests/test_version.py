# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-06-05 18:58:38 alex>
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

sys.path.append(os.getcwd())
import logging

from netProbeSrv import app
from netProbeSrv import version

from netProbeSrv import libUpgrade

# ---------------------------------------------
def test_version():
    """/version GET

    """
    global app
    c = app.test_client()
    rv = c.get("/version")

    j = json.loads(rv.data)
    if j['answer'] != "OK":
        assert False, "version GET not working"

# ---------------------------------------------
def test_lib_01():
    """ version to int"""
    if libUpgrade.versionToInt("1.2.3") == 0:
        assert False, "version to int 1.2.3"

    if libUpgrade.versionToInt("1.2") == 0:
        assert False, "version to int 1.2"

    if libUpgrade.versionToInt("test") != 0:
        assert False, "version to int test"

# ---------------------------------------------
def test_lib_02():
    """ def next version"""
    s=libUpgrade.defNextVersion("1.2.3", "1.9.0")
    if s != "1.9.0":
        assert False, "next version {} != 1.9.0".format(s)

    s = libUpgrade.defNextVersion("1.2.3", "1.2.2")
    if s != "1.2.3":
        assert False, "next version {} != 1.2.3".format(s)

    s = libUpgrade.defNextVersion("1.2.3", "1.8.0")
    if s != "1.8.0":
        assert False, "next version {} != 1.8.0".format(s)

    s = libUpgrade.defNextVersion("1.9.0","1.10.0")
    if s != "1.9.1":
        assert False, "next version {} != 1.9.1".format(s)

    s = libUpgrade.defNextVersion("1.9.1", "1.10.0")
    if s != "1.9.2":
        assert False, "next version {} != 1.9.2".format(s)

    s = libUpgrade.defNextVersion("99.0.1", "99.0.2")
    if s != "99.0.2":
        assert False, "next version {} != 99.0.2".format(s)


# ---------------------------------------------
def all(b=True):
    if b:
        test_version()
        test_lib_01()
    test_lib_02()

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    all(False)
