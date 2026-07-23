from IngestionPipeline.processor import process_documents
from IngestionPipeline.vector_store import create_vector_store


def main():

    print("Starting ingestion...\n")

    chunks = process_documents()

    create_vector_store(chunks)

    print("\nFinished!")


if __name__ == "__main__":
    main()