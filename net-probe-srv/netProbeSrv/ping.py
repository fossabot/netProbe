# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-17 22:47:07 alex>
#

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
        if not request.form.__contains__('uid'):
            return make_response(jsonify({"answer" : "missing uid"}), 400)
            
        uid = int(request.form['uid'])

        host = lDB.getHostByUid(uid)
        if host == None:
            return make_response(jsonify({"answer" : "host not found"}), 400)

        lDB.updateHost(host, {"last" : time.time()})
        # logging.info("conf : \n%s", pprint.pformat(conf.dump()))
        # logging.info("DB : \n%s", pprint.pformat(lDB.dump()))

        a = lDB.getAction(host)
        if a != None:
            r['action'] = a

    return make_response(jsonify(r), 200)
