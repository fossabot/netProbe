#
# Time-stamp: <2016-04-30 20:08:51 alex>
#

lint: clean
	pylint --rcfile=~/.pylint main.py probe.py netProbe sched hostId

clean:
	rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc
	rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ 

test: clean
	nosetests tests
