# netProbe

Installation
============

on the server
-------------
```
pip install Flask
```

on the probe
------------
```
pip install requests
pip install netifaces
pip install redis
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
