# netProbe

Installation
============

on the server
-------------
```
pip install Flask
pip install elasticsearch
```

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

Install with ansible
====================

* install a raspbian lite image on the probe memory card, connect on network and boot (requires DHCP and internet access)
* need an ssh key from the ansible user installed in id_rsa.pub
* find the raspberry ip address and install it in the files/hosts piprobes group
* exec the init playbook, this will install ssh key for future use and upgrade the pi version if required

```
ansible-playbook --ask-pass -i files/hosts playbooks/pi-init.yml --limit %ip of the pi%
```

* exec the installation playbook

```
ansible-playbook -i files/hosts playbooks/install-probe.yml --limit %ip of the pi%
```
