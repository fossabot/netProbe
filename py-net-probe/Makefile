#
# Time-stamp: <2017-02-20 21:41:29 alex>
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

all:
	@echo make flakes
	@echo make lint
	@echo make clean
	@echo make test

lint: clean
	@pylint --rcfile=~/.pylint main.py probe*.py netProbe sched hostId database probelib config

flakes: clean
	@pyflakes *py */*py

deb: clean
	@echo make deb package for PI
	@awk '/^__version/ { $$0="__version__ = \"'`cat ../VERSION`'\"" }; /^__date__/ { $$0="__date__ = \"'`date +%0d/%0m/%y-%H:%M:%S`'\"" } ; { print }' < main.py > /tmp/main.py
	@cp /tmp/main.py main.py
	@mkdir -p deb/home/pi/py-net-probe
	@cp -r init.cfg start.sh *py netProbe probelib sched database hostId config deb/home/pi/py-net-probe
	@rm -f netprobe_`cat ../VERSION`_all.deb
	fpm -s dir -t deb -n "netprobe" -a noarch --description "netProbe Pi client" -v `cat ../VERSION` --before-install deb/pre.sh --after-install deb/post.sh -C deb --deb-no-default-config-files --license GPL-3.0 --maintainer "ach@meta-x.org" --url "https://github.com/achauvinhameau/netProbe" --vendor none home

clean:
	@rm -f *pyc netProbe/*pyc sched/*pyc hostId/*pyc database/*pyc tests/*pyc
	@rm -f probelib/*pyc config/*pyc
	@rm -f *~ netProbe/*~ sched/*~ hostId/*~ database/*~ tests/*~ probelib/*~ config/*~ deb/*~
	@rm -f docker/scratch/*~
	@rm -f docker/*~
	@rm -rf deb/home

test: clean
	@nosetests tests

coverage: clean
	PI_TEST_NO_OUTPUT=1 coverage run ./tests/test_all.py
	coverage report -m
	coverage xml
	CODACY_PROJECT_TOKEN=1936f6ba7c3a41ee82aa5e1cbfc16ce6 python-codacy-coverage -r coverage.xml
