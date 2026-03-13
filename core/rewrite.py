from openai import OpenAI
from config import DASHSCOPE_API_KEY, BASE_URL, CHAT_MODEL

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=BASE_URL
)


def rewrite_query(question: str, chat_history=None) -> str:
    if not chat_history:
        return question

    history_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in chat_history[-6:]]
    )

    prompt = f"""
你是一个查询改写助手。

任务：
根据历史对话，把当前用户问题改写成一个独立、完整、明确的问题，
以便用于知识库检索。

要求：
1. 保留用户原意
2. 补全代词指代
3. 不要回答问题，只输出改写后的问题
4. 如果当前问题已经足够完整，就直接原样输出

历史对话：
{history_text}

当前问题：
{question}

改写后的完整问题：
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()