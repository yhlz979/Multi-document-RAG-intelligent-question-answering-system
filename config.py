import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

EMBEDDING_MODEL = "text-embedding-v4"
CHAT_MODEL = "qwen-plus"

DOCS_DIR = "docs"
INDEX_DIR = "index_store"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBED_BATCH_SIZE = 10
TOP_K = 3