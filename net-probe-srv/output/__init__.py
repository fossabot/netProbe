# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-12 21:46:29 alex>
#

"""
 output module
"""

from .output import output
from .debug import debug
from .elastic import elastic
from .logstash import logstash

# outputer = output.output()
outputer = [output()]
