from module import Registry
from flask import Blueprint, request
import time
import re

web_indexer_router = Blueprint("web-indexer-router", __name__)

@web_indexer_router.get("/search/manual")
def search():
    start = time.time()
    response_object = {"status": "success"}
    args = request.args.to_dict(flat=False)
    query = args["query"][0]

    score = Registry().web_indexer.bm25.transform(query)
    document = Registry().web_indexer.documents
    document["score"] = score
    document = document.sort_values(["score"], ascending=False)
    document = document[document["score"] != 0]
    results = list(document.T.to_dict().values()) 

    for result in results:
        text = result['text']
        sentences = re.split(r'(?<=[.!?])\s+', text)
        highlighted_sentences = []
        for sentence in sentences:
            if query in sentence:
                highlighted_sentence = sentence.replace(query, f'<b>{query}</b>')
                highlighted_sentences.append(highlighted_sentence)
        if highlighted_sentences:
            result['text'] = ' '.join(highlighted_sentences[:3])
    
    response_object["total_hit"] = len(results)
    response_object["results"] = results
    response_object["elapse"] = time.time() - start
    return response_object

@web_indexer_router.get("/search/manual/page-rank")
def search_with_pagerank():
    start = time.time()
    response_object = {"status": "success"}
    args = request.args.to_dict(flat=False)
    query = args["query"][0]

    score = Registry().web_indexer.bm25.transform(query)
    document = Registry().web_indexer.documents
    document["score"] = score

    pagerank_result = Registry().pagerank.pr_result
    pagerank_score = {}
    for url, score in pagerank_result.T.items():
        pagerank_score[url] = score["score"]/pagerank_result["score"].max()
    
    combined_scores = {}
    for url, score in pagerank_result.T.items():
        if pagerank_score[url]:
            score = score.iloc[0]
            combined_scores[url] = 0.9 * score + 0.1 * pagerank_score.get(url)

    document["combined_scores"] = document["url"].map(combined_scores)
    document = document.sort_values(["combined_scores"], ascending=False)
    document = document[document["combined_scores"] != 0]
    results = list(document.T.to_dict().values())
    for result in results:
        text = result['text']
        sentences = re.split(r'(?<=[.!?])\s+', text)
        highlighted_sentences = []
        for sentence in sentences:
            if query in sentence:
                highlighted_sentence = sentence.replace(query, f'<b>{query}</b>')
                highlighted_sentences.append(highlighted_sentence)
        if highlighted_sentences:
            result['text'] = ' '.join(highlighted_sentences[:3])

    response_object["total_hit"] = len(results)
    response_object["results"] = results
    response_object["elapse"] = time.time() - start
    return response_object