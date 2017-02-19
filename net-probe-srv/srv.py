# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-02-19 21:40:14 alex>
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
 server module for the probe system
"""

__version__ = "1.6"

import logging
import signal
import os

from config import conf

#from output import outputer
#import output

# ----------- parse args
try:
    import argparse
    parser = argparse.ArgumentParser(description='server for the raspberry probe system')

    parser.add_argument('--config', '-c', metavar='file', default='1.conf', type=str, help='configuration file', nargs='?')

    parser.add_argument('--log', '-l', metavar='level', default='INFO', type=str, help='log level', nargs='?', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    parser.add_argument('--debug', '-d', metavar='none', help='debug mode for engine', const=True, default=False, nargs='?')

    args = parser.parse_args()
    # print args

except ImportError:
    log.error('parse error')
    exit()

# ----- set the log level and format
_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logLevel = logging.INFO

if args.log == 'DEBUG':
    logLevel=logging.DEBUG
if args.log == 'WARNING':
    logLevel=logging.WARNING
if args.log == 'ERROR':
    logLevel=logging.ERROR

logging.basicConfig(format=_logFormat, level=logLevel)
# logging.basicConfig(level=logLevel)

if not isinstance(args.debug, bool):
    logging.error('debug arg is not taking argument')
    exit()

logging.info("starting server, version {}".format(__version__))
logging.debug("pid {}".format(os.getpid()))

if conf.loadFile(args.config) == False:
    logging.error('exiting')
    exit()

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover, results
from netProbeSrv import job
from netProbeSrv import pushAction, admin
from netProbeSrv import upgrade

# -----------------------------------------
def trap_HUP_signal(sig, heap):
    """ trap signal for config reload """

    global conf

    conf.reload()

signal.signal(signal.SIGHUP, trap_HUP_signal)

LOGGER = logging.getLogger('apscheduler.executors.default')
LOGGER.setLevel(logging.ERROR)
LOGGER = logging.getLogger('werkzeug')
LOGGER.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.debug = args.debug
    app.secret_key = "piprobe-{}".format(__version__)
    app.run(host='0.0.0.0')

