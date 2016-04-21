# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

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
