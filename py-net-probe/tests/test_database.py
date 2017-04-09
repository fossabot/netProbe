# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-04-09 14:07:14 alex>
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
import json

sys.path.append(os.getcwd())
import database

@nose.tools.timed(10)
def test_create_db():
    """ create database in redis """

    db = database.dbRedis.dbRedis()

    if db == None:
        assert False

def test_addjob():
    """ add job in the database """
    db = database.dbRedis.dbRedis()

    if db == None:
        assert False

    db.cleanJob("test")
    db.addJob("test", {'name' : 'test'})

    if db.dumpJob("test").next() != '{"name": "test"}':
        assert False

def test_clean():
    """ clean database """
    db = database.dbRedis.dbRedis()

    if db == None:
        assert False

    db.cleanJob("test")
    if sum(1 for x in db.dumpJob("test")) != 0:
        assert False

    db.addJob("test", {'name' : 'test'})

    if db.dumpJob("test").next() != '{"name": "test"}':
        assert False

    db.cleanJob("test")
    if sum(1 for x in db.dumpJob("test")) != 0:
        assert False

# test_clean()
# test_addjob()
