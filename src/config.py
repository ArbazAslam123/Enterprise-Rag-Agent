import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

@dataclass(frozen=True)
class AppConfig:
    """Read-only system configuration using the OOP Dataclass pattern."""

    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")

    # Embedding Model (Convert Text to Vectors)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM Inference Model via Groq
    llm_model: str = "qwen/qwen3.6-27b"

    # Cross-Encoder Re-Ranker Model
    rerank_model: str = "ms-marco-MiniLM-L-12-v2"

    # Chunking boundaries
    chunk_size: int = 500  # Number of tokens per chunk
    chunk_overlap: int = 50  # Number of overlapping tokens between chunks

    # Vector Storage Settings
    collection_name: str = "enterprise_policy"

# Instantiate the configuration object for global use
config = AppConfig()

# Checking for API key presence
if not config.groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")