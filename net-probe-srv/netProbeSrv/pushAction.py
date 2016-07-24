# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-24 21:53:45 alex>
#

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
    params : uid, action
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

    if action == "restart":
        r['action'] = "restart"
        lDB.updateHost(host, {"action" : "restart"})
        r['target_uid'] = uid
        return make_response(jsonify(r), 200)

    # exception
    r['answer'] = "KO"
    r['reason'] = "action not found"
    return make_response(jsonify(r), 400)
