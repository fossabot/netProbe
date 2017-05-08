# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-30 18:32:56 alex>
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
 probe for the traceroute protocol
"""

import time
import select
import socket
import logging

from impacket import ImpactDecoder, ImpactPacket

from .probemain import probemain

# import pprint

class probe_traceroute(probemain):
    """ traceroute on TRACEROUTE class for probe
    """

    # -----------------------------------------
    def __init__(self):
        """constructor

        """
        probemain.__init__(self, "TRACEROUTE")

        self.checkNet()
        self.getConfig("traceroute", self.job_traceroute)
        self.mainLoop()

    # -----------------------------------------
    @classmethod
    def f_testv4(cls, data):
        """testing method for insertion in the job list, check if ip version 4

        """
        return data['version'] == 4

    # -----------------------------------------
    def getConfig(self, name, f, testf=None):
        """get the configuration from the database if f_testv4 passed

        """
        jobs = super(probe_traceroute, self).getConfig(name, f, self.f_testv4)
        for j in jobs:
            logging.info("add job to scheduler to target {} every {} sec".format(j['data']['target'], j['freq']))

    # -----------------------------------------
    @classmethod
    def _setValueFromConfig(cls, _config, field, default=0, _min=-1000, _max=1000):
        if _config.__contains__(field):
            r = _config[field]
            r = max(_min, r)
            r = min(_max, r)
            return r
        return default
            

    # -----------------------------------------
    def job_traceroute(self, _config):
        """traceroute job

        """
        ip = self.getIP()

        src = ip.getIfIPv4()

        target = _config['target']
        try:
            a = socket.getaddrinfo(target, None, socket.AF_INET)
            dst = a[0][4][0]
        except socket.gaierror:
            logging.error("cannot find servername {}".format(target))
            return

        logging.info("probe traceroute to {} {}".format(target, dst))

        pkt_ip = ImpactPacket.IP()
        pkt_ip.set_ip_src(src)
        pkt_ip.set_ip_dst(dst)

        if _config.__contains__('tos'):
            tos = int(_config['tos'])
            if tos > 0:
                logging.info("set tos to {}".format(tos))
                pkt_ip.set_ip_tos(tos)

        # Create a new ICMP packet of type ECHO.
        pkt_icmp = ImpactPacket.ICMP()
        pkt_icmp.set_icmp_type(pkt_icmp.ICMP_ECHO)

        # Include a payload inside the ICMP packet.
        size = 64
        if _config.__contains__('size'):
            size = int(_config['size'])

        pkt_icmp.contains(ImpactPacket.Data("A"*size))

        # Have the IP packet contain the ICMP packet (along with its payload).
        pkt_ip.contains(pkt_icmp)

        # Open a raw socket. Special permissions are usually required.
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        seq_id = int(self._setValueFromConfig(_config, 'sequence', default=3, _min=1, _max=10))
        sleep_delay = float(self._setValueFromConfig(_config, 'sleep', default=0.25, _min=0.1, _max=10))
        timeout = float(self._setValueFromConfig(_config, 'timeout', default=3, _min=0.1, _max=10))
        iRange = int(self._setValueFromConfig(_config, 'range', default=30, _min=1, _max=30))

        res_timeout = [0]*(iRange-1)
        res_ok = [0]*(iRange-1)
        avg_rtt = [0]*(iRange-1)
        min_rtt = [1000000]*(iRange-1)
        max_rtt = [-1]*(iRange-1)
        step = ['*']*(iRange-1)

        iMaxHop = 0

        for _hop in range(1, iRange):
            pkt_ip.set_ip_ttl(_hop)

            for i in range(seq_id):
                # Give the ICMP packet the next ID in the sequence.
                pkt_icmp.set_icmp_id(i)

                # Calculate its checksum.
                pkt_icmp.set_icmp_cksum(0)
                pkt_icmp.auto_checksum = 1

                now = time.time()

                # Send it to the target host.
                s.sendto(pkt_ip.get_packet(), (dst, 0))

                # Wait for incoming replies.
                if s in select.select([s], [], [], timeout)[0]:
                    reply = s.recvfrom(2000)[0]

                    d = time.time() - now
                    avg_rtt[_hop-1] += d

                    if d < min_rtt[_hop-1]:
                        min_rtt[_hop-1] = d
                        if d > max_rtt[_hop-1]:
                            max_rtt[_hop-1] = d

                    # Use ImpactDecoder to reconstruct the packet hierarchy.
                    rip = ImpactDecoder.IPDecoder().decode(reply)

                    # Extract the ICMP packet from its container (the IP packet).
                    ricmp = rip.child()
                    # print d, ricmp.get_icmp_type(), rip.get_ip_src(), ricmp.get_icmp_id()

                    # If the packet matches, report it to the user.
                    if rip.get_ip_src() == dst and rip.get_ip_dst() == src and pkt_icmp.ICMP_ECHOREPLY == ricmp.get_icmp_type() and ricmp.get_icmp_id() == i:
                        logging.debug("reply for hop {} sequence #{} {:0.2f}".format(_hop, ricmp.get_icmp_id(), d*1000))
                        res_ok[_hop-1] += 1
                        step[_hop-1] = rip.get_ip_src()

                    # If the packet matches, report it to the user.
                    if pkt_icmp.ICMP_TIMXCEED == ricmp.get_icmp_type():
                        logging.debug("TIMXCEED hop {} sequence #{} from {} {:0.2f}".format(_hop, i, rip.get_ip_src(), d*1000))
                        step[_hop-1] = rip.get_ip_src()
                        
                    if i+1 <= seq_id:
                        time.sleep(sleep_delay)

                    iMaxHop = _hop

                else:
                    logging.warning("timeout")
                    res_timeout[_hop-1] += 1
                    avg_rtt[_hop-1] += timeout

            avg_rtt[_hop-1] = (avg_rtt[_hop-1] / seq_id)
            if res_ok[_hop-1] > 0:
                break

            time.sleep(sleep_delay*2)

        result = {
            "traceroute-seq" : seq_id,
            "traceroute-target" : target,
            "traceroute-targetIP" : dst,
            "traceroute-distance": iMaxHop
        }

        for _hop in range(iMaxHop):
            try:
                hostName = socket.gethostbyaddr(step[_hop])[0]
            except Exception as ex:
                logging.debug("timeout {}".format(" ".join(str(ex.args))))
                hostName = step[_hop]
            result["traceroute-addr-{:02d}".format(_hop+1)] = step[_hop]
            result["traceroute-name-{:02d}".format(_hop+1)] = hostName

            if res_ok[_hop] > 0:
                result["traceroute-ok-{:02d}".format(_hop+1)] = res_ok[_hop]

            if res_timeout[_hop] == 0:
                result["traceroute-avg-rtt-{:02d}".format(_hop+1)] = avg_rtt[_hop]*1000
                result["traceroute-min-rtt-{:02d}".format(_hop+1)] = min_rtt[_hop]*1000
                result["traceroute-max-rtt-{:02d}".format(_hop+1)] = max_rtt[_hop]*1000
            else:
                result["traceroute-timeout-{:02d}".format(_hop+1)] = res_timeout[_hop]


        logging.info("traceroute results : {}".format(result))
        self.pushResult(result)

        if 'run_once' in _config:
            logging.info("run only once, exit")
            exit()
