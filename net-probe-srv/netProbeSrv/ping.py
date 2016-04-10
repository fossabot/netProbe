# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 ping WS
"""

from flask import make_response, jsonify
from netProbeSrv import app

@app.route('/ping', methods=['GET'])
def ws_ping():
    """
    answers pong on ok
    """
    return make_response(jsonify({"answer" : "pong"}), 200)
