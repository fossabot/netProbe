# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-19 13:34:38 alex>
#

"""
 probe for the http protocol using urllib2
"""

import logging
import urllib2
import socket
import time
import re

from .probemain import probemain

class probe_http(probemain):
    """ http class for probe
    """

    # -----------------------------------------
    def __init__(self):
        """constructor

        """
        probemain.__init__(self, "HTTP")

        self.checkNet()
        self.getConfig("http", self.job_http)
        self.mainLoop()

    # -----------------------------------------
    def getConfig(self, name, f):
        """get the configuration from the database if f_testv4 passed

        """
        jobs = super(probe_http, self).getConfig(name, f, self.f_testOK)
        for j in jobs:
            logging.info("add job to scheduler for {} each {} sec".format(j['data']['url'], j['freq']))

    # -----------------------------------------
    def job_http(self, _config):
        """http job

        """
        sReContent = ""

        sURL = _config['url']
        if _config.__contains__('timeout'):
            fTimeout = float(_config['timeout'])
        else:
            iTimeout = 10

        if _config.__contains__('content'):
            sReContent = str(_config['content'])

        result = {
            "http-timeout" : fTimeout,
            "http-url" : sURL
        }

        sError = "ok"
        sReturnCode = "error"
        
        fNow = time.time()
        fTime = 0

        try:
            f = urllib2.urlopen(sURL, data=None, timeout=fTimeout)
            fTime = time.time() - fNow

            sReturnCode = str(f.getcode())
            
            # check content of the returned page
            if sReContent != "":
                content = f.read()
                #print content
                #print sReContent
                r = re.search(sReContent, content)

                if r != None:
                    result['contentMatch'] = "OK"
                else:
                    result['contentMatch'] = "KO"

            aInfo = f.info()
            s = aInfo.get('Content-Type')
            if s != None:
                result['http-contentType'] = s

            i = aInfo.get('Content-Length')
            if i != None:
                result['http-contentLen'] = i

            s = aInfo.get('Server')
            if s != None:
                result['http-server'] = s

        except urllib2.URLError, e:
            sError = str(e.reason)

        if fTime == 0:
            fTime = fTimeout

        result['http-code'] = sReturnCode
        result['http-error'] = sError
        result['http-time'] = fTime.__format__('0.4f')

        logging.info("http result : {}".format(result))
