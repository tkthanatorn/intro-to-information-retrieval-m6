from threading import Lock, Thread
from elasticsearch import Elasticsearch
from .web_indexer import WebIndexer
from .pagerank_indexer import PageRank

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class Registry(metaclass=SingletonMeta):
    elastic: Elasticsearch
    web_indexer: WebIndexer
    pagerank: PageRank

    def __init__(self,elastic: Elasticsearch,  web_indexer: WebIndexer, pagerank: PageRank):
        self.elastic = elastic
        self.web_indexer = web_indexer
        self.pagerank = pagerank
        print("registry created...")