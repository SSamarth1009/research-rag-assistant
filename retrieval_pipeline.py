# from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv

# load_dotenv()

# persistent_directory = "db/chroma_db"

# # load embeddings and vectory store
# embedding_model = OpenAIEmbeddings(model= "text-embedding-3-small")

# vectorstore = Chroma(
#         persistent_directory = persistent_directory,
#         embedding_function=embedding_model,
#         collection_metadata = {"hnsw:space": "cosine"}
#     )

# # Search for relevant documents
# query = "When was spaceX founded? Who were the founding members?"

# retriever = db.as_retreiver(search_kwargs={"k":3})

# # retriever = db.as_retreiver(
# #     search_type ="similarity_score_threshold",
# #     search_kwargs ={
# #         "k" = 5,
# #         "score_threshold": 0.3 # Only return chunks cosine similarity >=0.3
# #     }
# # )

# relevant_docs = retriever.invoke(query)

# print(f"User query: {query}")

# # Display results
# print(f"----- Context -----")
# for i, doc in enumerate(relevant_docs,1):
#     print(f"Document {i}: \n{doc.page_content}\n")






from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

persist_directory = "db/chroma_db"

# Load embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Load existing Chroma vector store
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)

# User query
query = "When did microsoft acquire github?"

# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# Retrieve relevant documents``
relevant_docs = retriever.invoke(query)

print(f"\nUser Query: {query}")

# Display retrieved results
print("\n----- Retrieved Context -----\n")

for i, doc in enumerate(relevant_docs, 1):

    print(f"Document {i}")
    print("-" * 50)

    print(doc.page_content[:500])

    print("\nMetadata:")
    print(doc.metadata)

    print("\n")