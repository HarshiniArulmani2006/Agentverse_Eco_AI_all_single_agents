import os
import glob
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self):
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.loaded = False
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        kb_dir = Config.KNOWLEDGE_BASE_DIR
        if not os.path.exists(kb_dir):
            logger.warning(f"Knowledge base directory not found at {kb_dir}")
            return

        txt_files = glob.glob(os.path.join(kb_dir, "*.txt"))
        chunks = []

        for filepath in txt_files:
            topic_name = os.path.basename(filepath).replace(".txt", "")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                
                # Simple chunking by double newlines / numbered sections
                sections = text.split("\n\n")
                for sec in sections:
                    clean_sec = sec.strip()
                    if len(clean_sec) > 30:
                        chunks.append({
                            "topic": topic_name,
                            "content": clean_sec
                        })
            except Exception as e:
                logger.error(f"Error reading knowledge file {filepath}: {e}")

        if chunks:
            self.documents = chunks
            corpus = [doc["content"] for doc in chunks]
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
            self.loaded = True
            logger.info(f"Loaded RAG engine with {len(chunks)} chunks across {len(txt_files)} files.")

    def search(self, query, top_k=3):
        if not self.loaded or not self.vectorizer or self.tfidf_matrix is None:
            return []

        try:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            top_indices = scores.argsort()[::-1][:top_k]

            results = []
            for idx in top_indices:
                if scores[idx] > 0.05:  # threshold score
                    results.append({
                        "content": self.documents[idx]["content"],
                        "topic": self.documents[idx]["topic"],
                        "score": float(scores[idx])
                    })
            return results
        except Exception as e:
            logger.error(f"RAG search error: {e}")
            return []

rag_engine = RAGEngine()
