import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
#print(os.getenv("OPENAI_API_KEY"))


def load_documents(docs_path = "docs"):
    '''Load all text files from docs directory'''
    print(f"Loading documents from {docs_path}...")

    #check if docs directory exists or not
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"the directory {docs_path} does not exist.")
    
    #load all .txt files from the docs directory
    loader = DirectoryLoader(
        path = docs_path,
        glob = "*.txt",
        loader_cls = TextLoader
    )

    documents = loader.load()

    if len(documents)==0:
        raise FileNotFoundError(f"No text file found in {docs_path}.")
    

    # for i, doc in enumerate(documents):
    #     print(f"\nDocument {i+1}:")
    #     print(f"   Source: {doc.metadata['source']}")
    #     print(f"   Content length: {len(doc.page_content)} characters")
    #     print(f"   Content preview: {doc.page_content[:100]}...")
    #     print(f"   metadata: {doc.metadata}")

    return documents

def split_documents(documents, chunk_size=800, chunk_overlap=0):
    '''split documents into smaller chunks with overlap'''
    print("Splitting documents into chunks")

    text_splitter = CharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap= chunk_overlap
    )

    chunks = text_splitter.split_documents(documents)

    # if chunks:
    #     for i, chunk in enumerate(chunks[:5]):
    #         print(f"\n---Chunk {i+1} ---")
    #         print(f"   Source: {chunk.metadata['source']}")
    #         print(f"   Content length: {len(chunk.page_content)} characters")
    #         print(f"   Content:")
    #         print(chunk.page_content)
    #         print("-" * 50)

    #     if len(chunks) > 5:
    #         print(f"\n... and {len(chunks) - 5} more chunks")

    return chunks

def create_vector_store(chunks, persist_directory = "db/chroma_db"):
    '''Create and persist ChromaDB vector store'''
    print("Creating embeddings and storing in ChromaDB...")

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create chromaDB vector store
    print("-------- Creating vector  store --------")

    vectorstore = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_model,
        persist_directory = persist_directory,
        collection_metadata = {"hnsw:space": "cosine"}
    )

    print("-------- Finished creating vector store --------")

    print(f"vector store created and saved to {persist_directory}")
    return vectorstore

# def inspect_vector_store(vectorstore):

#     print("\nInspecting vector store...\n")

#     data = vectorstore.get(
#     include=["documents", "metadatas", "embeddings"]
#     )

#     print(f"Total stored chunks: {len(data['documents'])}")

#     # Show first document
#     print("\nFirst Stored Chunk:")
#     print(data['documents'][0])

#     # Show metadata
#     print("\nMetadata:")
#     print(data['metadatas'][0])

#     # Show embedding size
#     print("\nEmbedding Dimension:")
#     print(len(data['embeddings'][0]))

#     # Show first 10 embedding values
#     print("\nFirst 10 embedding values:")
#     print(data['embeddings'][0][:10])


def main():
    print("Main func")

if __name__ == "__main__":
    main()
    documents = load_documents() # 1) Loading the files
    chunks = split_documents(documents) # 2) Chunking the files
    vectorstore = create_vector_store(chunks) # 3) store in vectorDB
    # inspect_vector_store(vectorstore)