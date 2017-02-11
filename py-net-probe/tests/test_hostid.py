# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:02:30 alex>
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

import sys
import os
import nose
import time

sys.path.append(os.getcwd())

import hostId

@nose.tools.timed(0.2)
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

