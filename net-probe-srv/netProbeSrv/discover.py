# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-22 20:31:04 alex>
#

"""
 discover WS
"""

from flask import make_response, jsonify, request
import time
import logging

from netProbeSrv import app
from config import conf
from liveDB import lDB


@app.route('/discover', methods=['POST'])
def ws_discover():
    """
    discover web service
    checks host in the configuration and returns its unique id
    """

    logging.info("/discover")

    global conf
    global lDB

    if request.method == 'POST':
        if not (request.form.__contains__('hostId') and 
                request.form.__contains__('ipv4') and 
                request.form.__contains__('ipv6')):
            logging.error("probe passing bad args")
            return make_response(jsonify({"answer" : "missing argument"}), 400)

        _sHostId = request.form['hostId']
        _sIpv4 = request.form['ipv4']
        _sIpv6 = request.form['ipv6']

        # if the probe is in the configuration db
        # update the probe db
        #

        if conf.checkHost(_sHostId):
            _id = lDB.getUniqueId(_sHostId)
            lDB.updateHost(_sHostId, {'uid' : _id,
                                      'discoverTime': time.time(),
                                      'last': time.time(),
                                      'ipv4' : _sIpv4,
                                      'ipv6' : _sIpv6})

            return make_response(jsonify({"answer" : "OK",
                                          "uid" : _id}), 200)
        else:
            logging.warning("probe not found {} {}".format(_sIpv4, _sIpv6))
            return make_response(jsonify({"answer" : "KO", "reason" : "not found"}), 400)

    return make_response(jsonify({"answer" : "KO", "reason" : "other"}), 400)
