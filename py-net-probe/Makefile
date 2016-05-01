#
# Time-stamp: <2016-05-01 18:21:40 alex>
#

all:
	@echo make lint
	@echo make flakes
	@echo make clean
	@echo make test

lint: clean
	@pylint --rcfile=~/.pylint main.py probe*.py netProbe sched hostId database

flakes: clean
	@pyflakes *py */*py

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ 

test: clean
	@nosetests tests

