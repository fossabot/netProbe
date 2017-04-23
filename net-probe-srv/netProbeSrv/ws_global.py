# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-23 11:47:59 alex>
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
global function for ws
"""

from liveDB import lDB
from flask import make_response, jsonify, request

# -------------------------------------------------------------
def wsCheckParams(params):
    """check if we have wanted params"""

    for p in params:
        if p == "uid":
            if request.form.__contains__('uid') == False:
                return make_response(jsonify({"answer":"KO", "reason":"missing uid"}), 412)

        if p == "action":
            if request.form.__contains__('action') == False:
                return make_response(jsonify({"answer":"KO", "reason":"missing action"}), 412)

        if p == "hostId":
            if not request.form.__contains__('hostId'):
                return make_response(jsonify({"answer":"KO", "reason" : "missing hostId"}), 412)

        if p == "data":
            if not request.form.__contains__('data'):
                return make_response(jsonify({"answer":"KO", "reason" : "missing data"}), 412)

    return None

# -------------------------------------------------------------
def wsCheckHostUID(uid):
    """check if we have the host in database"""
    # global lDB

    host = lDB.getHostByUid(uid)

    if host == None:
        return make_response(jsonify({"answer" : "KO",
                                      "reason" : "probe not known"}), 404)

    return host
