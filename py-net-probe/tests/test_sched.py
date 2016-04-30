# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-30 19:58:29 alex>
#

import sys
import os
import nose
import time

sys.path.insert(0, os.getcwd())
import sched

def test_create():
    """ create a scheduler """
    scheduler = sched.sched()

fLastFoo1 = time.time()
iTurn1 = 0
iTurn2 = 0

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

def test_one_iteration():
    """ one iteration on one job """
    global fLastFoo1

    scheduler = sched.sched()
    scheduler.add(0.1, foo1)

    fLastFoo1 = 0

    f = scheduler.step()
        
    if fLastFoo1 == 0:
        assert False, "not any loop"

def test_two_jobs():
    """ 2 jobs """
    global fLastFoo1
    global fLastFoo2
    global r, r2
    global iTurn1, iTurn2

    scheduler = sched.sched()
    scheduler.add(0.1, foo1)
    scheduler.add(0.25, foo2)

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
    scheduler.add(delay, foo1)

    fLastFoo1 = time.time()

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
    scheduler.add(1.01, foo1)

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

# test_create()
# test_deviation()    
# test_one_iteration()
# test_two_jobs()
# test_clean()
