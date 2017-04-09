server
======
* push regular stats to back office on probe connected or discovered, last hello...
* schedule on job definition
* configuration with fields by probe, not only globals
* avoid multiple conf read, add timer

probe
=====
* http probe can use a target IP address different than URL server name
* DNS probe
* CIFS probe
* NTP stats probe
* stop probe when not anymore in configuration
* disable the upgrade + config in the init.cfg
* send default router IP address to help locating new probes on internal network
* add IP address in stats frames
* add configuration change in updates of jobs
* add jobs restart in updates

raspberry
=========
* install watchdog

History
=======
move to changelog once released

1.7
-----
* upgrade path in configuration file
* correct upgrade on PI
* add hostname in conf and on PI
* fix: correct schedule handling on probes
* probe test mode without redis
