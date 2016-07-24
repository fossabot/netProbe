# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-24 21:53:10 alex>
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

@app.route('/db/getProbes', methods=['GET'])
def ws_dbGetProbes():
    """ ask for the list of the probes in the system
    """

    logging.info("/db/getProbes")

    global lDB

    p = lDB.getListProbes()

    r = {
        "answer" : "OK",
        "probes" : p
    }

    return make_response(jsonify(r), 200)
