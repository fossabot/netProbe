#!/bin/sh
#
# Time-stamp: <2017-06-04 21:49:40 alex>
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

# ----------------------------
rm -rf /home/pi/py-net-probe/*

# v1.8.1
# install dnspython
pip install dnspython

# v1.9.1
# upgrade PI in post-boot
cat > /home/pi/py-net-probe/post-boot.sh <<EOF
#!/bin/sh

# wait for dhcp to get an address
sleep 60

killall dhcpcd
killall cron

sleep 15

mount -o rw,remount /
mount -o rw,remount /boot

pip install --upgrade pip
pip install --upgrade -r /home/pi/py-net-probe/pi-python-reqs.txt

apt-get -y update
apt-get -y upgrade
apt-get -y clean
apt-get -y autoclean
apt-get -y autoremove

apt-get -y install watchdog

mount -o ro,remount /boot

rm -f /home/pi/py-net-probe/post-boot.sh

reboot
EOF

