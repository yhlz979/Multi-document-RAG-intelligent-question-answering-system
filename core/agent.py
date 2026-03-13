from openai import OpenAI
from config import DASHSCOPE_API_KEY, BASE_URL, CHAT_MODEL
from core.tools import calculator_tool

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=BASE_URL
)


def classify_question(question: str) -> str:
    prompt = f"""
你是一个任务分类助手。

请判断用户问题应该交给哪种工具处理。

规则：
1. 如果问题涉及文档知识、技术概念、系统原理、资料问答 → 返回 RAG
2. 如果问题涉及数学计算、加减乘除、百分比、数值运算 → 返回 CALCULATOR
3. 如果是普通聊天、泛化解释、非知识库问题 → 返回 LLM

只返回一个词：
RAG
CALCULATOR
LLM

问题：
{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    decision = response.choices[0].message.content.strip().upper()

    if "CALCULATOR" in decision:
        return "CALCULATOR"
    elif "RAG" in decision:
        return "RAG"
    else:
        return "LLM"