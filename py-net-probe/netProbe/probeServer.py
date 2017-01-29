# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:01:25 alex>
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
Manages communication with the central server

>>> import netProbe
>>> srv = netProbe.probeServer()
>>> srv.findServer()
True
>>> srv.ping()
True
"""

import socket
import requests
import time
import json
import logging
# import pprint
import zlib
from base64 import b64encode
import os
import re
import time
from subprocess import call,check_output, CalledProcessError

class probeServer(object):
    """class to talk to the probe server"""
	
    def __init__(self):
        """
        constructor
        """
        self.sServerName = ""
        self.iServerPort = 5000
        self.sPingURL = ""
        self.sSrvBaseURL = ""
        self.bServerAvail = False
        self.lastCmdRespTime = 0
        self.uid = 0

        if True:
            self.session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=2,
                                                    pool_maxsize=4)
            self.session.mount('http', adapter)

        else:
            self.session = requests

    # -----------------------------------------------------------------
    def findServer(self):
        """
        check which server host to contact
        based on server names
           net-probe-srv-prod
           net-probe-srv
           probe-srv
        """
        for server in ['net-probe-srv-prod',
                       'net-probe-srv',
                       'probe-srv']:
            try:
                socket.getaddrinfo(server, 80)
                self.sServerName = server
                break
            except socket.gaierror:
                logging.error("cannot find servername {}".format(server))

        if self.sServerName == "":
            logging.error("no suitable server to talk to")
            return False

        self.sSrvBaseURL = "http://{}:{}".format(self.sServerName,
                                                 self.iServerPort)

        return True

    # -----------------------------------------------------------------
    def ping(self):
        """
        calls the ping web service on the selected server in order
        to know if it is available for other transaction
        gather the response time and store the server status

        this channel is used by the server to push actions

        returns None or structure with action
        """
        if self.bServerAvail == False:
            self.uid = 0

        if self.sServerName == "":
            return None

        if self.sPingURL == "":
            self.sPingURL = self.sSrvBaseURL+'/ping'
            
        delta = -1

        dReturn = { 'status' : 'OK' }

        try:
            now = time.time()
            if self.uid > 0:
                data = {
                    'uid' : self.uid
                }
                r = self.session.post(self.sPingURL, data)
                if r.status_code == 200:
                    delta = time.time() - now
                    s = json.loads(r.text)
                    if s.__contains__('answer') and s['answer'] != "OK":
                        self.bServerAvail = False
                        return None

                    # action in the return ?
                    if s.__contains__('action'):
                        dReturn['action'] = s['action']
            else:
                self.session.get(self.sPingURL)
                delta = time.time() - now

            self.lastCmdRespTime = delta
            self.bServerAvail = True
        except requests.ConnectionError:
            logging.error("reaching srv : connection refused")
            self.bServerAvail = False
            return None

        return dReturn

    # -----------------------------------------------------------------
    def getLastCmdDeltaTime(self):
        """
        returns last command response time in seconds
        """
        return self.lastCmdRespTime

    # -----------------------------------------------------------------
    def getStatus(self):
        """
        returns communication with server status
        """
        return self.bServerAvail

    # -----------------------------------------------------------------
    def discover(self, sHostId, sIpV4, sIpV6, sVersion):
        """
        calls the discover web service on the server in order to
        announce the probe itself
        if the probe is known... TODO
        :param sHostId: hostid string to uniquely identify the probe
        :param sIpV4: IP v4 address of the probe
        :param sIpV6: IP v6 address of the probe
        :param sVersion: current version of the probe software
        """

        data = {
            'hostId':sHostId,
            'ipv4':sIpV4,
            'ipv6':sIpV6,
            'version':sVersion
        }

        req = self.sSrvBaseURL+'/discover'

        try:
            r = self.session.post(req, data, timeout=2)
        except:
            logging.error("reaching srv : connection refused")
            self.bServerAvail = False
            return False

        if r.status_code == 200:
            s = json.loads(r.text)
            if s.__contains__('uid') and s.__contains__('answer') and s['answer'] == "OK":
                self.uid = s['uid']
                self.bServerAvail = True
                logging.info("my id is {}".format(self.uid))
                return True
            else:
                logging.error("bad response from server, missing uid")

        self.bServerAvail = False
        return False

    # -----------------------------------------------------------------
    def getConfig(self):
        """
        get configuration for this probe from server
        """

        if self.bServerAvail == False or self.uid == 0:
            return None

        try:
            data = {
                'uid' : self.uid
            }

            r = self.session.post(self.sSrvBaseURL+'/myjobs', data)
            
            if r.status_code == 200:
                s = json.loads(r.text)
                if s.__contains__('answer') and s['answer'] != "OK":
                    if s.__contains__('reason'):
                        logging.error("bad answer from job ws : {}".format(s['reason']))
                    self.bServerAvail = False
                    return None

                if s.__contains__('jobs'):
                    return s['jobs']

        except requests.ConnectionError:
            logging.error("get jobs : connection error")
            return None

        return None

    # -----------------------------------------------------------------
    def pushResults(self, aResult):
        """push results to the server
        aResult should be an array
        """

        if not isinstance(aResult, list):
            raise Exception("pushResult not provided an array")
        
        if self.bServerAvail == False or self.uid == 0:
            return None

        data = {
            "uid" : self.uid,
            "time" : time.time()
        }

        if len(aResult) > 1:
            data['compressed'] = "yes"
            data['data'] = b64encode(zlib.compress(json.dumps(aResult)))
        else:
            data['compressed'] = "no"
            data['data'] = b64encode(json.dumps(aResult[0]))

        try:
            r = self.session.post(self.sSrvBaseURL+'/results', data)
            
            if r.status_code == 200:
                s = json.loads(r.text)
                if s.__contains__('answer') and s['answer'] != "OK":
                    if s.__contains__('reason'):
                        logging.error("bad answer from result ws : {}".format(s['reason']))
                    self.bServerAvail = False
                    return None

        except requests.ConnectionError:
            logging.error("push results : connection error")
            return None

        return True

    # -----------------------------------------------------------------
    def upgrade(self):
        """upgrade the software
        """

        logging.info("check for software upgrade")
        s = check_output(["uname", "-m"])
        if re.match("arm", s) == None:
            logging.info(" avoid on non ARM platform")
            return

        try:
            data = {
                'uid' : self.uid
            }
            r = self.session.post(self.sSrvBaseURL+'/upgrade', data, stream=True)
            if r.status_code == 201:
                logging.info("no need to upgrade")
                return

            if r.status_code != 200:
                logging.info("error in upgrade")
                return

            logging.info("turning FS to RW")

            call(["mount", "-o", "remount,rw", "/"])

            with open("/home/pi/new.deb", 'wb') as fd:
                for chunk in r.iter_content(1024):
                    fd.write(chunk)

        except requests.ConnectionError:
            logging.error("reaching srv : connection refused")


        try:
            logging.info("check downloaded package")
            s = check_output(["/usr/bin/dpkg-deb", "-f", "/home/pi/new.deb"])
            if re.match("Package: netprobe", s) != None:
                # package is correct, install it
                logging.info("install new version")
                call(["dpkg", "-i", "/home/pi/new.deb"])
            else:
                logging.error("bad package deb")

        except CalledProcessError,e:
            logging.error("error in call for dpkg")
            print(e)
            exit()
            None

        os.unlink("/home/pi/new.deb")

        logging.info("turning FS back to RO")
        call(["sync"])

        logging.info("exiting")
        exit()
