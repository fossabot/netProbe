server
======
* templates for probe config (can include multiple at probe level)
* push regular stats to back office on probe connected or discovered, last hello...
* schedule on job definition
* configuration with fields by probe, not only globals
* upgrade the software to the probe
* clean the probe DB after inactivity

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

1.3
-----


1.2
-----
* FIX : configuration reload not working
* set the configuration file name on command line for the server part
* set last seen on ping
* force reload the configuration on sighup
* add an "active" flag on a job in the server configuration
* exit the probe from the server action
* restart job from the server action
* add an exit command for the main process to restart everything
* don't run a job with active flag set to false
* add job process statistics in the stat message
* add cpu temp in health
