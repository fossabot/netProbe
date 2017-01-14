# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-20 13:44:32 alex>
#

"""
 server WS
"""

from liveDB import lDB

from flask import Flask
from flask_apscheduler import APScheduler

import logging

class Config(object):
    JOBS = [
        {
            'id': 'cleanOldProbes',
            'func': lDB.cleanOldProbes,
            'args': None,
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_VIEWS_ENABLED = False

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()

