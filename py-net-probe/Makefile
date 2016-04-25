#
# Time-stamp: <2016-04-24 22:31:04 alex>
#

lint: clean
	pylint --rcfile=~/.pylint main.py probe.py netProbe sched hostId

clean:
	rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc
	rm -f *~ netProbe/*~ sched/*~ hostId/*~ 
