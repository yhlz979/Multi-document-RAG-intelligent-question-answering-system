import json

from core.index_manager import load_index
from core.retriever import get_top_k_chunks
from core.generator import ask_llm
from core.rewrite import rewrite_query


def keyword_hit_rate(answer, keywords):
    if not keywords:
        return 0.0
    hit = sum(1 for k in keywords if k in answer)
    return hit / len(keywords)


def recall_at_k(retrieved, expected_sources):
    retrieved_sources = {chunk["source"] for chunk, _ in retrieved}
    expected_sources = set(expected_sources)
    if not expected_sources:
        return 0.0
    return 1.0 if len(retrieved_sources & expected_sources) > 0 else 0.0


def evaluate_once(question, expected_keywords, expected_sources, chunks, index, use_rewrite=True, top_k=3):
    query = question
    if use_rewrite:
        query = rewrite_query(question, chat_history=None)

    retrieved = get_top_k_chunks(query, chunks, index, top_k=top_k)
    answer = ask_llm(question, retrieved, chat_history=None)

    keyword_score = keyword_hit_rate(answer, expected_keywords)
    recall_score = recall_at_k(retrieved, expected_sources)

    return {
        "query": query,
        "retrieved": retrieved,
        "answer": answer,
        "keyword_score": keyword_score,
        "recall_score": recall_score
    }


def run_experiment(eval_set, chunks, index, use_rewrite, top_k):
    total_keyword = 0.0
    total_recall = 0.0

    for item in eval_set:
        result = evaluate_once(
            question=item["question"],
            expected_keywords=item["expected_keywords"],
            expected_sources=item["expected_sources"],
            chunks=chunks,
            index=index,
            use_rewrite=use_rewrite,
            top_k=top_k
        )

        total_keyword += result["keyword_score"]
        total_recall += result["recall_score"]

    n = len(eval_set)
    return {
        "avg_keyword_score": total_keyword / n,
        "avg_recall_score": total_recall / n
    }


def main():
    with open("data/eval_set.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    index, chunks = load_index()

    print("=" * 80)
    print("RAG 实验对比")
    print("=" * 80)

    # 1. Top-K 对比（固定 use_rewrite=True）
    print("\n[实验一] Top-K 对比（开启 Rewrite）")
    for top_k in [1, 3, 5]:
        metrics = run_experiment(
            eval_set=eval_set,
            chunks=chunks,
            index=index,
            use_rewrite=True,
            top_k=top_k
        )
        print(
            f"Top-K={top_k} | "
            f"Recall={metrics['avg_recall_score']:.2%} | "
            f"关键词命中率={metrics['avg_keyword_score']:.2%}"
        )

    # 2. Rewrite 对比（固定 top_k=3）
    print("\n[实验二] Rewrite 对比（Top-K=3）")
    for use_rewrite in [False, True]:
        metrics = run_experiment(
            eval_set=eval_set,
            chunks=chunks,
            index=index,
            use_rewrite=use_rewrite,
            top_k=3
        )
        mode = "Rewrite" if use_rewrite else "No Rewrite"
        print(
            f"{mode} | "
            f"Recall={metrics['avg_recall_score']:.2%} | "
            f"关键词命中率={metrics['avg_keyword_score']:.2%}"
        )


if __name__ == "__main__":
    main()