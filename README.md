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
docker build .
docker image to get the latest id
docker run -it %id bash

