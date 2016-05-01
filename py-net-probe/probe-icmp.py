# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-01 12:32:53 alex>
#

"""
 probe for the icmp protocol
"""

import time
import logging
import signal
# import pprint

import sched
from netProbe import ipConf

import select
import socket
# import sys

from impacket import ImpactDecoder, ImpactPacket

_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat,
                    level=logging.INFO)

logging.info("starting probe")

config1 = [
    {"job" : "ping",
     "freq" : 15,
     "target" : "0.us.pool.ntp.org",
     "version" : 4,

     "sequence" : 3,
     "wait" : 1,
     "tos" : 0,
     "timeout" : 0.5,
     "size": 320},
    {"job" : "ping",
     "freq" : 10,
     "target" : "10.0.2.1",
     "version" : 4,
       
     "sequence" : 3,
     "wait" : 1,
     "tos" : 0,
     "timeout" : 0.025,
     "size": 32}
]

config = [
    {"job" : "ping",
     "freq" : 10,
     "target" : "10.0.2.1",
     "version" : 4,

     "sequence" : 3,
     "wait" : 1,
     "tos" : 0,
     "timeout" : 0.025,
     "size": 32}
]

#
# -----------------------------------------
def trap_signal(sig, heap):
    """
    catch the signals to handle the restart of the probe module
    """
    logging.info("exiting after signal received")

    global bRunning
    bRunning = False

#
# -----------------------------------------
def job_ping(_config):
    """
    icmp job
    """
    global ip

    src = ip.getIfIPv4()

    target = _config['target']
    try:
        a = socket.getaddrinfo(target, None, socket.AF_INET)
        dst = a[0][4][0]
    except socket.gaierror:
        logging.error("cannot find servername {}".format(target))
        return

    logging.info("probe icmp to {} {}".format(target, dst))

    pkt_ip = ImpactPacket.IP()
    pkt_ip.set_ip_src(src)
    pkt_ip.set_ip_dst(dst)

    if _config.__contains__('tos'):
        tos = int(_config['tos'])
        pkt_ip.set_ip_tos(tos)
        if tos > 0:
            logging.info("set tos to {}".format(tos))

    # Create a new ICMP packet of type ECHO.
    pkt_icmp = ImpactPacket.ICMP()
    pkt_icmp.set_icmp_type(pkt_icmp.ICMP_ECHO)

    # Include a 156-character long payload inside the ICMP packet.
    size = 64
    if _config.__contains__('size'):
        size = int(_config['size'])

    pkt_icmp.contains(ImpactPacket.Data("A"*size))

    # Have the IP packet contain the ICMP packet (along with its payload).
    pkt_ip.contains(pkt_icmp)

    # Open a raw socket. Special permissions are usually required.
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    seq_id = 3
    if _config.__contains__('sequence'):
        seq_id = int(_config['sequence'])

    sleep_delay = 1
    if _config.__contains__('sleep'):
        sleep_delay = int(_config['sleep'])

    timeout = 1
    if _config.__contains__('timeout'):
        timeout = float(_config['timeout'])

    res_timeout = 0
    res_ok = 0
    avg_rtt = 0
    min_rtt = 10000
    max_rtt = 0

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
            avg_rtt += d

            if d < min_rtt:
                min_rtt = d
            if d > max_rtt:
                max_rtt = d

            # Use ImpactDecoder to reconstruct the packet hierarchy.
            rip = ImpactDecoder.IPDecoder().decode(reply)

            # print rip.get_ip_tos()

            # Extract the ICMP packet from its container (the IP packet).
            ricmp = rip.child()

            # If the packet matches, report it to the user.
            if rip.get_ip_dst() == src and rip.get_ip_src() == dst and pkt_icmp.ICMP_ECHOREPLY == ricmp.get_icmp_type() and ricmp.get_icmp_id() == i:
                logging.info("Ping reply for sequence #{} {:0.2f}".format(ricmp.get_icmp_id(), d*1000))
                res_ok += 1

            if (i+1 <= seq_id):
                time.sleep(sleep_delay)
        
        else:
            logging.warning("timeout")
            res_timeout += 1
            avg_rtt += timeout

    avg_rtt = (avg_rtt / seq_id)

    result = {
        "seq" : seq_id,
        "ok" : res_ok,
        "target" : target,
        "targetIP" : dst,
        "timeout" : res_timeout,
        "avg_rtt" : avg_rtt * 1000,
        "min_rtt" : min_rtt * 1000,
        "max_rtt" : max_rtt * 1000
    }

    logging.info("icmp results : {}".format(result))

# -----------------------------------------
def mainLoop():
    """
    main scheduler loop
    """
    global scheduler

    while bRunning:
        f = scheduler.step()
        time.sleep(f)


# check IP configuration of probe
# if no default route !
#
ip = ipConf()

if ip.hasDefaultRoute() == False:
    logging.error("no default route, abort")
    exit(1)

# -----------------------------------------

# create global scheduler
#
scheduler = sched.sched()
scheduler.clean()

# socket.settimeout(1.0)

for c in config:
    if c['job'] == "ping":
        if c['version'] == 4:
            scheduler.add(int(c['freq']), job_ping, c)

bRunning = True

signal.signal(signal.SIGTERM, trap_signal)
signal.signal(signal.SIGINT, trap_signal)

mainLoop()

logging.info("end probe-icmp")
