import uuid
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from IngestionPipeline.extract import extract_document

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 200)

# ---------------------------------------------------------
# Split Extracted Documents
# ---------------------------------------------------------

def split_text(data):
    """
    Split extracted document content into LangChain Documents.
    """
    document_name = data["document_name"]
    title = data.get("title")
    authors = data.get("authors")
    file_type = data["file_type"]

    documents = []

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if file_type == "pdf":
        pages = data["pages"]

        for page_number, page_content in pages.items():
            chunks = text_splitter.split_text(page_content)
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "id": str(uuid.uuid4()),
                            "source": document_name,
                            "title": title,
                            "authors": authors,
                            "page_number": page_number,
                            "file_type": file_type
                        }
                    )
                )

    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    elif file_type == "docx":
        chunks = text_splitter.split_text(data["content"])

        for chunks in chunks:
            documents.append(
                Document(
                    page_content = chunks,
                    metadata ={
                        "id": str(uuid.uuid4()),
                        "source": document_name,
                        "title": title,
                        "authors": authors,
                        "file_type": file_type
                    }
                )
            )

    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------

    elif file_type == "txt":

        chunks = text_splitter.split_text(
            data["content"]
        )

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "id": str(uuid.uuid4()),
                        "source": document_name,
                        "title": title,
                        "authors": authors,
                        "file_type": file_type
                    }
                )
            )

    else:
        raise ValueError(
            f"Unsupported file type: {file_type}"
        )

    return documents

if __name__ == "__main__":
    data = extract_document("../docs/sample.pdf")
    docs = split_text(data)

    print(f"Total chunks: {len(docs)}")
    print("\nFirst Chunk:\n")
    print(docs[0].page_content[:500])
    print("\nMetadata:\n")
    print(docs[0].metadata)