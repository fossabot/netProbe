# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py
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
 main / WS
"""

from flask import abort, make_response, jsonify
from netProbeSrv import app

@app.route('/')
def hello_world():
    """
    / ws : do nothing
    """
    return make_response(jsonify({'status': 'OK'}), 200)

@app.errorhandler(404)
def not_found(error):
    """
    handle the 404 error
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

