#
# Time-stamp: <2016-05-15 16:08:15 alex>
#

all:
	@echo make flakes
	@echo make lint
	@echo make clean
	@echo make test

lint: clean
	@pylint --rcfile=~/.pylint main.py probe*.py netProbe sched hostId database probelib

flakes: clean
	@pyflakes *py */*py

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc probelib/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ probelib/*~ 

test: clean
	@nosetests tests

