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

class sched(object):
    """
    scheduler class
    """

    def __init__(self):
        """
        constructor, calls once the step() method
        """
        self.aSchedJobs = []
        self.step()

    def add(self, iFreq, func):
        """
        add a job to the schedule
        :param iFreq: frequency in seconds
        :param func: function to call each iteration
        """
        self.aSchedJobs.append({'freq' : iFreq,
                                'func': func,
                                'nextExec' : time.time()+iFreq})


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
            nextJob['func']()
            self.aSchedJobs.append(nextJob)
            return 0

