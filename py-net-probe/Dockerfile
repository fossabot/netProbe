# Docker file for testing the probe
#
# Time-stamp: <2016-05-05 15:50:08 alex>
#

FROM centos:7

MAINTAINER Alex

RUN yum -y update
RUN yum -y install epel-release gcc
RUN yum -y update
RUN yum -y install python-pip python-devel git

RUN pip install --upgrade pip

RUN pip install requests
RUN pip install netifaces
RUN pip install redis

RUN git clone https://github.com/CoreSecurity/impacket
RUN git clone -b icmp-v1 https://github.com/achauvinhameau/netProbe.git
RUN mv impacket/impacket netProbe/py-net-probe

RUN rm -rf /netProbe/net-probe-srv
