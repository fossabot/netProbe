#
# Time-stamp: <2016-11-05 16:31:43 alex>
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

deb: clean
	@echo make deb package for PI
	@mkdir -p deb/home/pi/py-net-probe
	@cp -r *py netProbe probelib sched database hostId deb/home/pi/py-net-probe
	@rm -f netprobe_`cat ../VERSION`_all.deb
	fpm -s dir -t deb -n "netProbe" -a noarch --description "netProbe Pi client" -v `cat ../VERSION` --before-install deb/pre.sh --after-install deb/post.sh -C deb home

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc probelib/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ probelib/*~
	@rm -rf deb/home

test: clean
	@nosetests tests

