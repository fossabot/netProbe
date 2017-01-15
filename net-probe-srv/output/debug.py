# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-15 16:32:13 alex>
#

"""
 debug output module
"""

import logging

from .output import output

class debug(output):
    """ class to handle debug output """
    
    # ----------------------------------------------------------
    def __init__(self):
        """constructor"""

        output.__init__(self)

    # ----------------------------------------------------------
    def send(self, data):
        """send to console"""
        if data.__contains__('timestamp'):
            del data['timestamp']

        logging.info("{}".format(data))
