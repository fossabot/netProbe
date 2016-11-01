# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-11-01 21:21:21 alex>
#

"""
 probe for the health
"""

from probelib.health import probe_health

p = probe_health(False)

#p = probe_health(True)
#p.job_health({})
#exit()

