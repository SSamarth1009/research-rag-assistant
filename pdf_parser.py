# pdf_parser.py
import fitz                             # PyMuPDF
from pathlib import Path

def parse_pdf(file_path: str) -> list[dict]:
    """
    Extract text page-by-page from a PDF.
    Returns a list of page dicts, one per page.

    WHY page-by-page instead of full doc:
    Every chunk needs to know its page number.
    That's what makes citations possible — "Page 4" 
    is stored in metadata here, not guessed later.
    """
    doc = fitz.open(file_path)
    source_filename = Path(file_path).name

    # Pull title + authors from first page heuristically
    first_page_lines = [
        l.strip() for l in doc[0].get_text().split("\n") if l.strip()
    ]
    title = first_page_lines[0] if first_page_lines else "Unknown Title"
    authors = first_page_lines[1] if len(first_page_lines) > 1 else "Unknown Authors"

    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if not text.strip():            # skip blank/image-only pages
            continue

        pages.append({
            "text": text,
            "metadata": {
                "source_file": source_filename,
                "title": title,
                "authors": authors,
                "page_number": page_num,
            }
        })

    doc.close()
    print(f"  Parsed '{source_filename}': {len(pages)} pages")
    return pages


def parse_all_pdfs(docs_path: str = "docs") -> list[dict]:
    """
    Parse every PDF in the docs/ folder.
    This replaces load_documents() from 1_ingestion_pipeline.py.
    """
    pdf_files = list(Path(docs_path).glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in '{docs_path}/'")

    all_pages = []
    for pdf_file in pdf_files:
        pages = parse_pdf(str(pdf_file))
        all_pages.extend(pages)

    print(f"\nTotal pages parsed: {len(all_pages)}")
    return all_pages