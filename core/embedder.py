from openai import OpenAI
from config import DASHSCOPE_API_KEY, BASE_URL, EMBEDDING_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=BASE_URL
)


def get_embeddings(chunks, batch_size=10):
    texts = [chunk["text"] for chunk in chunks]
    vectors = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        emb = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch
        )

        batch_vectors = [item.embedding for item in emb.data]
        vectors.extend(batch_vectors)

    return vectors


def get_query_embedding(question: str):
    emb = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question
    )
    return emb.data[0].embedding