# Connect to ChromaDB
# Retrieve relevant documents

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, TOP_K

def load_vector_store():
    """
    Load the existing Chroma vector database.
    """
    embedding_model = OpenAIEmbeddings( model=EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=CHROMA_PERSIST_DIR,embedding_function=embedding_model)

    return vector_store


def retrieve_documents(query: str, k: int = TOP_K):
    """
    Retrieve the most relevant chunks for a user query.
    """
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": k,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)
    documents = retriever.invoke(query)

    return documents

if __name__ == "__main__":
    query = "Tell me about Jensen Huang"
    documents = retrieve_documents(query)
    print(f"\nRetrieved {len(documents)} documents\n")
    for i, doc in enumerate(documents, start=1):
        print("=" * 80)
        print(f"Document {i}")

        print(f"Source : {doc.metadata.get('source')}")
        print(f"Title  : {doc.metadata.get('title')}")
        print(f"Page   : {doc.metadata.get('page_number')}")
        print(f"Type   : {doc.metadata.get('file_type')}")

        print("\nContent:")
        print(doc.page_content[:350])
        print()