"""
rag_retriever.py

RAG retriever with two interchangeable backends:

    - "tfidf"      : TF-IDF + cosine similarity. Zero downloads, runs
                     anywhere, good for quick iteration and as a
                     lightweight/edge-realistic baseline.
    - "embedding"  : sentence-transformers (all-MiniLM-L6-v2) + cosine
                     similarity. Realistic modern dense-retrieval RAG,
                     matches what PoisonedRAG/BadRAG/Phantom test against
                     and what production systems like ChatIoT-style
                     assistants actually use.

Both backends expose the same interface (retrieve, add_documents), so the
rest of the pipeline (attack scripts, defense, evaluation) does not care
which one is active.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TfidfRetriever:

    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english")
        corpus_texts = [doc["text"] for doc in self.documents]
        self.doc_matrix = self.vectorizer.fit_transform(corpus_texts)

    def retrieve(self, query, top_k=3):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.doc_matrix)[0]
        ranked = sorted(
            zip(self.documents, scores), key=lambda p: p[1], reverse=True
        )

        return ranked[:top_k]

    def add_documents(self, new_documents):
        self.documents = self.documents + new_documents
        corpus_texts = [doc["text"] for doc in self.documents]
        self.doc_matrix = self.vectorizer.fit_transform(corpus_texts)


class EmbeddingRetriever:
    """
    Requires: pip install sentence-transformers
    Downloads the model the first time it runs (needs internet once;
    cached locally afterward under ~/.cache/huggingface).

    Default model changed from all-MiniLM-L6-v2 to BAAI/bge-m3.
    all-MiniLM-L6-v2 is trained mostly on English and general web text,
    so its representation of Hausa, Yoruba, and Igbo is unreliable.
    BGE-M3 is evaluated directly on these three languages in published
    research (Improving BGE-M3 Multilingual Dense Embeddings for
    Nigerian Low Resource Languages, ACL WiNLP 2025), where it
    outperforms other multilingual options including LaBSE on Yoruba
    retrieval specifically. That's a stronger evidence base than a
    general multilingual benchmark average.
    """

    def __init__(self, documents, model_name="BAAI/bge-m3"):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)
        self.documents = documents
        self._embed_corpus()

    def _embed_corpus(self):
        texts = [doc["text"] for doc in self.documents]
        # normalize_embeddings=True makes cosine similarity a simple dot
        # product, which is what util.cos_sim relies on internally.
        self.doc_embeddings = self.model.encode(
            texts, normalize_embeddings=True, convert_to_numpy=True
        )

    def retrieve(self, query, top_k=3):
        from sentence_transformers import util

        query_embedding = self.model.encode(
            [query], normalize_embeddings=True, convert_to_numpy=True
        )
        scores = util.cos_sim(query_embedding, self.doc_embeddings)[0].tolist()
        ranked = sorted(
            zip(self.documents, scores), key=lambda p: p[1], reverse=True
        )
        return ranked[:top_k]

    def add_documents(self, new_documents):
        self.documents = self.documents + new_documents
        self._embed_corpus()


def get_retriever(backend, documents):
    """
    Factory function. backend: "tfidf" or "embedding".

    Every other script (phase1_baseline.py, phase2_attack.py, etc.) should
    call this instead of instantiating a retriever class directly, so
    switching backends is a one-line change wherever the retriever is
    created.
    """
    
    if backend == "tfidf":
        return TfidfRetriever(documents)
    elif backend == "embedding":
        return EmbeddingRetriever(documents)
    else:
        raise ValueError(f"Unknown backend: {backend!r}. Use 'tfidf' or 'embedding'.")