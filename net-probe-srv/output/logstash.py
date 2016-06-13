# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-12 22:59:57 alex>
#

"""
 logstash output module
"""

from .output import output

import json
import socket
import logging
import time
import datetime

class logstash(output):
    """ class to handle logstash json output """
    
    # ----------------------------------------------------------
    def __init__(self, conf):
        """constructor"""

        output.__init__(self)

        if not conf.__contains__('server'):
            assert False, "logstash configuration missing server"

        if not conf.__contains__('port'):
            assert False, "logstash configuration missing udp port"

        self.server = conf['server']
        self.iPort = int(conf['port'])

    # ----------------------------------------------------------
    def send(self, data):
        """send to logstash"""

        logging.info("send to logstash")

        # open UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        data['@timestamp'] = datetime.datetime.fromtimestamp(data['date']).isoformat()
        del data['timestamp']

        sock.sendto(str.encode(json.dumps(data)), (self.server, self.iPort))
        sock.close()

