# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-21 15:54:17 alex>
#

"""
 results WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app, es
from liveDB import lDB
# from config import conf
# import time
import logging
import pprint
import json
import zlib
from base64 import b64decode
import datetime

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
    host = lDB.getHostByUid(uid)
    if host == None:
        logging.error("probe not known {}".format(uid))

    probename = lDB.getNameForHost(host)

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
        d['timestamp'] = datetime.datetime.utcfromtimestamp(d['date'])
        d['probeuid'] = uid
        d['probename'] = probename
        # pprint.pprint(d)
        res = es.index(index="pyprobe", doc_type='result', body=d)
        if res['created'] != True:
            logging.error("insert in ES {}".format(res))
        
    return make_response(jsonify({"answer" : "OK"}), 200)
