# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-03-15 14:49:30 alex>
#
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
 config class
"""

# import logging
import ConfigParser

# import pprint

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
            except Exception as ex:
                assert False, "key not found in the config file {}".format(k)
            
        return

    # ----------------------------------------------------------
    def get(self, section, key):
        """get a key

        """

        return self.scheduler[key]
