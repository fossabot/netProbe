# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 16:24:07 alex>
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
 ping WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
# from config import conf
import time
import logging
#import pprint
from ws_global import wsCheckParams, wsCheckHostUID

@app.route('/ping', methods=['GET', 'POST'])
def ws_ping():
    """
    answers ok if everything is good
    """

    logging.info("/ping")

    global lDB
    # global conf

    r = {
        "answer" : "OK"
    }

    if request.method == 'POST':
        _r = wsCheckParams(["uid", "hostId"])
        if _r != None:
            return _r

        uid = int(request.form['uid'])

        host = wsCheckHostUID(uid)
        if not isinstance(host, unicode) and not isinstance(host, str):
            return host

        if host != request.form['hostId']:
            logging.error("bad probe {} {}".format(host, request.form['hostId']))
            return make_response(jsonify({"answer" : "bad probe matching id and hostid"}), 400)

        lDB.updateHost(host, {"last" : time.time()})

        a = lDB.getAction(host)
        if a != None:
            r['action'] = a

        return make_response(jsonify(r), 200)

    r = {
        "answer" : "KO"
    }
    
    return make_response(jsonify(r), 500)
