# 多文档 RAG 智能问答系统
基于 RAG（Retrieval-Augmented Generation） 构建的多文档知识库问答系统。
系统支持 PDF / DOCX 文档解析、向量检索、Query Rewrite、多轮对话、引用来源展示以及增量索引更新，通过 向量检索 + 大模型生成 的方式实现企业知识库问答。

## 项目简介
在企业知识管理场景中，常见的问题包括：
- 文档内容分散，人工检索效率低
- 大模型直接回答缺乏外部知识支撑，容易产生幻觉
- 文档更新频繁，重建索引成本高

本项目通过 RAG（Retrieval-Augmented Generation）架构解决这些问题，实现完整的知识库问答流程：
文档解析 → 文本切分 → 向量化 → 向量检索 → 问题改写 → 回答生成 → 引用来源展示

## 系统流程
系统核心流程如下：

用户问题
   │
   ▼
Query Rewrite
   │
   ▼
向量检索（FAISS）
   │
   ▼
Top-K 文本片段
   │
   ▼
LLM 基于上下文生成答案
   │
   ▼
返回答案 + 引用来源

## 功能特性
| 功能 | 描述 |
| ---- | ---- |
| 文档解析 | 支持 PDF / DOCX 文档上传 |
| 文本切分 | chunk + overlap 文本切分 |
| 向量检索 | Embedding + FAISS 相似度检索 |
| Top-K Retrieval | 检索最相关文本片段 |
| Query Rewrite | 提升多轮对话检索效果 |
| 来源引用 | 展示回答引用的文档来源 |
| 增量索引 | 新文档加入无需重建索引 |
| 文件去重 | 基于 hash 的文档去重 |
| Web UI | Streamlit 可视化界面 |

## 示例
用户问题：
什么是 RAG？

系统回答：
RAG（Retrieval-Augmented Generation）是一种结合信息检索与文本生成的大模型架构，
通过从外部知识库检索相关内容并结合生成模型生成回答。

引用来源：
rag.docx
chunk id: 12
similarity: 0.87

## 系统架构
文档上传 (PDF / DOCX)
        │
    Hash 去重
        │
    文档解析
        │
chunk 切分 + overlap
        │
Embedding 向量化
        │
FAISS 向量索引
        │
Query Rewrite
        │
Top-K 相似度检索
        │
LLM 基于上下文生成答案
        │
引用来源展示 + 前端交互

## 安装依赖
pip install -r requirements.txt

## 配置 API Key
如果使用 DashScope / OpenAI 兼容 API：
export DASHSCOPE_API_KEY="your_api_key"
或者在 config.py 中配置。

## 运行系统
启动 Web 界面：
streamlit run app.py

浏览器访问：
http://localhost:8501

## 离线评测
项目提供 evaluate.py 用于系统效果评估。

评测指标：
Recall@K
Answer Keyword Hit Rate

运行评测：
python evaluate.py

实验内容：
Top-K 对比
Rewrite vs No-Rewrite

## 技术栈
Python
Streamlit
FAISS
LLM API
RAG

## 未来改进
未来可以扩展：
Web Search Tool
向量数据库（Milvus / Chroma）
OCR PDF 解析
Streaming Answer
多 Agent 协作

