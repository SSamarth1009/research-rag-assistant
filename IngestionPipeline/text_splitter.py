import uuid
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from IngestionPipeline.extract import extract_document

paragraph_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200
)

# ---------------------------------------------------------
# Split Extracted Documents
# ---------------------------------------------------------

def build_chunks(document):
    """
    Split the extracted document into chunks and return a list of Document objects.
    """
    metadata = document["metadata"]
    document_name = metadata["document_name"]
    file_type = metadata["file_type"]
    documents = []
    for page in document["pages"]:
        page_number = page["page_number"]
        for block in page["text_blocks"]:
            text = block["content"]
            chunks = paragraph_splitter.split_text(text)
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "id": str(uuid.uuid4()),
                            "source": document_name,
                            "file_type": file_type,
                            "page_number": page_number,
                            "block_id": block["id"],
                            "block_type": block["type"],
                        }
                    )
                )

    return documents


if __name__ == "__main__":
    data = extract_document("../docs/sample.pdf")
    docs = build_chunks(data)

    print(f"Total chunks: {len(docs)}")
    print("\nFirst Chunk:\n")
    print(docs[0].page_content[:500])
    print("\nMetadata:\n")
    print(docs[0].metadata)