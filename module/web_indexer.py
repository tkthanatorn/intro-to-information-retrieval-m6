from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle
import json
import pandas as pd
from .bm25 import BM25


from nltk.corpus import stopwords

class WebIndexer:
    def __init__(self):
        self.crawled_folder = Path(os.path.abspath('')) / 'crawled/'
        self.stored_file = './manual_indexer.pkl'
        if os.path.isfile(self.stored_file):
            with open(self.stored_file, 'rb') as f:
                cached_dict = pickle.load(f)
                self.__dict__.update(cached_dict)
        else:
            self.run_indexer()
    
    def pre_process(self, s: str):
        return s.lower()

    def run_indexer(self):
        documents = []
        for file in os.listdir(self.crawled_folder):
            if file.endswith(".txt"):
                j = json.load(open(os.path.join(self.crawled_folder, file)))
                documents.append(j)
        self.documents = pd.DataFrame.from_dict(documents)
        tfidf_vectorizer = TfidfVectorizer(preprocessor=self.pre_process, stop_words=stopwords.words('english'))
        self.bm25 = BM25(tfidf_vectorizer)
        self.bm25.fit(self.documents.apply(lambda s: ' '.join(s[['title', 'text']]), axis=1))
        with open(self.stored_file, 'wb') as f:
            pickle.dump(self.__dict__, f)