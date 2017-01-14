# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-20 14:52:29 alex>
#

"""
 config class
"""

import logging
import ConfigParser

import pprint

class config(object):
    """ class to manipulate the configuration """
    
    # ----------------------------------------------------------
    def __init__(self):
        """constructor

        """
        self.conf = ConfigParser.RawConfigParser()
        self.conf.read("init.cfg")

        self.scheduler = {
            'get_conf': 3600,
            'push_results': 15,
            'ping_server': 60,
            'check_probes': 30,
            'stats_probes': 60,
            'stats_push': 300,
            'upgrade': 3600*6
        }
        
        for k in self.scheduler.keys():
            try:
                self.scheduler[k] = self.conf.getint("scheduler", k)
                
            except:
                None
            
        return

    # ----------------------------------------------------------
    def get(self, section, key):
        """get a key

        """

        return self.scheduler[key]
