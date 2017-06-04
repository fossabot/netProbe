# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-06-03 14:53:11 alex>
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
import logging

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

def clean():
    global iTurn2, iTurn1, arg, fLastFoo2, fLastFoo1
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

def foo4():
    print("**** job exec : just print")

def test_one_iteration():
    """ one iteration on one job """
    global fLastFoo1

    clean()

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

    clean()

    scheduler = sched.sched()
    scheduler.add("two_jobs 1",0.1, foo1)
    scheduler.add("two_jobs 2",0.25, foo2)

    fLastFoo1 = 0
    fLastFoo2 = 0

    for i in range(10):
        f = scheduler.step()
        time.sleep(f)

    # print "{} =? {}".format(iTurn1, iTurn2)

    if iTurn1 != 7 or iTurn2 != 3:
        assert False, "loop issue"

def test_deviation():
    """ 25 iteration and check deviation """
    global r
    clean()

    delay = 0.05
    iter = 25

    scheduler = sched.sched()
    scheduler.add("deviation", delay, foo1)

    time.time()

    sum = 0

    for i in range(1,iter):
        f = scheduler.step()
        sum += r
        # print "{} {} {}".format(i, r, sum/i)
        time.sleep(f)

    if abs(sum/iter - delay) > delay/10:
        assert False, "deviation compare {:.5f} to {:.5f}".format(abs(sum/iter - delay), delay/10)

def test_clean():
    """ suppress jobs """
    clean()

    scheduler = sched.sched()
    scheduler.add("clean", 1.01, foo1)

    f = scheduler.step()
    # print f

    if f < 1:
        assert False, "clean add job {}<1".format(f)

    scheduler.clean()

    time.sleep(f)

    f = scheduler.step()
    # print f

    if f != 30:
        assert False, "sched not clean"

def test_arg():
    """ job called with argument """
    global arg
    clean()

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
    clean()
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
    clean()
    scheduler = sched.sched()
    waitTime = 5
    scheduler.add("next1", waitTime, foo1, None, 1)

    b = time.time()
    scheduler.step()
    n = time.time()-b

    if n-1 > 0.01:
        assert False, "bad start time, should be less than 0.01, is {:.4f}".format(n-1)

def test_next2():
    """job will start in rand sec

    """
    clean()
    scheduler = sched.sched()
    scheduler.add("next2", 30, foo1, None, 2)

    t = scheduler.step()

    if t == 5 or t == 30:
        assert False, "bat start time, should be random {:.4f}".format(t)

def test_at0():
    """start time prior to now

    """
    clean()
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
    clean()

    scheduler = sched.sched()
    scheduler.addAt("at1", 30, foo1, None, time.time()+10)

def test_at2():
    """start time in exactly 600

    """
    clean()

    scheduler = sched.sched()
    scheduler.addAt("at2", 30, foo1, None, time.time()+600)

    t = scheduler.step()

    if t - 600 > 0.01:
        assert False, "bat start time, should be 600 {:.4f}".format(t-600)

def test_str2at_1():
    """ str2atTime HH:MM in +2 minute"""
    clean()

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour, tm_min+2, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(120)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_2():
    """ str2atTime HH:MM tomorow -1 minute"""
    clean()

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour, tm_min-1, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(24*3600-60)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_3():
    """ str2atTime HH:MM tomorow -1 hour"""
    clean()

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(23*3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_4():
    """ str2atTime HH:MM in +1 hour"""
    clean()

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_str2at_5():
    """ str2atTime HH:MM in +13 hour"""
    clean()

    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    s = time.strftime("%H:%M", time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+13, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    scheduler = sched.sched()
    t = scheduler.str2atTime(s)

    e = abs(t-(13*3600)-time.time()) 
    if e > 1:
        assert False, "error, should be < 1 and is {}".format(e)

def test_ext_between():
    """ check execution in a defined range """
    clean()

    scheduler = sched.sched()

    # what time is it
    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    # enable just before
    sEnable = time.strftime("%H:%M:%S", 
                            time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    sDisable = time.strftime("%H:%M:%S", 
                             time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    data = [
             {
                 "type" : "inside",
                 "enable": sEnable,
                 "disable": sDisable
             }
    ]

    scheduler.addExtended("ext between in", 60, data, foo4, None, 3)

    t = scheduler.step()
    if not (t > 2.8 and t < 3.1):
        assert False, "first step should be around 3"

    print("sleep for {}".format(t))
    time.sleep(t)

    t = scheduler.step()
    if t != 0:
        assert False, "second step should be 0"

    t = scheduler.step()
    if not (t > 59.8 and t < 60.1):
        assert False, "third step should be around 60"


# --------------------------------------------------------
def test_ext_between_andnext():
    """ check execution in a defined range and next execution to tomorrow """
    clean()

    scheduler = sched.sched()

    # what time is it
    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    # enable just before
    sEnable = time.strftime("%H:%M:%S", 
                            time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    sDisable = time.strftime("%H:%M:%S", 
                             time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour+1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    data = [
             {
                 "type" : "inside",
                 "enable": sEnable,
                 "disable": sDisable
             }
    ]

    scheduler.addExtended("ext between in", 86000, data, foo4, None, 3)

    t = scheduler.step()
    if not (t > 2.8 and t < 3.1):
        assert False, "first step should be around 3"

    print("sleep for {}".format(t))
    time.sleep(t)

    t = scheduler.step()
    if t != 0:
        assert False, "second step should be 0"

    t = scheduler.step()
    if not (t > 85998 and t < 86002):
        assert False, "third step should be around 86000 and is {:.2f}".format(t)

# --------------------------------------------------------
def test_ext_not_between():
    """ check no execution if not in a defined range """
    clean()

    scheduler = sched.sched()

    # what time is it
    (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

    # enable just before
    sEnable = time.strftime("%H:%M:%S", 
                            time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-2, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    sDisable = time.strftime("%H:%M:%S", 
                             time.localtime(time.mktime((tm_year, tm_mon, tm_day, tm_hour-1, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))))

    data = [
             {
                 "type" : "inside",
                 "enable": sEnable,
                 "disable": sDisable
             }
    ]

    scheduler.addExtended("ext not between in", 60, data, foo4, None, 1)

    t = scheduler.step()
    if t != 0:
        assert False, "first step should be 0"
    
    t = scheduler.step()
    if not (t > 79100 and t < 79260):
        assert False, "third step should be around 79200 and is {}".format(t)

# ---------------------------------------------
def foo_lock_incr(p):
    global fLastFoo1

    logging.info("foo_lock_incr")

    if not p.db.isProbeRunning():
        assert False, "no probe should be running"

    fLastFoo1 = 0

# ---------------------------------------------
def test_lock_counter():
    """ a job increment lock counter """
    global fLastFoo1

    from probelib.probemain import probemain

    p = probemain("test")

    clean()
    p.db.cleanLock()

    scheduler = sched.sched()
    scheduler.clean()

    if p.db.isProbeRunning():
        assert False, "no probe should be running"

    scheduler.add("test_lock_incr", 1, foo_lock_incr, args=p, startIn=1)

    fLastFoo1 = 1

    while fLastFoo1 == 1:
        t = scheduler.step(p)
        time.sleep(t)

    if p.db.isProbeRunning():
        assert False, "no probe should be running"

# ---------------------------------------------
def test_lock():
    """ exclusive job should set local lock """
    global fLastFoo1

    from probelib.probemain import probemain

    p = probemain("test")

    clean()
    p.db.cleanLock()

    scheduler = sched.sched()
    scheduler.clean()

    if p.db.isProbeRunning():
        assert False, "a probe should be running"

    scheduler.addExtended("test_lock", 1, None, foo_lock_incr, args=p, startIn=1, sLock="local")

    fLastFoo1 = 1

    while fLastFoo1 == 1:
        t = scheduler.step(p)
        time.sleep(t)

    if p.db.isProbeRunning():
        assert False, "no probe should be running"

# ---------------------------------------------
def test_locked():
    """ if job is locked, wait"""
    global fLastFoo1

    from probelib.probemain import probemain

    p = probemain("test")

    clean()
    p.db.cleanLock()

    scheduler = sched.sched()
    scheduler.clean()

    if p.db.isProbeRunning():
        assert False, "a probe should be running"

    p2 = probemain("test_locker")
    logging.info("acquire lock on p2 {}".format(str(p2.acquireLocalLock())))

    if p.acquireLocalLock():
        assert False, "a lock should be present"

    logging.info("release lock on p2 {}".format(str(p2.releaseLocalLock())))

    scheduler.addExtended("test_lock", 1, None, foo_lock_incr, args=p, startIn=1, sLock="local")

    logging.info("acquire lock on p2 #2 {}".format(str(p2.acquireLocalLock())))
    fLastFoo1 = 1

    t = scheduler.step(p)
    if fLastFoo1 != 1:
        assert False, "function should not have been called"
    time.sleep(t)

    t = scheduler.step(p)
    if fLastFoo1 != 1:
        assert False, "function should not have been called"
    time.sleep(t)

    logging.info("release lock on p2 #2 {}".format(str(p2.releaseLocalLock())))
    t = scheduler.step(p)
    if fLastFoo1 != 0:
        assert False, "function should have been called"

    if p.db.isProbeRunning():
        assert False, "no probe should be running"

# ---------------------------------------------
def all_sched(b=True):
    if b:
        test_create()
        test_deviation()    
        test_one_iteration()
        test_two_jobs()
        test_clean()
        test_arg()
        test_next0()
        test_next1()
        test_next2()
        test_at0()
        test_at1()
        test_at2()
        test_str2at_1()
        test_str2at_2()
        test_str2at_3()
        test_str2at_4()
        test_str2at_5()
        test_ext_between()
        test_ext_not_between()
        test_ext_between_andnext()
        test_lock_counter()
        test_lock()
    test_locked()

if __name__ == '__main__':
    _logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    logging.basicConfig(format=_logFormat,
                        level=logging.DEBUG)

    all_sched(False)
