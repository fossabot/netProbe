#/bin/sh

cd `dirname $0`

while [ true ]
do
 echo "starting"
 python ./main.py
 sync
 mount -o remount,ro /
 if [ $? -ne 0 ]
 then
   reboot
 fi
 sleep 15
done
