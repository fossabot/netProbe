#!/bin/bash


echo "raspberry
raspberry" | passwd pi

set -e

/set_root_pw.sh
exec /usr/sbin/sshd -D
