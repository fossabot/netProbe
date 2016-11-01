#
# Time-stamp: <2016-07-24 21:52:01 alex>
#

all:
	@echo make lint
	@echo make flakes
	@echo make clean
	@echo make test

lint: clean
	pylint --rcfile=~/.pylint srv.py netProbeSrv/*py config/*py output/*py liveDB/*py

flakes: clean
	@pyflakes *py */*py

clean:
	rm -f *pyc */*pyc
	rm -f *~ */*~

test: clean
	@nosetests tests
