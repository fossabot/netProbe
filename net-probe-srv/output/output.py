# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-12 21:49:06 alex>
#

"""
 outputer
"""

# import logging

class output(object):
    """class to handle output generic

    """

    TYPE_UNKNOWN = 0
    TYPE_ELASTICSEARCH = 1
    TYPE_DEBUG = 2

    # ----------------------------------------------------------
    def __init__(self):
        """constructor

        """

        self.lKnownMethod = ("debug", "elastic", "logstash")

    # ----------------------------------------------------------
    def getMethodName(self):
        """push output valid methods"""

        for m in self.lKnownMethod:
            yield m

    # ----------------------------------------------------------
    def checkMethodName(self, name):
        """check wether method is known, from configuration"""
        try:
            self.lKnownMethod.index(name)
            return True
        except ValueError:
            return False

        return False

    # ----------------------------------------------------------
    def send(self, data):
        """send"""
        return
