import os
import streamlit as st
from config import DOCS_DIR, INDEX_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBED_BATCH_SIZE
from core.splitter import load_chunks_from_files
from core.embedder import get_embeddings
from core.retriever import build_faiss_index, get_top_k_chunks
from core.generator import ask_llm
from core.rewrite import rewrite_query
from core.index_manager import save_index, load_index, append_to_index, get_next_chunk_id
from core.file_registry import is_file_duplicate, register_file
from core.agent import classify_question
from core.tools import calculator_tool

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

st.set_page_config(page_title="多文档 RAG 问答系统", layout="wide")
st.title("多文档 RAG 问答系统")

# 保存聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("文档管理")

    uploaded_files = st.file_uploader(
        "上传 PDF 或 DOCX 文件",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        file_names = [f.name for f in uploaded_files]
        st.text("当前上传文件： " + ", ".join(file_names))

        if st.button("上传并自动更新索引"):
            with st.spinner("正在上传文件并自动更新索引..."):
                saved_paths = []
                skipped_files = []

                for uploaded_file in uploaded_files:
                    save_path = os.path.join(DOCS_DIR, uploaded_file.name)

                    # 先保存临时文件
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # 去重检测
                    if is_file_duplicate(save_path):
                        skipped_files.append(uploaded_file.name)
                        os.remove(save_path)
                        continue

                    register_file(save_path)
                    saved_paths.append(save_path)

                # 如果没有任何新文件
                if not saved_paths:
                    st.warning("没有新文件被加入索引。")
                else:
                    try:
                        # 如果已有索引，则增量追加
                        start_id = get_next_chunk_id(save_dir=INDEX_DIR)
                        new_chunks = load_chunks_from_files(
                            saved_paths,
                            chunk_size=500,
                            chunk_overlap=100,
                            start_id=start_id
                        )
                        append_to_index(new_chunks, save_dir=INDEX_DIR)
                        st.success(f"自动更新完成，新增 {len(new_chunks)} 个文本片段。")
                    except FileNotFoundError:
                        # 如果还没有索引，则首次构建
                        chunks = load_chunks_from_files(
                            saved_paths,
                            chunk_size=500,
                            chunk_overlap=100,
                            start_id=0
                        )
                        vectors = get_embeddings(chunks, batch_size=10)
                        index = build_faiss_index(vectors)
                        save_index(index, chunks, save_dir=INDEX_DIR)
                        st.success(f"首次索引构建完成，共 {len(chunks)} 个文本片段。")

                if skipped_files:
                    st.warning("以下文件已存在，已跳过： " + ", ".join(skipped_files))

    if st.button("重建索引（基于 docs 目录全部文件）"):
        file_paths = [
            os.path.join(DOCS_DIR, f)
            for f in os.listdir(DOCS_DIR)
            if f.lower().endswith((".pdf", ".docx"))
        ]

        if not file_paths:
            st.warning("docs/ 目录中没有 PDF 或 DOCX 文件。")
        else:
            with st.spinner("正在解析文档、生成向量并构建索引..."):
                chunks = load_chunks_from_files(
                    file_paths,
                    chunk_size=500,
                    chunk_overlap=100,
                    start_id=0
                )
                vectors = get_embeddings(chunks, batch_size=10)
                index = build_faiss_index(vectors)
                save_index(index, chunks, save_dir=INDEX_DIR)

            st.success(f"索引构建完成。共 {len(chunks)} 个文本片段。")

    if st.button("查看当前文档列表"):
        doc_files = [
            f for f in os.listdir(DOCS_DIR)
            if f.lower().endswith((".pdf", ".docx"))
        ]
        if doc_files:
            st.write(doc_files)
        else:
            st.info("docs/ 目录暂无文档。")

    if st.button("清空聊天记录"):
        st.session_state.messages = []
        st.success("聊天记录已清空。")

st.subheader("聊天记录")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

top_k = st.slider("检索 Top-K", min_value=1, max_value=8, value=3)

question = st.chat_input("请输入你的问题")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    try:
        # Agent 判断问题类型
        with st.spinner("Agent 正在分析问题..."):
            task_type = classify_question(question)

        st.write("Agent 判断任务类型：", task_type)

        if task_type == "RAG":

            with st.spinner("正在加载索引..."):
                index, chunks = load_index(save_dir=INDEX_DIR)

            with st.spinner("正在改写问题..."):
                rewritten_question = rewrite_query(
                    question,
                    chat_history=st.session_state.messages
                )

            with st.spinner("正在检索相关片段..."):
                retrieved = get_top_k_chunks(
                    rewritten_question,
                    chunks,
                    index,
                    top_k=top_k
                )

            with st.expander("查看改写后的检索问题"):
                st.write(rewritten_question)

            with st.spinner("正在生成答案..."):
                answer = ask_llm(
                    question,
                    retrieved,
                    chat_history=st.session_state.messages
                )

        elif task_type == "CALCULATOR":

            with st.spinner("正在调用计算器工具..."):
                retrieved = []
                answer = calculator_tool(question)

        else:

            with st.spinner("直接调用大模型回答..."):
                retrieved = []
                answer = ask_llm(
                    question,
                    retrieved,
                    chat_history=st.session_state.messages
                )

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.markdown("### 本轮引用来源")
        for i, (chunk, score) in enumerate(retrieved, 1):
            with st.expander(
                f"{i}. 来源={chunk['source']} | 片段ID={chunk['id']} | 相似度={score:.4f}"
            ):
                st.write(chunk["text"])

    except FileNotFoundError:
        st.error("还没有索引，请先在左侧点击“重建索引”。")
    except Exception as e:
        st.error(f"运行出错：{e}")