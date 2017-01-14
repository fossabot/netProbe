Deployment
==========

Purpose:
-------

duplicate an image file of the raw filesystem contained on the flash
card to multiple new Pi probes

* install a freshly deployed Pi probe with ansible method
* copy the flash card on a raw file (ie using Win32 Disk Imager on Windows, or dd on Linux)
* use the reduce-slash.sh script to build a smaller version of the image
* copy the new image on the SD card for the new Pi Probe and boot the PI, the file system will be expanded during the first boot cycles, this will take more time than a normal boot sequence (expands the FS, reboot, expands the partition, reboot).

Stats:
------

* raw image size : 7.761.920 KB
* reduced image size : 1.490.048 KB