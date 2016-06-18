#
# Time-stamp: <2016-06-05 17:32:34 alex>
#

all:
	@echo make lint
	@echo make flakes
	@echo make clean
	@echo make test

lint: clean
	pylint --rcfile=~/.pylint srv.py netProbeSrv/*py config/*py output/*py

flakes: clean
	@pyflakes *py */*py

clean:
	rm -f *pyc */*pyc
	rm -f *~ */*~

test: clean
	@nosetests tests
