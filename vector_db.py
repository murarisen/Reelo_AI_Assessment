import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorDB:
    """
    A wrapper around Chroma vector store for adding and querying Google Reviews using HuggingFace embeddings.
    """

    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the vector database with a persistence directory.
        Uses HuggingFace embeddings by default.
        """
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        logging.info("VectorDB initialized with HuggingFace embeddings.")

    def add_reviews(self, reviews: List[Dict]):
        texts = [review.get("text", "").strip() for review in reviews if review.get("text", "").strip()]
        if not texts:
            logging.warning("No valid review texts to add.")
            return
        try:
            self.db.add_texts(texts)
            logging.info(f"Added {len(texts)} reviews to the vector DB.")
        except Exception as e:
            logging.error(f"Failed to add reviews to vector DB: {e}")

    def query(self, query_text: str, k: int = 5) -> List[str]:
        query_text = query_text.strip()
        if not query_text:
            logging.warning("Query text is empty.")
            return []
        try:
            results = self.db.similarity_search(query_text, k=k)
            logging.info(f"Retrieved {len(results)} search results for query: '{query_text}'")
            return [doc.page_content for doc in results]
        except Exception as e:
            logging.error(f"Query failed: {e}")
            return []

    def persist(self):
        try:
            self.db.persist()
            logging.info("Vector DB persisted successfully.")
        except Exception as e:
            logging.error(f"Failed to persist vector DB: {e}")


if __name__ == "__main__":
    vector_db = VectorDB()

    sample_reviews = [
        {"text": "Great service and friendly staff."},
        {"text": "The product quality was poor and delivery was late."},
        {"text": "Affordable and tasty meals."}
    ]

    vector_db.add_reviews(sample_reviews)
    vector_db.persist()

    query_results = vector_db.query("complaints about delivery")
    logging.info(f"Query Results: {query_results}")
