# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-02-19 22:10:31 alex>
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

@app.route('/myjobs', methods=['POST', 'GET'])
def ws_myjobs():
    """
    provide job list to probe asking for
    """

    logging.info("/myjobs")

    global lDB

    if request.method == 'POST':
        uid = int(request.form['uid'])

        host = lDB.getHostByUid(uid)
        if host == None:
            return make_response(jsonify({"answer" : "KO",
                                          "reason" : "probe not known"}), 404)

        jobs = lDB.getJobsForHost(host)

        conf.reload()

        return make_response(jsonify({"answer" : "OK",
                                      "jobs" : jobs}), 200)


    return make_response(jsonify({"answer" : "KO",
                                  "reason" : "bad method used"}), 400)
