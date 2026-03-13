import os
import pickle
import faiss
import numpy as np

from core.embedder import get_embeddings


def save_index(index, chunks, save_dir="index_store"):
    os.makedirs(save_dir, exist_ok=True)

    faiss.write_index(index, os.path.join(save_dir, "faiss.index"))

    with open(os.path.join(save_dir, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)


def load_index(save_dir="index_store"):
    index_path = os.path.join(save_dir, "faiss.index")
    chunks_path = os.path.join(save_dir, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError("索引文件不存在，请先构建索引。")

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def append_to_index(new_chunks, save_dir="index_store"):
    index, old_chunks = load_index(save_dir=save_dir)

    new_vectors = get_embeddings(new_chunks, batch_size=10)
    new_vectors_np = np.array(new_vectors, dtype="float32")
    faiss.normalize_L2(new_vectors_np)

    index.add(new_vectors_np)

    all_chunks = old_chunks + new_chunks
    save_index(index, all_chunks, save_dir=save_dir)


def get_next_chunk_id(save_dir="index_store"):
    try:
        _, chunks = load_index(save_dir=save_dir)
        if not chunks:
            return 0
        return max(chunk["id"] for chunk in chunks) + 1
    except FileNotFoundError:
        return 0
