import faiss
import numpy as np
from core.embedder import get_query_embedding


def build_faiss_index(vectors):
    vectors_np = np.array(vectors, dtype="float32")
    faiss.normalize_L2(vectors_np)

    dimension = vectors_np.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors_np)
    return index


def get_top_k_chunks(question, chunks, index, top_k=3):
    question_vector = get_query_embedding(question)

    question_np = np.array([question_vector], dtype="float32")
    faiss.normalize_L2(question_np)

    scores, indices = index.search(question_np, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            results.append((chunks[idx], float(score)))

    return results