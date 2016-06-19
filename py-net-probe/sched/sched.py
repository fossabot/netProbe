# -*- Mode: Python; python-indent-offset: 4 -*-
#

"""
fLastFoo1 = 0
def foo1():
	global fLastFoo1
	print("foo1", round(time.time()-fLastFoo1,2))
	fLastFoo1 = time.time()

fLastFoo3 = 0
def foo3():
	global fLastFoo3
	print("foo3", round(time.time()-fLastFoo3,2))
	fLastFoo3 = time.time()

fLastFoo5 = 0
def foo5():
	global fLastFoo5
	print("foo5", round(time.time()-fLastFoo5,2))
	fLastFoo5 = time.time()

fLastFoo10 = 0
def foo10():
	global fLastFoo10
	print("foo10", round(time.time()-fLastFoo10,2))
	fLastFoo10 = time.time()

schedStep()

schedAdd(5, foo5)
schedAdd(1, foo1)
schedAdd(3, foo3)
schedAdd(10, foo10)

# pprint.pprint(aSchedJobs)

while (True):
	f = schedStep()
	# print(f)
	time.sleep(f)
"""

__version__ = "1.0"
__date__ = "08/04/2016"
__author__ = "Alex Chauvin"

import time
import random
import logging
import re

class sched(object):
    """
    scheduler class
    """
    
    # ------------------------------------
    def __init__(self):
        """
        constructor, calls once the step() method
        """
        self.aSchedJobs = []
        self.clean()

    # ------------------------------------
    def add(self, name, iFreq, func, args=None, startIn=0):
        """
        add a job to the schedule
        :param name: name of the job, for information
        :param iFreq: frequency in seconds
        :param func: function to call each iteration
        :param args: argument to pass to the job
        :param startIn: next execution of the job in 
           0: iFreq
           1: now+1
           2: random between 5s and iFreq
        """

        iNextExec = time.time()
        if startIn == 0:
            iNextExec += iFreq
        else:
            if startIn == 1:
                iNextExec += 1
            else:
                if startIn == 2:
                    if iFreq<5:
                        iNextExec += 5
                    else:
                        iNextExec += int(random.random() * (iFreq-5)) + 5
            
        logging.info("add job {} : freq = {}, next = {:0.2f}".format(name, iFreq, iNextExec-time.time()))

        self.aSchedJobs.append({'freq' : iFreq,
                                'func': func,
                                'args': args,
                                'nextExec' : iNextExec})

    # ------------------------------------
    def addAt(self, name, iFreq, func, args=None, atTime=0):
        """
        add a job to the schedule, will run once
        :param name: name of the job, for information
        :param iFreq: frequency in seconds
        :param func: function to call each iteration
        :param args: argument to pass to the job
        :param atTime: time for first iteration
        """

        now = time.time()

        if atTime < now:
            assert False, "at time prior to now"

        logging.info("add at job {} : freq = {}, next = {:0.3f}".format(name, iFreq, atTime-now))

        self.aSchedJobs.append({'freq' : iFreq,
                                'func': func,
                                'args': args,
                                'nextExec' : atTime})
        
    # ------------------------------------
    def str2atTime(self, s):
        """ convert a time string to a atTime usable in addAt()
        HH:MM in 24h00 format
        """

        # print s

        (tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst) = time.localtime()

        # print "before",(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)

        r = re.match("(\d\d):(\d\d)", s)
        if r != None:
            hour = int(r.group(1))
            minute = int(r.group(2))

            if hour < tm_hour:
                # tomorow ?
                tm_day += 1
                tm_hour = hour
                tm_min = minute
            else:
                if hour == tm_hour:
                    if minute < tm_min:
                        # tomorow
                        tm_day += 1
                        tm_hour = hour
                        tm_min = minute
                    else:
                        # today
                        tm_hour = hour
                        tm_min = minute
                else:
                    tm_hour = hour
                    tm_min = minute
                
        # print "after ",(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)

        return time.mktime((tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))

    # ------------------------------------
    def step(self):
        """
        run a step and return the delay till next step
        returns the wait time in seconds

        if no job is in the queue, returns 30
        if next job in more than a second, returns next sched delta time
        if next job is within the sec, wait for the delay and launch job, 
           then returns 0
        """
        if len(self.aSchedJobs) == 0:
            return 30

        self.aSchedJobs.sort(key=lambda item: item['nextExec'], reverse=True)
        # pprint.pprint(aSchedJobs)
        nextJob = self.aSchedJobs[-1:][0]
        fNextSched = nextJob['nextExec'] - time.time()
        if fNextSched > 1:
            return fNextSched
        else:
            if fNextSched > 0:
                time.sleep(fNextSched)
                        
            nextJob = self.aSchedJobs.pop()
            nextJob['nextExec'] += nextJob['freq']
            if nextJob['args'] == None:
                nextJob['func']()
            else:
                nextJob['func'](nextJob['args'])

            self.aSchedJobs.append(nextJob)
            return 0

    # ------------------------------------
    def clean(self):
        """
        suppress all jobs scheduled
        """
        self.aSchedJobs = []
        self.step()
