# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:05:27 alex>
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
 logstash output module
"""

from .output import output

import json
import socket
import logging
# import time
import datetime

# import pprint

class logstash(output):
    """ class to handle logstash json output """

    T_UDP = 0
    T_TCP = 1
    aProto = ["UDP", "TCP"]
    
    # ----------------------------------------------------------
    def __init__(self, conf):
        """constructor"""

        output.__init__(self)

        if not conf.__contains__('server'):
            assert False, "logstash configuration missing server"

        if not conf.__contains__('port'):
            assert False, "logstash configuration missing udp port"

        if not conf.__contains__('transport'):
            self.transport = self.T_UDP
        else:
            if conf['transport'] == "tcp":
                self.transport = self.T_TCP
            else:
                self.transport = self.T_UDP

        self.server = conf['server']
        self.iPort = int(conf['port'])

        if conf.__contains__('fields'):
            self.fields = conf['fields'][0]
        else:
            self.fields = {}

        logging.info("output to logstash using {} towards {}:{}".format(self.aProto[self.transport], self.server, self.iPort))

    # ----------------------------------------------------------
    def send(self, _data):
        """send to logstash. build a message from the data, correct the
           timestamp and add special fields from the configuration

        """

        data = _data['data']
        
        data['@timestamp'] = datetime.datetime.fromtimestamp(_data['date']).isoformat()
        data['probe-name'] = _data['probename']
        data['probe-app'] = _data['name']

        for f in self.fields:
            data[f] = self.fields[f]

        if self.transport == self.T_UDP:
            self.sendUDP(data)
        else:
            self.sendTCP(data)

    # ----------------------------------------------------------
    def sendUDP(self, data):
        """send to logstash using UDP socket"""

        logging.info("send to logstash using UDP")

        # open UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.sendto(str.encode(json.dumps(data)), (self.server, self.iPort))
        sock.close()

    # ----------------------------------------------------------
    def sendTCP(self, data):
        """send to logstash using TCP socket"""

        logging.info("send to logstash using TCP to {}:{}".format(self.server, self.iPort))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.server, self.iPort))
            sock.send(str.encode(json.dumps(data)))
            # print str.encode(json.dumps(data))
            sock.close()
        except socket.error:
            logging.error("can't communicate with logstash")
