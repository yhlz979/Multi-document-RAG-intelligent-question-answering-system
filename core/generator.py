from openai import OpenAI
from config import DASHSCOPE_API_KEY, BASE_URL, CHAT_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=BASE_URL
)


def ask_llm(question: str, retrieved=None, chat_history=None) -> str:
    if retrieved:
        context = "\n\n".join(
            [
                f"[来源:{chunk['source']} | 片段ID:{chunk['id']} | 相似度:{score:.4f}]\n{chunk['text']}"
                for chunk, score in retrieved
            ]
        )
    else:
        context = "当前没有检索到知识库资料，请直接根据常识与对话上下文回答。"

    history_text = ""
    if chat_history:
        history_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in chat_history[-6:]]
        )

    prompt = f"""
请根据给定上下文回答问题。

历史对话：
{history_text}

资料：
{context}

当前问题：
{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个智能助手，请尽量基于提供的上下文回答。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content