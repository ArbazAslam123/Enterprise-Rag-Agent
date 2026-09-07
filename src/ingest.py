import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from src.config import config

class DocumentIngestionPipeline:
    """Pipeline responsible for loading, chunking, and indexing enterprise text."""

    def __init__(self):
        # Initialize the embedding model (converts text to numbers)
        self.embedding = HuggingFaceEmbeddings(model_name=config.embedding_model)

        # Connect to in memory Qdrant vector database
        self.client = QdrantClient(":memory:")

        # Create the database table using settings from config.py
        self.client.create_collection(
            collection_name=config.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    def load_document(self, file_path: str) -> str:
            """Reads the raw text file from the data folder."""
            with open(file_path,"r", encoding ="utf-8") as f:
                text = f.read()
            print(f"loaded document '{file_path}' ({len(text)} characters.)")
            return text

    def chunk_text(self, raw_text: str, source_label: str) -> list[Document]:
            """Slices the raw text file from the data folder."""
            splitter= RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                separators=["\n\n", "\n", " ",""],
            )

            # chop the text into pieces and attach a label[metadata]
            chunks = splitter.create_documents(
                texts=[raw_text],
                metadatas=[{"source": source_label}],
            )

            # Add a unique ID to every chunk so we can track it later
            for idx, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = f"{source_label}_chunk_{idx}"

            print(f" Sliced text into {len(chunks)} individual chunks.")
            return chunks    

    def build_vector_store(self, chunks: list[Document]) -> tuple[QdrantVectorStore, list[Document]]:
            """Converts chunks into vectors and saves them in Qdrant."""
            print(f"Indexing chunks into Qdrant collection '{config.collection_name}'.")

            vector_store = QdrantVectorStore(
                  client=self.client,
                  collection_name=config.collection_name,
                  embedding=self.embedding,
            )

            # Save the chunks into our database
            vector_store.add_documents(chunks)
            print(f"Vector indexing complete:")
            return vector_store, chunks

    def run(self, file_path: str) -> tuple[QdrantVectorStore, list[Document]]:
            """Facade Method: The single button to run the whole assembly line."""
            raw_text=self.load_document(file_path)

            # Extract just the file name for the label
            file_name= os.path.basename(file_path)

            chunks = self.chunk_text(raw_text, source_label=file_name)
            vector_store, indexed_chunks = self.build_vector_store(chunks)

            return vector_store, indexed_chunks

