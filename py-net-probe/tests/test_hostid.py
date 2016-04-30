# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-30 19:52:50 alex>
#

import sys
import os
import nose
import time

sys.path.append(os.getcwd())

import hostId

@nose.tools.timed(0.1)
def test_1():
    """ check hostid """
    hid1 = hostId.hostId("test")
    h1 = hid1.get()
    print h1

    time.sleep(0.01)

    hid2 = hostId.hostId("test")
    h2 = hid2.get()
    print h2

    if h1 != h2:
        assert False,"2 calls not returning same id"

    time.sleep(0.01)
    hid3 = hostId.hostId("test2")
    h3 = hid3.get()
    print h3

    if h1 == h3:
        assert False,"2 different calls should return different id"

