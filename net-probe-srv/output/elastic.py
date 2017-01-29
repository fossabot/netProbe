# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2017-01-29 14:05:22 alex>
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
 elasticseatch output module
"""

from .output import output

from elasticsearch import Elasticsearch
import logging

class elastic(output):
    """ class to handle elastic output """
    
    # ----------------------------------------------------------
    def __init__(self, conf):
        """constructor"""

        output.__init__(self)

        if not conf.__contains__('server'):
            assert False, "elastic configuration missing server"

        if conf.__contains__('index'):
            sConfIndex = conf['index']
        else:
            sConfIndex = "pyprobe"

        if conf.__contains__('shard'):
            iConfShard = int(conf['shard'])
            if iConfShard < 1:
                iConfShard = 1
            if iConfShard > 12:
                iConfShard = 12
        else:
            iConfShard = 3

        if conf.__contains__('replica'):
            iConfReplica = int(conf['replica'])
            if iConfReplica < 0:
                iConfReplica = 0
            if iConfReplica > 3:
                iConfReplica = 3
        else:
            iConfReplica = 1

        self.es_server = conf['server']
        try:
            self.es = Elasticsearch(host=self.es_server)
        except:
            assert False, "cannot find elastic server, exiting"

        self.es.indices.create(index=sConfIndex,
                               body={
                                   'settings': {
                                       'number_of_shards': iConfShard,
                                       'number_of_replicas': iConfReplica
                                   }
                               },
                               ignore=400)

    # ----------------------------------------------------------
    def send(self, data):
        """send to elastic"""

        logging.info("send to elasticsearch")

        res = self.es.index(index="pyprobe", doc_type='result', body=data)

        if res['created'] != True:
            logging.error("error on insert in ES {}".format(res))
