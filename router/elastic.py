from flask import Blueprint, request
from module import Registry
import pandas as pd
import time

es_router = Blueprint("elastic-router", __name__)

@es_router.get("/search/elastic")
def search():
    start = time.time()
    response_object = {"status": "success"}
    args = request.args.to_dict(flat=True)
    query_term = args["query"][0]

    results = Registry().elastic.search(
        index='simple',
        source_excludes=['url_lists'],
        size=100,
        query={"match": {"text": query_term}}
    )
    end = time.time()

    total_hit = results["hits"]["total"]["value"]
    results_df = pd.DataFrame([
        [hit["_source"]['title'], hit["_source"]['url'], hit["_source"]['text'][:100], hit["_score"]]
        for hit in results['hits']['hits']
    ], columns=['title', 'url', 'text', 'score'])

    response_object['total_hit'] = total_hit
    response_object['results'] = results_df.to_dict('records')
    response_object['elapse'] = end - start
    return response_object