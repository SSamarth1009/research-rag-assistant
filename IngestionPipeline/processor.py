import os
from IngestionPipeline.extract import extract_document
from IngestionPipeline.text_splitter import split_text

DOCUMENT_FOLDER = "docs"


def process_documents():
    """
    Process all supported documents and return
    LangChain Document chunks.
    """
    all_chunks = []

    supported_extensions = (".pdf",".docx", ".txt",)

    for file_name in os.listdir(DOCUMENT_FOLDER):
        if not file_name.lower().endswith(supported_extensions):
            continue

        file_path = os.path.join(DOCUMENT_FOLDER,file_name)
        
        print(f"Processing: {file_name}")

        extracted_data = extract_document(file_path)
        chunks = split_text(extracted_data)
        all_chunks.extend(chunks)

        print(f"Chunks Created: {len(chunks)}\n")

    print("=" * 60)
    print(f"Total Chunks Created: {len(all_chunks)}")

    return all_chunks


if __name__ == "__main__":

    documents = process_documents()

    print("\nFirst Chunk\n")
    print(documents[0].page_content[:300])

    print("\nMetadata\n")
    print(documents[0].metadata)