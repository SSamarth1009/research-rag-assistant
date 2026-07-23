from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def create_vector_store(
    chunks,
    persist_directory="db/chroma_db"
):

    print("Creating embeddings...")

    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={
            "hnsw:space": "cosine"
        }
    )

    print("Vector store created.")

    return vectorstore