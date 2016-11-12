# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 17:32:53 alex>
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
                                          "reason" : "probe not known"}), 200)

        sVersion = lDB.getHostVersionByUid(uid)

        if sVersion == None:
            logging.warning("probe with no version")
            return make_response(jsonify({"answer" : "KO", "reason" : "no version provided"}), 400)

        root = os.path.join(os.getcwd(), "static")

        # last version
        nextVersion = "1.3.1"

        # what is the next version acceptable ?
        if sVersion == "1.3":
            nextVersion = "1.3.1"

        fileName = "netprobe_1.3.1_all.deb".format(nextVersion)

        logging.info("current version {}, next version {}, file static/{}".format(sVersion, nextVersion, fileName))

        return send_from_directory(root, fileName)
