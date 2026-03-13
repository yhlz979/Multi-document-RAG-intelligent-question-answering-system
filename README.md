多文档 RAG 智能问答系统
一个基于 Python、Streamlit、FAISS 和大模型 API 构建的多文档 RAG 问答系统，支持 PDF / DOCX 文档解析、向量检索、多轮对话、Query Rewrite、来源引用展示以及增量索引更新。
系统通过 向量检索 + 大模型生成 的方式实现知识库问答，并展示引用来源，提高回答的可解释性。
项目简介
本项目面向 企业知识库问答场景，主要解决以下问题：
文档内容分散，人工检索效率低
大模型直接回答缺乏外部知识支撑，容易产生幻觉
文档持续更新时，全量重建索引成本高
因此，本项目实现了一套完整的 RAG（Retrieval-Augmented Generation）流程，包括：
文档解析
文本切分
向量化
向量检索
问题改写
回答生成
引用来源展示
Demo
系统提供基于 Streamlit 的 Web 界面，支持：
文档上传
多轮对话
检索来源展示
Query Rewrite 显示
示例交互：
用户问题：
什么是 RAG？
系统回答：
RAG（Retrieval-Augmented Generation）是一种结合信息检索和文本生成的大模型架构，通过从外部知识库检索相关内容并结合生成模型生成回答。
引用来源：
rag.docx
chunk id: 12
similarity: 0.87
如果需要展示项目效果，可以在仓库中添加截图：
assets/demo.png
并在 README 中展示：
功能特性
支持 PDF / DOCX 文档上传
支持 多文档知识库构建
支持 chunk + overlap 文本切分
支持 Embedding 向量化
基于 FAISS 的 Top-K 相似度检索
支持 Query Rewrite 提升检索效果
支持 引用来源展示
支持 增量索引更新
支持 文件 hash 去重
提供 Streamlit 前端界面
系统架构
文档上传 (PDF / DOCX)
        ↓
     Hash 去重
        ↓
     文档解析
        ↓
chunk 切分 + overlap
        ↓
Embedding 向量化
        ↓
FAISS 向量索引
        ↓
Query Rewrite
        ↓
Top-K 相似度检索
        ↓
LLM 基于上下文生成答案
        ↓
引用来源展示 + 前端交互
项目结构
rag-doc-qa/
│
├── app.py                # Streamlit 前端
├── config.py             # API 配置
├── evaluate.py           # 离线评测脚本
├── metadata.json         # 文档注册表
├── requirements.txt
│
├── core/
│   ├── loader.py         # 文档解析
│   ├── splitter.py       # 文本切分
│   ├── embedder.py       # 向量生成
│   ├── retriever.py      # 向量检索
│   ├── rewrite.py        # Query Rewrite
│   ├── generator.py      # LLM 生成
│   ├── index_manager.py  # FAISS 索引管理
│   └── file_registry.py  # 文件去重
│
├── docs/                 # 知识库文档
├── data/
│   └── eval_set.json     # 测试集
│
└── index_store/          # 向量索引
安装依赖
pip install -r requirements.txt
配置 API Key
如果使用 DashScope / OpenAI 兼容 API：
export DASHSCOPE_API_KEY="your_api_key"
或者在 config.py 中填写。
运行系统
启动 Web 界面：
streamlit run app.py
浏览器访问：
http://localhost:8501
离线评测
项目提供 evaluate.py 用于系统效果评估。
评测指标：
Recall@K
Answer Keyword Hit Rate
运行评测：
python evaluate.py
实验包括：
Top-K 对比
Rewrite vs No-Rewrite
技术栈
Python
Streamlit
FAISS
LLM API
RAG
未来改进
未来可以扩展：
Web Search Tool
向量数据库（Milvus / Chroma）
OCR PDF 解析
Streaming Answer
多 Agent 协作
