# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-07-17 21:33:30 alex>
#

"""
 server module for the probe system
"""

import logging

from config import conf

from output import outputer
import output

# from werkzeug.serving import WSGIRequestHandler

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting server")

conf.loadFile('1.conf')

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results
from netProbeSrv import job
from netProbeSrv import dbGetProbes, pushAction

if __name__ == '__main__':
    # WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.debug = True
    app.secret_key = 'test'
    app.run(host='0.0.0.0')
