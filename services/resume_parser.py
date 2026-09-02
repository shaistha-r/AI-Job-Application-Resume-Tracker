from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type")
    text = " ".join(text.split())
    if not text:
        raise ValueError("No readable text was found in the document")
    return text[:100000]
