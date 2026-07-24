import os
import fitz
import pdfplumber
from docx import Document

def create_document(document_name: str, file_type: str):
    return {
        "metadata": {
            "document_name": document_name,
            "file_type": file_type,
            "page_count": 0,
        },
        "pages": []
    }

def create_page(page_number: int, text: str = ""):
    """
    Create a standardized page representation.
    """
    page = {
        "page_number": page_number,
        "text_blocks": [],
        "tables": [],
        "figures": [],
        "charts": [],
        "metadata": {}
    }
    if text:
        page["text_blocks"].append({
            "id": 0,
            "type": "paragraph",
            "content": text
        })

    return page

def extract_pdf_tables(page):
    """
    Extract tables from a pdfplumber page while preserving structure.
    """
    tables = []

    extracted_tables = page.extract_tables()

    for table_id, table in enumerate(extracted_tables):
        tables.append({
            "id": table_id,
            "rows": table
        })

    return tables

def extract_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    pdf = fitz.open(pdf_path)
    plumber_pdf = pdfplumber.open(pdf_path)
    document = create_document(os.path.basename(pdf_path),"pdf")

    for page_number, (fitz_page, plumber_page) in enumerate(zip(pdf, plumber_pdf.pages),start=1):
        text = fitz_page.get_text().strip()
        tables = extract_pdf_tables(plumber_page)
        page_data = create_page(page_number, text)
        page_data["tables"] = tables
        document["pages"].append(page_data)
        document["metadata"]["page_count"] = pdf.page_count

    pdf.close()
    plumber_pdf.close()

    return document


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

    document = create_document(os.path.basename(docx_path),"docx")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


def extract_txt(txt_path):
    """
    Extract text from a TXT file.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    document = create_document(os.path.basename(txt_path),"txt")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


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

if __name__ == "__main__":
    docs_folder = "../docs"

    for file in os.listdir(docs_folder):
        file_path = os.path.join(docs_folder, file)
        data = extract_document(file_path)

        print("\n" + "=" * 60)
        print(f"Document : {data['metadata']['document_name']}")
        print(f"Type     : {data['metadata']['file_type']}")
        print(f"Pages    : {data['metadata']['page_count']}")

        if data["pages"]:
            first_page = data["pages"][0]
            print(f"\nPage {first_page['page_number']}")
            if first_page["text_blocks"]:
                print(first_page["text_blocks"][0]["content"][:300])
            else:
                print("<No text found on this page>")
    import os
import fitz
import pdfplumber
from docx import Document

def create_document(document_name: str, file_type: str):
    return {
        "metadata": {
            "document_name": document_name,
            "file_type": file_type,
            "page_count": 0,
        },
        "pages": []
    }

def create_page(page_number: int, text: str = ""):
    """
    Create a standardized page representation.
    """
    page = {
        "page_number": page_number,
        "text_blocks": [],
        "tables": [],
        "figures": [],
        "charts": [],
        "metadata": {}
    }
    if text:
        page["text_blocks"].append({
            "id": 0,
            "type": "paragraph",
            "content": text
        })

    return page

def extract_pdf_tables(page):
    """
    Extract tables from a pdfplumber page while preserving structure.
    """
    tables = []

    extracted_tables = page.extract_tables()

    for table_id, table in enumerate(extracted_tables):
        tables.append({
            "id": table_id,
            "rows": table
        })

    return tables

def extract_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    pdf = fitz.open(pdf_path)
    plumber_pdf = pdfplumber.open(pdf_path)
    document = create_document(os.path.basename(pdf_path),"pdf")

    for page_number, (fitz_page, plumber_page) in enumerate(zip(pdf, plumber_pdf.pages),start=1):
        text = fitz_page.get_text().strip()
        tables = extract_pdf_tables(plumber_page)
        page_data = create_page(page_number, text)
        page_data["tables"] = tables
        document["pages"].append(page_data)
        document["metadata"]["page_count"] = pdf.page_count

    pdf.close()
    plumber_pdf.close()

    return document


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

    document = create_document(os.path.basename(docx_path),"docx")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


def extract_txt(txt_path):
    """
    Extract text from a TXT file.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    document = create_document(os.path.basename(txt_path),"txt")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


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

if __name__ == "__main__":
    docs_folder = "../docs"

    for page in data["pages"]:
        if page["tables"]:
            print(f"\nTables found on page {page['page_number']}")
            print(page["tables"])

    for file in os.listdir(docs_folder):
        file_path = os.path.join(docs_folder, file)
        data = extract_document(file_path)

        print("\n" + "=" * 60)
        print(f"Document : {data['metadata']['document_name']}")
        print(f"Type     : {data['metadata']['file_type']}")
        print(f"Pages    : {data['metadata']['page_count']}")

        if data["pages"]:
            first_page = data["pages"][0]
            print(f"\nPage {first_page['page_number']}")
            if first_page["text_blocks"]:
                print(first_page["text_blocks"][0]["content"][:300])
            else:
                print("<No text found on this page>")
    # ------------------------------
    # Print extracted tables
    # ------------------------------
    for page in data["pages"]:
        if page["tables"]:
            print(f"\nTables found on page {page['page_number']}")
            print(page["tables"])