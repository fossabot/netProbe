# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 server module for the probe system
"""

from config import conf

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover

from werkzeug.serving import WSGIRequestHandler

conf.loadFile('1.conf')

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.debug = True
    app.run(host='0.0.0.0')
