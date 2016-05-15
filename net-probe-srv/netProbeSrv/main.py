# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

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
    return 'Hello World!'


@app.route('/post/<int:post_id>', methods=['GET'])
def show_post(post_id):
    """
    show the post with the given id, the id is an integer
    """
    if post_id == 0:
        abort(404)
    return 'Post %d' % post_id

@app.errorhandler(404)
def not_found(error):
    """
    handle the 404 error
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

