#
# Time-stamp: <2016-04-30 18:42:39 alex>
#

lint: clean
	pylint --rcfile=~/.pylint main.py probe.py netProbe sched hostId

clean:
	rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc
	rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ 

test:
	nosetests tests
