# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 15:05:17 alex>
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
 pushAction WS

 used to set an action to be pushed to the selected host at the next ping sequence
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
# import time
import logging

@app.route('/pushAction', methods=['POST'])
def ws_pushAction():
    """ add an action for the uid
    params : uid, action, module
    actions : restart
    """

    logging.info("/pushAction")
    global lDB

    if request.form.__contains__('uid') == False:
        return make_response(jsonify({"answer":"KO", "reason":"missing uid"}), 400)

    if request.form.__contains__('action') == False:
        return make_response(jsonify({"answer":"KO", "reason":"missing action"}), 400)

    uid = int(request.form['uid'])
    action = str(request.form['action'])

    host = lDB.getHostByUid(uid)
    if host == None:
        return make_response(jsonify({"answer":"KO", "reason":"host not found"}), 400)

    # global conf

    r = {
        "answer" : "OK"
    }

    # -------------------------
    if action == "restart":
        if request.form.__contains__('module') == False:
            return make_response(jsonify({"answer":"KO", "reason":"missing module"}), 400)

        module = str(request.form['module'])
        r['action'] = "restart"
        r['target_uid'] = uid

        sAction = { "name" : "restart" }

        if module == "all":
            sAction['args'] = { "module" : module }
            lDB.updateHost(host, {"action" : sAction })

        if module == "job":
            if request.form.__contains__('job') == False:
                return make_response(jsonify({"answer":"KO", "reason":"missing job"}), 400)

            job = str(request.form['job'])
            sAction['args'] = { "module" : module, "job" : job }

            lDB.updateHost(host, {"action" : sAction })

        return make_response(jsonify(r), 200)

    # -------------------------
    if action == "upgrade":
        sAction = { "name" : "upgrade" }
        sAction['args'] = { "when" : "now" }
        
        lDB.updateHost(host, {"action" : sAction })
        return make_response(jsonify(r), 200)

    # exception
    r['answer'] = "KO"
    r['reason'] = "action not found"
    return make_response(jsonify(r), 400)
