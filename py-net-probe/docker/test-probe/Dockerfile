# Docker file for testing the probe
#
# Time-stamp: <2016-11-19 20:30:36 alex>
#

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