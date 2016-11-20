server
======
* templates for probe config (can include multiple at probe level)
* push regular stats to back office on probe connected or discovered, last hello...
* schedule on job definition
* configuration with fields by probe, not only globals
* clean the probe DB after inactivity
* pushAction for upgrading specific probe

probe
=====
* http probe can use a target IP address different than URL server name
* DNS job

raspberry
=========
* install watchdog
* add vcgencmd display_power 0 (?)

History
=======
move to changelog once released

1.4
-----
* fix : check probe connectivity with the server in the ping job
* add probe configuration for timers in init.cfg
* clean dead probes on the server
