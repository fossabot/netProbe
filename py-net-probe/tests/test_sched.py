# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:02:33 alex>
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
# import nose
import time

sys.path.insert(0, os.getcwd())
import sched

def test_create():
    """ create a scheduler """
    scheduler = sched.sched()

fLastFoo1 = time.time()
fLastFoo2 = time.time()
iTurn1 = 0
iTurn2 = 0
arg = 0

def foo1():
    global r
    global fLastFoo1
    global iTurn1
    r = round(time.time()-fLastFoo1,3)
    iTurn1 += 1
    fLastFoo1 = time.time()

def foo2():
    global r2
    global fLastFoo2
    global iTurn2
    r2 = round(time.time()-fLastFoo1,3)
    iTurn2 += 1
    fLastFoo2 = time.time()

def foo3(config):
    global arg
    arg = config['test']

def test_one_iteration():
    """ one iteration on one job """
    global fLastFoo1

    scheduler = sched.sched()
    scheduler.add("test_one_iteration", 0.1, foo1)

    fLastFoo1 = 0

    scheduler.step()
        
    if fLastFoo1 == 0:
        assert False, "not any loop"

def test_two_jobs():
    """ 2 jobs """
    global fLastFoo1
    global fLastFoo2
    global r, r2
    global iTurn1, iTurn2

    scheduler = sched.sched()
    scheduler.add("two_jobs 1",0.1, foo1)
    scheduler.add("two_jobs 2",0.25, foo2)

    fLastFoo1 = 0
    fLastFoo2 = 0

    for i in range(10):
        f = scheduler.step()
        time.sleep(f)

    print "{} =? {}".format(iTurn1, iTurn2)

    if iTurn1 != 8 or iTurn2 != 3:
        assert False, "loop issue"

def test_deviation():
    """ 25 iteration and check deviation """
    global r

    delay = 0.05
    iter = 25

    scheduler = sched.sched()
    scheduler.add("deviation", delay, foo1)

    time.time()

    sum = 0

    for i in range(1,iter):
        f = scheduler.step()
        sum += r
        print "{} {} {}".format(i, r, sum/i)
        time.sleep(f)

    print "compare {:.5f} to {:.5f}".format(abs(sum/iter - delay), delay/10)
    if abs(sum/iter - delay) > delay/10:
        assert False, "deviation"

def test_clean():
    """ suppress jobs """

    scheduler = sched.sched()
    scheduler.add("clean", 1.01, foo1)

    f = scheduler.step()
    print f

    if f < 1:
        assert False, "clean add job"

    scheduler.clean()

    time.sleep(f)

    f = scheduler.step()
    print f

    if f != 30:
        assert False, "sched not clean"

def test_arg():
    """ job called with argument """
    global arg

    arg = 1

    scheduler = sched.sched()
    config = { "test" : 10 }
    scheduler.add("arg", 0.1, foo3, config)
    scheduler.step()
        
    if arg != 10:
        assert False, "argument issue"

def test_next0():
    """job will start in iFreq

    """

    scheduler = sched.sched()
    waitTime = 0.5
    scheduler.add("next0", waitTime, foo1, None, 0)

    b = time.time()
    scheduler.step()
    n = time.time()-b

    if n-waitTime > 0.01:
        assert False, "bat start time, should be less than 0.005, is {:.4f}".format(n-waitTime)

def test_next1():
    """job will start in 1 sec

    """

    scheduler = sched.sched()
    waitTime = 5
    scheduler.add("next1", waitTime, foo1, None, 1)

    b = time.time()
    scheduler.step()
    n = time.time()-b

    if n-1 > 0.01:
        assert False, "bat start time, should be less than 0.01, is {:.4f}".format(n-1)

def test_next2():
    """job will start in rand sec

    """

    scheduler = sched.sched()
    scheduler.add("next2", 30, foo1, None, 2)

    t = scheduler.step()

    if t == 5 or t == 30:
        assert False, "bat start time, should be random {:.4f}".format(t)

def test_at0():
    """start time prior to now

    """

    scheduler = sched.sched()

    ok = 0
    try:
        scheduler.addAt("at0", 30, foo1, None, time.time()-1)
        ok = 1
    except:
        ok = 2

    if ok == 1:
        assert False, "prior to now not trapped"

def test_at1():
    """start time after now

    """

    scheduler = sched.sched()
    scheduler.addAt("at1", 30, foo1, None, time.time()+10)

def test_at2():
    """start time in exactly 600

    """

    scheduler = sched.sched()
    scheduler.addAt("at2", 30, foo1, None, time.time()+600)

    t = scheduler.step()

    if t - 600 > 0.01:
        assert False, "bat start time, should be 600 {:.4f}".format(t-600)

def test_str2at_1():
    """ str2atTime HH:MM in +2 minute"""

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour, tm_min+2, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(120)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_2():
    """ str2atTime HH:MM tomorow -1 minute"""

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour, tm_min-1, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(24*3600-60)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_3():
    """ str2atTime HH:MM tomorow -1 hour"""

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(23*3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_4():
    """ str2atTime HH:MM in +1 hour"""

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_5():
    """ str2atTime HH:MM in +13 hour"""

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+13, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(13*3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

# test_create()
# test_deviation()    
# test_one_iteration()
# test_two_jobs()
# test_clean()
# test_arg()
# test_next0()
# test_next1()
# test_next2()
# test_at0()
# test_at1()
# test_at2()
# test_str2at_1()
# test_str2at_2()
# test_str2at_3()
# test_str2at_4()
# test_str2at_5()
