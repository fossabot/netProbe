# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 16:15:48 alex>
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

"""
 admin WS

 used to pilot the server
"""

# from flask import make_response, jsonify, request
from flask import make_response, jsonify
from netProbeSrv import app
from liveDB import lDB
# import time
from config import conf
import logging

# -----------------------------------------------
@app.route('/admin/reload', methods=['POST'])
def ws_adminReload():
    """ reload configuration
    """

    logging.info("/admin/reload")

    # global conf

    conf.reload()

    r = {
        "answer" : "OK"
    }

    return make_response(jsonify(r), 200)

# -----------------------------------------------
@app.route('/admin/getProbes', methods=['GET'])
def ws_dbGetProbes():
    """ ask for the list of the probes in the system
    """

    logging.info("/admin/getProbes")

    # global lDB

    p = lDB.getListProbes()

    r = {
        "answer" : "OK",
        "probes" : p
    }

    return make_response(jsonify(r), 200)
