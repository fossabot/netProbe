# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 16:32:57 alex>
#

"""
 admin WS

 used to pilot the server
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from liveDB import lDB
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

# -----------------------------------------------
@app.route('/admin/getProbes', methods=['GET'])
def ws_dbGetProbes():
    """ ask for the list of the probes in the system
    """

    logging.info("/admin/getProbes")

    global lDB

    p = lDB.getListProbes()

    r = {
        "answer" : "OK",
        "probes" : p
    }

    return make_response(jsonify(r), 200)
