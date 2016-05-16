# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-05-16 14:51:55 alex>
#

"""
 probe for the health
"""

from probelib.health import probe_health

p = probe_health(True)

p.job_health({})

