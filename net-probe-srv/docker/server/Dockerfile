# Docker file for testing the server
# from the git master version
# 
# Time-stamp: <2017-01-08 13:39:46 alex>
#

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
