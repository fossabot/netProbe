# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-05 22:06:26 alex>
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
 discover WS
"""

from flask import make_response, jsonify, request
import time
import datetime
import logging

from netProbeSrv import app
from config import conf
from liveDB import lDB
from output import outputer


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
                request.form.__contains__('ipv6') and
                request.form.__contains__('version') ):
            logging.error("probe passing bad args")
            return make_response(jsonify({"answer" : "missing argument"}), 400)

        _sHostId = request.form['hostId']
        _sIpv4 = request.form['ipv4']
        _sIpv6 = request.form['ipv6']
        _sVersion = request.form['version']

        # if the probe is in the configuration db
        # update the probe db
        #

        if conf.checkHost(_sHostId):
            _id = lDB.getUniqueId(_sHostId)
            _hostConf = conf.getConfigForHost(_sHostId)

            lDB.updateHost(_sHostId, {'uid' : _id,
                                      'discoverTime': time.time(),
                                      'last': time.time(),
                                      'ipv4' : _sIpv4,
                                      'ipv6' : _sIpv6,
                                      'version' : _sVersion,
                                      'name': _hostConf['probename']})

            # push to outputer
            data = {}

            d = {}
            d['timestamp'] = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
            d['probe_ipv4'] = str(_sIpv4)
            d['probe_ipv6'] = str(_sIpv6)
            d['probe_version'] = str(_sVersion)
            d['probe_hostid'] = str(_sHostId)

            data['date'] = time.time()
            data['probename'] = _hostConf['probename']
            data['probeuid'] = _id
            data['name'] = str('DISCOVER')

            data['data'] = d

            for o in outputer:
                o.send(data)

            return make_response(jsonify({"answer" : "OK",
                                          "uid" : _id}), 200)
        else:
            logging.warning("probe not found {} {}".format(_sIpv4, _sIpv6))

            # push to outputer
            data = {}

            d = {}
            d['timestamp'] = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
            d['probe_ipv4'] = str(_sIpv4)
            d['probe_ipv6'] = str(_sIpv6)
            d['probe_version'] = str(_sVersion)
            d['probe_hostid'] = str(_sHostId)

            data['date'] = time.time()
            data['probename'] = str('unknown')
            data['probeuid'] = int(0)
            data['name'] = str('DISCOVER')

            data['data'] = d

            for o in outputer:
                o.send(data)

            # inform probe
            return make_response(jsonify({"answer" : "KO", "reason" : "not found"}), 404)

    return make_response(jsonify({"answer" : "KO", "reason" : "other"}), 400)
