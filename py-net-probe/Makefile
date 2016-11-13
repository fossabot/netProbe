#
# Time-stamp: <2016-11-13 18:22:07 alex>
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
	@awk '/^__version/ { $$0="__version__ = \"'`cat ../VERSION`'\"" }; /^__date__/ { $$0="__date__ = \"'`date +%0d/%0m/%y-%H:%M:%S`'\"" } ; { print }' < main.py > /tmp/main.py
	@cp /tmp/main.py main.py
	@mkdir -p deb/home/pi/py-net-probe
	@cp -r start.sh *py netProbe probelib sched database hostId deb/home/pi/py-net-probe
	@rm -f netprobe_`cat ../VERSION`_all.deb
	fpm -s dir -t deb -n "netprobe" -a noarch --description "netProbe Pi client" -v `cat ../VERSION` --before-install deb/pre.sh --after-install deb/post.sh -C deb --deb-no-default-config-files --license GPL-3.0 --maintainer "ach@meta-x.org" --url "https://github.com/achauvinhameau/netProbe" --vendor none home

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc probelib/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ probelib/*~
	@rm -rf deb/home

test: clean
	@nosetests tests

