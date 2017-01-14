Installation
============

on the server
-------------
```
pip install Flask
pip install elasticsearch
pip install Flask-APScheduler
```

add iperf3

need fpm :
https://github.com/jordansissel/fpm
yum install ruby-devel gcc make rpm-build
gem install fpm

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


Install the probe with ansible
==============================

* install a raspbian lite image on the probe memory card
* on the flash disk at root add an empty 'ssh' file
* connect on network and boot (requires DHCP and internet access)
* need an ssh key from the ansible user installed in ~/.ssh/id_rsa.pub
* ssh to the pi with pi login in order to add its fingerprint in the known_hosts file
  (password should be raspberry)
* find the raspberry ip address and install it in the files/hosts piprobes group, 
  in the new section
* exec the init playbook, this will install ssh key for future use and upgrade the pi
  version if required


All in one
----------
in the ansible directory
```
ansible-playbook --ask-pass -i files/hosts playbooks/pi-all.yml
```
option: --limit %ip of the pi%

duration around : 16 minutes

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
