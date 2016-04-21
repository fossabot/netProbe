# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 ping WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from config import conf
import time
import logging

@app.route('/ping', methods=['GET', 'POST'])
def ws_ping():
    """
    answers ok if everything is good
    """

    global conf

    if request.method == 'POST':
        uid = int(request.form['uid'])

        host = conf.getHostByUid(uid)
        if host == None:
            return make_response(jsonify({"answer" : "KO"}), 200)

        conf.updateHost(host, {"last" : time.time()})
        # logging.info("config : %s", conf.dump())

    return make_response(jsonify({"answer" : "OK"}), 200)
