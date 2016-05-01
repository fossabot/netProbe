# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-01 18:16:49 alex>
#

import sys
import os
import nose
import json

sys.path.append(os.getcwd())
import database

@nose.tools.timed(10)
def test_create_db():
    """ create database in redis """

    db = database.database()

    if db == None:
        assert False

def test_addjob():
    """ add job in the database """
    db = database.database()

    if db == None:
        assert False

    db.cleanJob("test")
    db.addJob("test", {'name' : 'test'})

    if db.dumpJob("test").next() != '{"name": "test"}':
        assert False

def test_clean():
    """ clean database """
    db = database.database()

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
