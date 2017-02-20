#
# Time-stamp: <2017-02-20 22:27:26 alex>
#
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


all:
	@echo make git-status
	@echo make clean
	@echo make test

clean:
	@cd net-probe-srv && make -s clean
	@cd py-net-probe && make -s clean
	@rm -f *~ \#*# .*~
	@rm -f ansible/files/*~ ansible/playbooks/*~ ansible/playbooks/*retry
	@rm -f docs/*~

test: clean
	@cd net-probe-srv && make -s test
	@cd py-net-probe && make -s test

git-status: clean
	git status

coverage: clean
	@cd net-probe-srv && make -s coverage
	@cd py-net-probe && make -s coverage
	@coverage combine py-net-probe/.coverage net-probe-srv/.coverage
	@coverage xml
	CODACY_PROJECT_TOKEN=1936f6ba7c3a41ee82aa5e1cbfc16ce6 python-codacy-coverage -r coverage.xml
