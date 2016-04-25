# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-22 15:10:40 alex>
#

"""
 jobs WS used to manipulate jobs on the probes
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
import time
import logging
import pprint

@app.route('/myjobs', methods=['POST'])
def ws_myjobs():
    """
    provide job list to probe asking for
    """

    global lDB

    if request.method == 'POST':
        uid = int(request.form['uid'])

        host = lDB.getHostByUid(uid)
        if host == None:
            return make_response(jsonify({"answer" : "KO",
                                          "reason" : "probe not known"}), 200)

        config = lDB.getConfigForHost(host)

        # lDB.updateHost(host, {"last" : time.time()})
        # logging.info("conf : \n%s", pprint.pformat(conf.dump()))
        # logging.info("DB : \n%s", pprint.pformat(lDB.dump()))

        return make_response(jsonify({"answer" : "OK",
                                      "jobs" : config}), 200)


    return make_response(jsonify({"answer" : "KO",
                                  "reason" : "bad method used"}), 200)
