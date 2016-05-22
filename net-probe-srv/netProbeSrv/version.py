# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-22 23:25:12 alex>
#

"""
 version WS
"""

from flask import make_response, jsonify
from netProbeSrv import app

aVersion = {
    "answer" : "OK",
    "version" : "1.0.2",
    "date" : "2016/05/22",
    "author" : "Alex Chauvin"
}

@app.route('/version', methods=['GET'])
def ws_version():
    """
    version web service
    """
    global aVersion
    return make_response(jsonify(aVersion), 200)
