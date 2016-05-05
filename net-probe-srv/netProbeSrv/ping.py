# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-05 14:19:19 alex>
#

"""
 ping WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
# from config import conf
import time
# import logging
#import pprint

@app.route('/ping', methods=['GET', 'POST'])
def ws_ping():
    """
    answers ok if everything is good
    """

    global lDB
    # global conf

    if request.method == 'POST':
        uid = int(request.form['uid'])

        host = lDB.getHostByUid(uid)
        if host == None:
            return make_response(jsonify({"answer" : "KO"}), 200)

        lDB.updateHost(host, {"last" : time.time()})
        # logging.info("conf : \n%s", pprint.pformat(conf.dump()))
        # logging.info("DB : \n%s", pprint.pformat(lDB.dump()))

    return make_response(jsonify({"answer" : "OK"}), 200)
