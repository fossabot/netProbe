# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-30 17:11:26 alex>
#

"""
 version WS
"""

from flask import make_response, jsonify
from netProbeSrv import app

aVersion = {
    "version" : "1.0.1",
    "date" : "2016/04/21",
    "author" : "Alex Chauvin"
}

@app.route('/version', methods=['GET'])
def ws_version():
    """
    version web service
    """
    global aVersion
    return make_response(jsonify(aVersion), 200)
