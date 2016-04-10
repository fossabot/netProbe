# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 server module for the probe system
"""

from netProbeSrv import app
from netProbeSrv import main, ping, version, discover

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
