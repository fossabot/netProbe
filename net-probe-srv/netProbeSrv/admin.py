# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-24 22:22:08 alex>
#

"""
 admin WS

 used to pilot the server
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
#from liveDB import lDB
# import time
from config import conf
import logging

# -----------------------------------------------
@app.route('/admin/reload', methods=['POST'])
def ws_adminReload():
    """ reload configuration
    """

    logging.info("/admin/reload")

    global conf
    conf.reload()

    r = {
        "answer" : "OK"
    }

    return make_response(jsonify(r), 200)
