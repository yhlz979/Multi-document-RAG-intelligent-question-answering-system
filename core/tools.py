def calculator_tool(question: str) -> str:

    try:
        expr = question.replace("等于多少", "").replace("等于几", "").strip()
        result = eval(expr, {"__builtins__": {}})
        return f"计算结果是：{result}"
    except Exception:
        return "计算器工具无法解析这个表达式。"