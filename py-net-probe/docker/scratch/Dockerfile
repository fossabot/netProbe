# Docker file for testing the probe
#
# Time-stamp: <2017-01-29 13:59:30 alex>
#
# docker build -t np-test .
# docker run -d -p 2022:22 -e SSH_KEY="$(cat ~/.ssh/id_rsa.pub)" np-test
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

MAINTAINER Alex <ach@meta-x.org>

RUN apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install apt-utils
RUN apt-get -y install apt-transport-https 

RUN apt-get -y install openssh-server
RUN apt-get -y install sudo

ADD set_root_pw.sh /set_root_pw.sh
ADD run.sh /run.sh
RUN chmod +x /*.sh

RUN mkdir -p /var/run/sshd && sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config \
  && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
  && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config \
  && echo 'UseDNS no' >> /etc/ssh/sshd_config \
  && sed -i 's/#UsePAM yes/UsePAM no/' /etc/ssh/sshd_config \
  && true

RUN useradd pi \
    	&& passwd -d pi \
        && mkdir /home/pi \
        && chown pi /home/pi \
        && addgroup pi staff \
        && addgroup pi sudo \
        && true

RUN apt-get -y install dhcpd

EXPOSE 22

CMD ["/run.sh"]
