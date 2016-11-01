Installation
============

on the server
-------------
```
pip install Flask
pip install elasticsearch
```

add iperf3

on the probe
------------
```
pip install requests
pip install netifaces
pip install redis
pip install psutil
```

requires impacket from :
* https://github.com/CoreSecurity/impacket
to be installed in one system directory (ie /usr/lib/python2.7/site-packages)

requires a redis started on the probe host

Docker test client
==================

manual
------

docker run -it centos:7 bash

yum -y install epel-release python-pip python-devel git 

add libraries (pip install + impacket)

image
-----
docker build -t netprobe .
docker run -it netprobe bash

the pakcage is in /netProbe/py-net-probe

specific changes :
* add net-probe-srv-prod in the /etc/hosts file pointing to the server
* add host="xxxxx" in the database/database.py file on the call to redis.Redis since the redis database is local to the probe host and not supposed to be elswhere

start the client with python main.py

Install the probe with ansible
==============================

* install a raspbian lite image on the probe memory card, connect on network and boot (requires DHCP and internet access)
* need an ssh key from the ansible user installed in ~/.ssh/id_rsa.pub
* ssh to the pi with pi login in order to add its fingerprint in the known_hosts file (password should be raspberry)
* find the raspberry ip address and install it in the files/hosts piprobes group, in the new section
* exec the init playbook, this will install ssh key for future use and upgrade the pi version if required


All in one
----------
```
ansible-playbook --ask-pass -i files/hosts playbooks/pi-all.yml
option: --limit %ip of the pi%
```

Step by Step
------------
```
ansible-playbook --ask-pass -i files/hosts playbooks/pi-init.yml --limit %ip of the pi%
```

* exec the installation playbook

```
ansible-playbook -i files/hosts playbooks/install-probe.yml --limit %ip of the pi%
```

* turn the pi in read-only mode to preserve SD and allow power stop
```
ansible-playbook -i files/hosts playbooks/pi-ro.yml --limit %ip of the pi%
```
