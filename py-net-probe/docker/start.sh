#! /bin/bash

# add host in the /etc/hosts file

host=`ip route | awk '/default/ { print $3; }'`

egrep -v '^\s*#' /etc/hosts | fgrep probe-srv > /dev/null
if [ $? -eq 1 ]
then
  echo $host probe-srv >> /etc/hosts
fi

cd /home/pi/py-net-probe

python ./main.py -r $host
