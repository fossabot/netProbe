# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-16 16:00:06 alex>
#

"""
 results WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
# from liveDB import lDB
# from config import conf
# import time
import logging
import pprint
import json
import zlib
from base64 import b64decode


@app.route('/results', methods=['POST'])
def ws_results():
    """
    answers ok if everything is good
    """

    logging.info("/results")

    # global lDB

    if request.method != 'POST':
        return make_response(jsonify({"answer" : "KO"}), 300)

    uid = int(request.form['uid'])
    fTime = float(request.form['time'])
    bCompressed = False
    if request.form['compressed'] == "yes":
        bCompressed = True

    data = []
    if bCompressed:
        s = zlib.decompress(b64decode(request.form['data']))
        data = json.loads(s)
    else:
        data.append(json.loads(b64decode(request.form['data'])))

    for d in data:
        pprint.pprint(d)

    return make_response(jsonify({"answer" : "OK"}), 200)
