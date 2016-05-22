#
# Time-stamp: <2016-05-22 21:50:39 alex>
#

all:
	@echo make lint
	@echo make flakes
	@echo make clean
	@echo make test

lint: clean
	pylint --rcfile=~/.pylint srv.py netProbeSrv/*py config/*py

flakes: clean
	@pyflakes *py */*py

clean:
	rm -f *pyc */*pyc
	rm -f *~ */*~

test: clean
	@nosetests tests
