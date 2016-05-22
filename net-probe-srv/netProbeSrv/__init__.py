# -*- Mode: Python; python-indent-offset: 4 -*-
#
# pylint --rcfile=~/.pylint main.py

"""
 server WS
"""

#import main
#import netProbeSrv.ping
#import netProbeSrv.version
#import netProbeSrv.discover

from flask import Flask

app = Flask(__name__)
es_server = "127.0.0.1"

from elasticsearch import Elasticsearch

es = Elasticsearch(host=es_server)

res = es.indices.create(index="pyprobe",
                        body={
                            'settings': {
                                'number_of_shards': 5,
                                'number_of_replicas': 0
                                }
                        },
                        ignore=400
                    )

# print res
