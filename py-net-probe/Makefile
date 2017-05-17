#
# Time-stamp: <2017-05-14 17:36:36 alex>
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

dirs = netProbe sched hostId database probelib config
PYTHON = python

all: clean
	@echo make cc
	@echo make flakes
	@echo make lint
	@echo make clean
	@echo make test
	@echo make deb
	@echo make coverage-all
	@echo make  coverage-probes
	@echo make  coverage
	@echo make all-probes
	@echo make  probe-ntp
	@echo make  probe-smb
	@echo make  probe-icmp
	@echo make  probe-traceroute
	@echo make  probe-http
	@echo make  probe-https
	@echo make  probe-dns

lint: clean
	@pylint --rcfile=~/.pylint main.py probe*.py $(dirs:%=%/*.py)

flakes: clean
	@pyflakes *.py $(dirs:%=%/*.py)

cc: clean
	@echo complexity
	@radon cc $(dirs) *py -a -nc
	@echo maintenability
	@radon mi $(dirs) *py -nb

deb: clean version
	@echo make deb package for PI
	@mkdir -p deb/home/pi/py-net-probe
	@cp -r init.cfg start.sh *py netProbe probelib sched database hostId config deb/home/pi/py-net-probe
	@rm -f netprobe_`cat ../VERSION`_all.deb
	fpm -s dir -t deb -n "netprobe" -a noarch --description "netProbe Pi client" -v `cat ../VERSION` --before-install deb/pre.sh --after-install deb/post.sh -C deb --deb-no-default-config-files --license GPL-3.0 --maintainer "ach@meta-x.org" --url "https://github.com/achauvinhameau/netProbe" --vendor none home

clean:
	@rm -f $(dirs:%=%/*pyc)
	@rm -f $(dirs:%=%/*~)
	@rm -f tests/*pyc tests/*~
	@rm -f docker/scratch/*~
	@rm -f docker/*~
	@rm -rf deb/home

test: clean
	@nosetests tests

coverage-all: coverage-probes coverage
	@coverage combine .coverage-main .coverage-probes
	@coverage report -m

coverage: clean
	@PI_TEST_NO_OUTPUT=1 coverage run ./tests/test_all.py
	@cp .coverage .coverage-main
	@coverage report -m

coverage-probes: PYTHON=PI_TEST_NO_OUTPUT=1 coverage run
coverage-probes: all-probes
	@sudo chown $(shell whoami) .coverage-*
	@coverage combine .coverage-*
	@cp .coverage .coverage-probes
	coverage report -m

all-probes: probe-ntp probe-smb probe-icmp probe-traceroute probe-http probe-https

probe-ntp: clean
	@echo "**** NTP"
	@cat tests/ntp-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-ntp.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-http: clean
	@echo "**** HTTP"
	@cat tests/http-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-http.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-https: clean
	@echo "**** HTTPS"
	@cat tests/https-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-http.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-dns: clean
	@echo "**** DNS"
	@cat tests/dns-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-dns.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi
	@cat tests/dnsMX-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-dns.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi
	@cat tests/dns-er1-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-dns.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi
	@cat tests/dns-er2-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-dns.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-smb: clean
	@echo "**** SMB"
	@cat tests/smb-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-smb.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-icmp: clean
	@echo "**** ICMP"
	@cat tests/icmp-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-icmp.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

probe-traceroute: clean
	@echo "**** TRACEROUTE"
	@cat tests/traceroute-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 PI_RUN_ONCE=1 $(PYTHON) probe-traceroute.py
	@if [ -f .coverage ];then mv .coverage .coverage-`date +%s`;fi

version:
	@awk '/^__version/ { $$0="__version__ = \"'`cat ../VERSION`'\"" }; /^__date__/ { $$0="__date__ = \"'`date +%0d/%0m/%y-%H:%M:%S`'\"" } ; { print }' < main.py > /tmp/main.py
	@cp /tmp/main.py main.py
	@rm -f /tmp/main.py

