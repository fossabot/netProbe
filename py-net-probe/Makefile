#
# Time-stamp: <2016-05-01 12:51:20 alex>
#

all:
	@echo make lint
	@echo make clean
	@echo make test

lint: clean
	@pyflakes *py */*py
	@pylint --rcfile=~/.pylint main.py probe*.py netProbe sched hostId database

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ 

test: clean
	@nosetests tests

