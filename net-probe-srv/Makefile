#
# Time-stamp: <2017-02-20 22:27:31 alex>
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

coverage: clean
	PI_TEST_NO_OUTPUT=1 coverage run ./tests/test_all.py
	coverage report -m
