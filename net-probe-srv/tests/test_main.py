# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-13 16:06:55 alex>
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
from netProbeSrv import main

# ---------------------------------------------
def test_main():
    """get /"""
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()

    # get /
    rv = c.get("/")
    j = json.loads(rv.data)
    if j['status'] != "OK":
        assert False, "get / failed"


# ---------------------------------------------
def test_404():
    """get 404"""
    global app
    global lDB
    lDB.cleanDB()

    c = app.test_client()

    # get /unknown
    rv = c.get("/unknown")
    if rv.status_code != 404:
        assert False, "404 expected"

# ---------------------------------------------
if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.INFO)

    test_main()
    test_404()
