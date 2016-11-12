# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-12 16:11:28 alex>
#

"""
 version WS
"""

from flask import make_response, jsonify
from netProbeSrv import app

aVersion = {
    "answer" : "OK",
    "version" : "1.3",
    "date" : "12/11/2016",
    "author" : "Alex Chauvin"
}

@app.route('/version', methods=['GET'])
def ws_version():
    """
    version web service
    """
    global aVersion
    return make_response(jsonify(aVersion), 200)
