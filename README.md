[![Codacy Badge](https://api.codacy.com/project/badge/Grade/783f58bd103940a399331ca5711af28f)](https://www.codacy.com/app/achauvinhameau/netProbe?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=achauvinhameau/netProbe&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/783f58bd103940a399331ca5711af28f)](https://www.codacy.com/app/achauvinhameau/netProbe?utm_source=github.com&utm_medium=referral&utm_content=achauvinhameau/netProbe&utm_campaign=Badge_Coverage) [![Code Climate](https://codeclimate.com/github/achauvinhameau/netProbe/badges/gpa.svg)](https://codeclimate.com/github/achauvinhameau/netProbe)
Purpose
=======

netProbe is a small client/server tool to monitor the network
capabilities by using network client, probe some servers, collect
statistics and push these to a backend.

The small probes are totally controlled by a server and could run on a
small device like a raspberry pi (even 1B+). The main idea behind is
to be able to install probes at every location of your network with a
minimal cost and gather information "like users".

Architecture
============

The probe architecture uses individual probe services like ICMP or
HTTP that could be started on a regular basis.

Probe handles the communication to the central server and launches
processes dedicated to specific jobs. Between the probe and the job a
redis bus stores the configuration and the results in order to allow
asynchronous transactions.

The server part is only composed of web service engine running on
flask and provides simple features like registration of the probe, job
configuration, result gathering and push to a backend like
elasticsearch.

Current probes
==============
* health : gather the status of the Raspberry
* http : get URL content, page status, load delay, check content keyword
* icmp : send ping to target and report delay and loss
* iperf : check bandwidth
* ntp : report status of local ntp synch of the probe
* smb : some checks on CIFS server (mount, get file)
* temperature : gather raspberry processor temperature
* traceroute : report path to target and delay at each step
