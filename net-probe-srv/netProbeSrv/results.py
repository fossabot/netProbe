# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 14:04:47 alex>
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
 results WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from output import outputer

from liveDB import lDB
# from config import conf
# import time
import logging
# import pprint
import json
import zlib
from base64 import b64decode
import datetime

@app.route('/results', methods=['POST'])
def ws_results():
    """
    answers ok if everything is good
    """

    logging.debug("/results")

    if request.method != 'POST':
        return make_response(jsonify({"answer" : "KO"}), 300)

    uid = int(request.form['uid'])
    host = lDB.getHostByUid(uid)
    if host == None:
        logging.error("probe not known {}".format(uid))

    probename = lDB.getNameForHost(host)

    # fTime = float(request.form['time'])
    bCompressed = False
    if request.form['compressed'] == "yes":
        bCompressed = True

    data = []
    if bCompressed:
        s = zlib.decompress(b64decode(request.form['data']))
        data = json.loads(s)
    else:
        data.append(json.loads(b64decode(request.form['data'])))

    for d in data:
        d['timestamp'] = datetime.datetime.utcfromtimestamp(d['date']).isoformat()
        d['probeuid'] = uid
        d['probename'] = probename

        for o in outputer:
            o.send(d)

    return make_response(jsonify({"answer" : "OK"}), 200)
