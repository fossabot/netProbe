# Docker file for testing the server
# from the git master version
# 
# Time-stamp: <2017-01-29 14:03:54 alex>
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

FROM centos:7

MAINTAINER Alex

RUN yum -y update
RUN yum -y install epel-release
RUN yum -y update

RUN yum -y install python-pip
RUN pip install --upgrade pip

RUN pip install Flask
RUN pip install Flask-APScheduler
RUN pip install elasticsearch

RUN yum -y install iperf3

RUN yum -y install git

WORKDIR /opt
RUN git clone https://github.com/achauvinhameau/netProbe


# main communication port from probes
EXPOSE 5000
# communication port for the iperf3 udp
EXPOSE 5201/udp
