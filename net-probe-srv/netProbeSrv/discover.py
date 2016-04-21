# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-21 12:07:13 alex>
#

"""
 discover WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app
from config import conf
import time

@app.route('/discover', methods=['POST'])
def ws_discover():
    """
    discover web service
    checks host in the configuration and returns its unique id
    """
    
    global conf

    if request.method == 'POST':
        _sHostId = request.form['hostId']
        _sIpv4 = request.form['ipv4']
        _sIpv6 = request.form['ipv6']

        if conf.checkHost(_sHostId):
            _id = conf.getUniqueId(_sHostId)
            conf.updateHost(_sHostId, {'uid' : _id,
                                       'discoverTime': time.time(),
                                       'ipv4' : _sIpv4,
                                       'ipv6' : _sIpv6})

            return make_response(jsonify({"answer" : "OK",
                                          "uid" : _id}), 200)

    return make_response(jsonify({"answer" : "KO"}), 400)

