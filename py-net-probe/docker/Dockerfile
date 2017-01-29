# Docker file for testing the probe
#
# Time-stamp: <2017-01-29 13:59:01 alex>
#
# docker build -t netprobe .
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

FROM debian:jessie

MAINTAINER Alex

RUN apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install apt-transport-https

RUN apt-get -y install gcc
RUN apt-get -y install vim
RUN apt-get -y install python-pip
RUN apt-get -y install python-dev

RUN apt-get -y install git
RUN pip install --upgrade pip

# RUN pip install requests
RUN pip install netifaces
RUN pip install redis
RUN pip install psutil

RUN apt-get -y install iperf3

RUN git clone https://github.com/CoreSecurity/impacket

COPY netprobe.deb /
RUN dpkg -i /netprobe.deb

COPY start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]