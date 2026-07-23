# config.py
from dotenv import load_dotenv
import os

load_dotenv()

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"           # cheaper than gpt-4o, good enough for MVP

# Embeddings — switching from OpenAI to BGE (free, local, competitive quality)
EMBEDDING_MODEL = "text-embedding-3-small"

# ChromaDB
CHROMA_PERSIST_DIR = "db/chroma_db"
CHROMA_COLLECTION = "research_papers"

# Retrieval
TOP_K = 5                               # how many chunks to retrieve

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100                     # was 0 in your code — overlap prevents
                                        # answers being split across chunk boundaries