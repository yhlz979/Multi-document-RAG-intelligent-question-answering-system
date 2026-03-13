from core.loader import load_text_from_file


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100):
    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - chunk_overlap

    return chunks


def load_chunks_from_files(file_paths, chunk_size=500, chunk_overlap=100, start_id=0):
    chunks = []
    chunk_id = start_id

    for file_path in file_paths:
        full_text = load_text_from_file(file_path)
        raw_chunks = split_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for i, chunk in enumerate(raw_chunks):
            chunks.append({
                "id": chunk_id,
                "source": file_path.split("/")[-1],
                "source_path": file_path,
                "chunk_index": i,
                "text": chunk
            })
            chunk_id += 1

    return chunks