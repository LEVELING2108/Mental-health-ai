import os

import chromadb
from chromadb.utils import embedding_functions

from core.logger import setup_logger

logger = setup_logger(__name__)

class RAGEngine:
    def __init__(self, persist_directory="data/vector_db"):
        self.persist_directory = persist_directory

        # 1. Setup ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # 2. Use a high-quality local embedding model (no API key needed)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # 3. Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name="mental_health_knowledge",
            embedding_function=self.embedding_fn
        )

        # 4. Always index on startup to pick up new/updated files
        self.index_knowledge_base()

    def index_knowledge_base(self):
        """Index all markdown files from data/knowledge_base into the vector DB."""
        kb_path = "data/knowledge_base"
        if not os.path.exists(kb_path):
            logger.warning(f"Knowledge base directory {kb_path} not found.")
            return

        logger.info(f"Checking knowledge base at {kb_path}...")

        documents = []
        ids = []
        metadatas = []

        for filename in os.listdir(kb_path):
            if filename.endswith(".md"):
                file_path = os.path.join(kb_path, filename)
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                    documents.append(content)
                    ids.append(filename)
                    metadatas.append({"source": filename})

        if documents:
            # Use upsert to handle updates and additions gracefully
            self.collection.upsert(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            logger.info(f"Knowledge base synced: {self.collection.count()} documents total.")

    def query(self, text: str, n_results: int = 1) -> str:
        """Search for the most relevant medical guidance."""
        try:
            results = self.collection.query(
                query_texts=[text],
                n_results=n_results
            )

            if results["documents"] and results["documents"][0]:
                return results["documents"][0][0]
            return ""
        except Exception as e:
            logger.error(f"RAG Query failed: {e}")
            return ""

# Singleton instance
rag_engine = RAGEngine()
