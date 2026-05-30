from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

load_dotenv()

#print(os.getenv("OPENAI_API_KEY"))

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
query = "Tell me about Jensen Huang's background and career achievements."

# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# Retrieve relevant documents
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

combined_input = f""" Based on the following retrieved documents, answer the question: {query}

Documents:
{chr(10).join([doc.page_content for doc in relevant_docs])} #
combines multiple documents into a single string with newline separation because, gpt expects a single string input.

Please provide a clear and concise answer based on the information from the retrieved documents. If the documents do not contain enough information to answer the question, say I don't have enough information to answer the question.
"""

model = ChatOpenAI(model="gpt-4o", temperature=0)

messages = [
    SystemMessage(content="You are a helpful assistant that answers questions based on the provided retrieved documents."),
    HumanMessage(content=combined_input),
]

# Invoke the model with compbined input
result = model.invoke(messages)

# Display the full result and content only
print("\n----- Final Answer -----\n")
print("Content only:")
print(result.content)