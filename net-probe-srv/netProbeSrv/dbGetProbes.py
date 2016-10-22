# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-10-22 12:32:42 alex>
#

"""
 getProbes

 returns the list of the probes
"""

from flask import make_response, jsonify
from netProbeSrv import app
from liveDB import lDB
# import time
import logging

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
