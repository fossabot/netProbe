# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-05-14 18:10:04 alex>
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
 probe for the dns service
"""

import time
# import select
# import socket
import logging
import dns
import dns.resolver
import dns.exception

# import pprint

from .probemain import probemain

class probe_dns(probemain):
    """ DNS class for probe
    """

    # -----------------------------------------
    def __init__(self):
        """constructor

        """
        probemain.__init__(self, "DNS")

        self.checkNet()
        self.getConfig("dns", self.job_dns)
        self.mainLoop()

    # -----------------------------------------
    @classmethod
    def f_test(cls, data):
        """testing method for insertion in the job list, 
           check if target

        """
        if 'target' in data:
            return True

        logging.error("missing target in DNS configuration")

    # -----------------------------------------
    def getConfig(self, name, f, testf=None):
        """get the configuration from the database

        """
        jobs = super(probe_dns, self).getConfig(name, f, self.f_test)
        for j in jobs:
            logging.info("add dns job to scheduler every {} sec".format(j['freq']))

    # -----------------------------------------
    @classmethod
    def _checkEntry(cls, myResolver, qname, sServer=None, rdtype="A", proto="UDP", lifetime=1):
        """ unit dns request
        """
        if lifetime < 0:
            lifetime = 1
        if lifetime > 60:
            lifetime = 60

        if rdtype not in ["A", "MX"]:
            rdtype = "A"

        bTCP = bool(proto == "TCP")

        if sServer != None:
            myResolver.nameservers = [sServer]
        else:
            myResolver.nameservers = [myResolver.nameservers[0]]

        myResolver.lifetime = lifetime
        myResolver.timeout = myResolver.lifetime*2

        #print "nameservers ", myResolver.nameservers
        #print "timeout ", myResolver.timeout
        #print "lifetime ",myResolver.lifetime

        cache = dns.resolver.Cache()
        cache.flush()

        r = {
            'dns-error' : 'no-error',
            'dns-server': myResolver.nameservers[0],
            'dns-target': str(qname),
            'dns-rdtype': str(rdtype),
            'dns-proto': str(proto)
        }

        try:
            now = time.time()
            myAnswers = myResolver.query(qname=qname, rdtype=rdtype, tcp=bTCP)
            r['dns-response-time'] = float((time.time() - now).__format__('0.5f'))
            
            r['dns-ttl'] = myAnswers.__getattr__('ttl')

            r['dns-response'] = str(sorted(myAnswers)[0])

        except dns.resolver.NoNameservers:
            r['dns-error'] = "no name servers"
        except dns.exception.Timeout:
            r['dns-error'] = "timeout"
        except dns.resolver.NoAnswer:
            r['dns-error'] = "no answer"
        except dns.resolver.NXDOMAIN:
            r['dns-error'] = "name does not exist"
        except dns.exception.DNSException:
            r['dns-error'] = "unknown"

        return r

    # -----------------------------------------
    def job_dns(self, _config):
        """dns job

        """
        myResolver = dns.resolver.Resolver()

        if 'servers' in _config:
            sServers = _config['servers']
        else:
            sServers = [None]

        if 'type' in _config:
            rdtype = _config['type']
        else:
            rdtype = "A"

        if 'proto' in _config:
            proto = _config['proto']
        else:
            proto = "UDP"

        for s in sServers:
            result = self._checkEntry(myResolver,
                                      qname=_config['target'],
                                      sServer=s,
                                      rdtype=rdtype,
                                      proto=proto)
            #pprint.pprint(result)
            logging.info("dns results : {}".format(result))
            self.pushResult(result)

        if 'run_once' in _config:
            logging.info("run only once, exit")
            exit()
