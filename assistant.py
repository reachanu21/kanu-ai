import re
import PyPDF2

def chunk_text(self, text, max_len=500):
    """
    Sentence-aware chunking for RAG.
    Splits text into sentences, then groups them into ~500-word chunks.
    """
    # 1. Split into sentences using regex
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current = []

    for sentence in sentences:
        words = sentence.split()

        # If adding this sentence exceeds max_len → commit current chunk
        if len(current) + len(words) > max_len:
            chunks.append(" ".join(current))
            current = []

        current.extend(words)

    # Add last chunk
    if current:
        chunks.append(" ".join(current))

    return chunks


def ingest_document(self, file):
    """
    Extracts text from PDF or text files, chunks it, and stores chunks in RAG.
    Returns the number of chunks added.
    """

    # 1. Extract text
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = file.read().decode("utf-8", errors="ignore")

    # 2. Chunk text
    chunks = self.chunk_text(text)

    # 3. Add chunks to RAG
    for chunk in chunks:
        self.rag.add_document(chunk)

    return len(chunks)
