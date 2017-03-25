# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 16:11:40 alex>
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
 version WS
"""

import os

from flask import make_response, jsonify, request, send_from_directory
import logging
from netProbeSrv import app
from liveDB import lDB
from ws_global import wsCheckParams, wsCheckHostUID

@app.route('/upgrade', methods=['POST'])
def ws_upgrade():
    """
    upgrade web service, sends back to PI the appropriate version
    """

    logging.info("/upgrade")

    global lDB

    if request.method == 'POST':
        _r = wsCheckParams(["uid"])
        if _r != None: return _r

        uid = int(request.form['uid'])

        host = wsCheckHostUID(uid)
        if not isinstance(host, unicode):
            return host

        sVersion = lDB.getHostVersionByUid(uid)

        if sVersion == None:
            logging.warning("probe with no version")
            return make_response(jsonify({"answer" : "KO", "reason" : "no version provided"}), 400)

        root = os.path.join(os.getcwd(), "static")

        # last version
        nextVersion = "1.5.2"

        # what is the next version acceptable ?
        if sVersion == "1.3.1":
            nextVersion = "1.3.1b"

        fileName = "netprobe_{}_all.deb".format(nextVersion)

        logging.info("current version {} for {}, next version {}, file static/{}".format(sVersion, host, nextVersion, fileName))

        # return send_from_directory(root, fileName)

        if sVersion == nextVersion:
            logging.info("no need for upgrade")
            return make_response(jsonify({"answer" : "OK",
                                          "reason" : "no need for upgrade"}), 201)

        return send_from_directory(root, fileName)
