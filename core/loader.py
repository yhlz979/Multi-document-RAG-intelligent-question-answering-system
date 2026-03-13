import os
from pypdf import PdfReader
from docx import Document


def load_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    texts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texts.append(page_text)

    return "\n".join(texts)


def load_docx_text(file_path: str) -> str:
    doc = Document(file_path)
    texts = []

    for para in doc.paragraphs:
        if para.text.strip():
            texts.append(para.text.strip())

    return "\n".join(texts)


def load_text_from_file(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        return load_pdf_text(file_path)
    elif file_path.lower().endswith(".docx"):
        return load_docx_text(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_path}")