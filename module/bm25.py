from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import numpy as np
from nltk.corpus import stopwords

class BM25(object):
    def __init__(self, vectorizer, b=0.75, k1=1.6):
        if not isinstance(vectorizer, TfidfVectorizer):
            raise ValueError("Vectorizer must be an instance of TfidfVectorizer")
        self.vectorizer = vectorizer
        self.b = b
        self.k1 = k1

    def fit(self, X):
        # Fit the vectorizer and transform the document set
        self.vectorizer.fit(X)
        self.y = self.vectorizer.transform(X)

        # Calculate the average document length
        self.avdl = self.y.sum(1).mean()

    def transform(self, q):
        # Ensure the input query is a list
        if not isinstance(q, list):
            q = [q]

        # Transform the query using the vectorizer
        q_vector = self.vectorizer.transform(q)
        assert sparse.isspmatrix_csr(q_vector)

        # Calculate BM25 scores
        len_y = self.y.sum(1).A1
        y = self.y.tocsc()[:, q_vector.indices]
        denom = y + (self.k1 * (1 - self.b + self.b * len_y / self.avdl))[:, None]
        idf = self.vectorizer._tfidf.idf_[None, q_vector.indices] - 1
        numerator = y.multiply(np.broadcast_to(idf, y.shape)) * (self.k1 + 1)
        return (numerator / denom).sum(1).A1