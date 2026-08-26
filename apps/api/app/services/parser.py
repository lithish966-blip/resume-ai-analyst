import re
from pathlib import Path
import fitz
from docx import Document


def parse_resume(path: str, file_type: str) -> str:
    if file_type == "pdf":
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    if file_type == "docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Only PDF and DOCX files are supported")


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
