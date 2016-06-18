# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-05 17:15:14 alex>
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
        logging.warning("{}".format(data))
