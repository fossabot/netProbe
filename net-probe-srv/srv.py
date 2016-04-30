# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 server module for the probe system
"""

import logging

from config import conf

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover
from netProbeSrv import job

from werkzeug.serving import WSGIRequestHandler

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting server")

conf.loadFile('1.conf')

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.debug = False
    app.run(host='0.0.0.0')
