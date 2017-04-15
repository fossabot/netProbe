Test probes
===========

set the log level for the probe to upper level, INO or DEBUG
```
PI_LOG_LEVEL=INFO
```

set the next iteration for testing to 1s
```
PI_SCHED_NOW=1
```

bypass the redis key/value for configuration to be extracted from stdin
```
PI_DB_TEST=1
```

launch the probe in the py-net-probe directory :
```
cat tests/icmp-test.json | sudo PI_LOG_LEVEL=INFO PI_DB_TEST=1 PI_SCHED_NOW=1 python probe-icmp.py
```
