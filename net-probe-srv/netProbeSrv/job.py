# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 15:59:06 alex>
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
 jobs WS used to manipulate jobs on the probes
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
import logging

from config import conf
from ws_global import wsCheckParams, wsCheckHostUID

@app.route('/myjobs', methods=['POST', 'GET'])
def ws_myjobs():
    """
    provide job list to probe asking for
    """

    logging.debug("/myjobs")

    # global lDB

    if request.method == 'POST':
        _r = wsCheckParams(["uid"])
        if _r != None: return _r

        uid = int(request.form['uid'])

        host = wsCheckHostUID(uid)
        if not isinstance(host, unicode):
            return host

        conf.reload()

        jobs = lDB.getJobsForHost(host)

        return make_response(jsonify({"answer" : "OK",
                                      "jobs" : jobs}), 200)


    return make_response(jsonify({"answer" : "KO",
                                  "reason" : "bad method used"}), 400)
