server
======
* push regular stats to back office on probe connected or discovered, last hello...
* schedule on job definition
* configuration with fields by probe, not only globals
* pushAction for upgrading specific probe
* hostname

probe
=====
* http probe can use a target IP address different than URL server name
* DNS probe
* CIFS probe
* stop probe when not anymore in configuration

raspberry
=========
* install watchdog

History
=======
move to changelog once released

1.4
-----
* fix : check probe connectivity with the server in the ping job
* add probe configuration for timers in init.cfg
* clean dead probes on the server
* clean the probe DB after inactivity
* templates for probe config (can include multiple at probe level)
* add vcgencmd display_power 0 to disable display
* disable audio on the PI
* rpi-update at install time
* adjust gpu memory on PI
* disable wifi
* suppress urllib3 logs
* add upgrade feature on probe
* dhcp specific client id
* docker configuration file for test
