# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-13 20:32:21 alex>
#

"""
 version WS
"""

import os

from flask import make_response, jsonify, request, send_from_directory
import logging
from netProbeSrv import app
from liveDB import lDB

@app.route('/upgrade', methods=['POST'])
def ws_upgrade():
    """
    upgrade web service, sends back to PI the appropriate version
    """

    logging.info("/upgrade")

    global lDB

    if request.method == 'POST':
        uid = int(request.form['uid'])

        host = lDB.getHostByUid(uid)

        if host == None:
            return make_response(jsonify({"answer" : "KO",
                                          "reason" : "probe not known"}), 401)

        sVersion = lDB.getHostVersionByUid(uid)

        if sVersion == None:
            logging.warning("probe with no version")
            return make_response(jsonify({"answer" : "KO", "reason" : "no version provided"}), 402)

        root = os.path.join(os.getcwd(), "static")

        # last version
        nextVersion = "1.3.1b"

        # what is the next version acceptable ?
        if sVersion == "1.3.1":
            nextVersion = "1.3.1b"

        fileName = "netprobe_{}_all.deb".format(nextVersion)

        logging.info("current version {}, next version {}, file static/{}".format(sVersion, nextVersion, fileName))

        # return send_from_directory(root, fileName)

        if sVersion == nextVersion:
            logging.info("no need for upgrade")
            return make_response(jsonify({"answer" : "OK",
                                          "reason" : "no need for upgrade"}), 201)

        return send_from_directory(root, fileName)
