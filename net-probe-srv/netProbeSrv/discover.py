# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 discover WS
"""

from flask import make_response, jsonify, request
from netProbeSrv import app

# TODO

@app.route('/discover', methods=['POST'])
def ws_discover():
    """
    discover web service
    """
    if request.method == 'POST':
        print request.form
        return make_response(jsonify({"answer" : "OK"}), 200)

    return make_response(jsonify({"answer" : "KO"}), 400)
