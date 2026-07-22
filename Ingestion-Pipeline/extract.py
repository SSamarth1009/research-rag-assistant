import os
import fitz
from docx import Document

def extract_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    pdf = fitz.open(pdf_path)
    pages = {}

    for page_number, page in pages in enumerate(pdf,start = 1):
        text = page.get_text().strip()
        if text: 
            pages[page_number] = text
    pdf.close()

    return {
        "document_name": os.path.basename(pdf_path),
        "file_type": "pdf",
        "pages": pages
    }


def extract_docx(docx_path):
    """
    Extract text from a DOCX file.
    """
    doc = Document(docx_path)

    content = "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )
    return {
        "document_name": os.path.basename(docx_path),
        "file_type": "docx",
        "content": content
    }


def extract_txt(txt_path):
    """
    Extract text from a TXT file.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "document_name": os.path.basename(txt_path),
        "file_type": "txt",
        "content": content
    }


def extract_document(file_path):
    """
    Detect file type and call the appropriate extractor.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)
    elif extension == ".docx":
        return extract_docx(file_path)
    elif extension == ".txt":
        return extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")