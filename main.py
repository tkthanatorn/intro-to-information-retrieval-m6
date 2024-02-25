import os
import sys
project_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(project_path))

import nltk
nltk.download("stopwords")
nltk.download("punkt")

from flask import Flask
from elasticsearch import Elasticsearch
from module import WebIndexer, Registry, PageRank

app = Flask(__name__)
elastic = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "abcd1234"))
web_indexer = WebIndexer()
pagerank = PageRank(0.85)
Registry(elastic, web_indexer, pagerank)

from router.elastic import es_router
from router.web_indexer import web_indexer_router
app.register_blueprint(es_router)
app.register_blueprint(web_indexer_router)

if __name__ == "__main__":
    app.run(debug=True)