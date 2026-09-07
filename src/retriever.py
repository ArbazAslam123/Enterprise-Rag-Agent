from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.document_compressors import FlashrankRerank
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_qdrant import QdrantVectorStore
from src.config import config

class EnterpriseRetriever:
    """Combines vector search and keyword search, then re-ranks the best results."""

    def __init__(self,vector_store: QdrantVectorStore, chunks: list):
        # OOP Composition: we pass the vector_store and chunks into this object
        self.vector_store = vector_store
        self.chunks = chunks

        # Setup Keyword Search Retriever (BM25)
        print("Initializing BM25 Keyword Search Retriever...")
        self.bm25_retriever = BM25Retriever.from_documents(self.chunks)
        self.bm25_retriever.k = 5  # Get 5 exact keyword matches

        # Setup Vector Search Retriever (Qdrant)
        print("Initializing Qdrant Semantic Search Retriever...")
        self.vector_retriever = self.vector_store.as_retriever(search_kwargs={"k": 5}) # Get 5 semantic matches

        # Combine then into Hybrid Retriever (Ensemble)
        # Weights: 50% keyword, 50% semantic meaning
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.5, 0.5]
        )

        # Setup the Re-ranker (The Judge)
        self.compressor = FlashrankRerank(
            model=config.rerank_model,
            top_n=4,
        )

        # Wrap the Hybrid Retriever inside the Re-ranker
        self.final_retriever = ContextualCompressionRetriever(
            base_compressor=self.compressor,
            base_retriever=self.hybrid_retriever
        )

    def search(self, query: str):
        """Facade Method: Takes a question and retunrs the smartest, re-ranked chunks"""
        print(f"\n Searching for: '{query}'")

        # This single line runs BM25, runs Qdrant, merges them, and re-ranks them!
        results = self.final_retriever.invoke(query)

        return results
