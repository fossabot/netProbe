# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-06-05 17:35:04 alex>
#

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

        if conf.__contains__('server'):
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

        res = self.es.indices.create(index=sConfIndex,
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
