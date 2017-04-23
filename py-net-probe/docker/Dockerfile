# Docker file for testing the probe
#
# Time-stamp: <2017-04-18 21:47:36 alex>
#
# docker build -t netprobe .
# docker run -d netprobe
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
RUN apt-get -y install apt-utils dialog apt-transport-https

RUN apt-get -y install gcc vim python-pip python-dev

RUN apt-get -y install git
RUN pip install --upgrade pip

# RUN pip install requests
RUN pip install netifaces
RUN pip install redis
RUN pip install psutil
RUN pip install pycrypto

RUN apt-get -y install iperf3

RUN mkdir -p /home/pi/py-net-probe

COPY start.sh /
RUN chmod +x /start.sh

COPY netprobe.deb /
RUN dpkg -i /netprobe.deb

RUN git clone https://github.com/CoreSecurity/impacket
RUN mv /impacket/impacket /home/pi/py-net-probe

CMD ["/start.sh"]