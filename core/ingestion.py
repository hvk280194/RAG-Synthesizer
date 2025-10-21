from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict

def load_pdfs(files: List) -> List[Dict]:
    """Extract text chunks from uploaded PDFs."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    all_chunks = []
    for file in files:
        reader = PdfReader(file)
        text = " ".join(page.extract_text() or "" for page in reader.pages)
        chunks = text_splitter.split_text(text)
        for c in chunks:
            all_chunks.append({"source": file.name, "content": c})
    return all_chunks
