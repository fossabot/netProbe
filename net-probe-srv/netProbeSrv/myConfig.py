# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 16:20:33 alex>
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
 jobs WS used for a probe to get its main configuration
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
import logging

# from config import conf
from ws_global import wsCheckParams, wsCheckHostUID

@app.route('/myConfig', methods=['POST'])
def ws_myconfig():
    """
    provide main configuration for the probe
    """

    logging.info("/myConfig")

    # global lDB

    _r = wsCheckParams(["uid"])
    if _r != None: return _r

    uid = int(request.form['uid'])

    host = wsCheckHostUID(uid)
    if not isinstance(host, unicode):
        return host

    config = lDB.getConfigForHost(host)

    r = {
        'probename' : config['probename'],
        'hostname' : config['hostname'],
        'firmware' : config['firmware']
    }

    return make_response(jsonify({"answer" : "OK",
                                  "config" : r}), 200)
