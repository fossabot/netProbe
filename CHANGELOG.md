Changelog
=========

1.3 - 20/11/2016
----------------
* upgrade the software to the probe
* docker test probe

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

1.1.1 (fix)
-----------
* check on regular basis the job processes for zombies and restart...
* detect if main.py has crashed in each probe
