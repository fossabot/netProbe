# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 16:22:50 alex>
#

"""
 version WS
"""

from flask import make_response, jsonify
from netProbeSrv import app

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

        return app.send_static_file('netprobe_1.3.1_all.deb')
