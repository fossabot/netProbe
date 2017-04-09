CONFIGURATION
=============

probe iperf
-----------

* server : target as a name or an ip address
* duration : seconds for the test in both direction
* way : input, output or both
* port : 5201 by default
* tos

used to set the TOS on each of the iperf frames. DSCP is using the
first 6 bits, ECN the last 2. Options for DSCP are listed below with
CS for class selector stated in RFC2474, AFxy for assured forwarding
(x=class, y=drop) as in RFC2597:
```
AF11	40
AF12	48
AF13	56
AF21	72
AF22	80
AF23	88
AF31	104
AF32	112
AF33	120
AF41	136
AF42	144
AF43	152
CS0	0
CS1	32
CS2	64
CS3	96
CS4	128
CS5	160
CS6	192
CS7	224
EF	184
```

configuration template example:
```
{ 
    "name": "T_IPERF",
    "jobs" : [
      { "job" : "iperf",
        "freq" : 600,
	"version" : 1,
	"data" : {
	   "server" : "iperf.server",
	   "duration" : 5,
	   "way" : "both",
	   "port" : 5201,
	   "tos" : 96
	}
      }
    ]
}
```

probe ntp
---------

check the ntp local PI client to gather statistics and clock stability of the main peer.

configuration template example:
```
{ 
    "name": "T_NTP",
    "jobs" : [
	{ 
          "active": "True",
          "job" : "ntp",
          "freq" : 600,
	  "version" : 1,
	  "data" : {}
	}
    ]
}
```

