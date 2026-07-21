from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

load_dotenv()

#print(os.getenv("OPENAI_API_KEY"))

persist_directory = "db/chroma_db"

def load_vector_store():

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(persist_directory=persist_directory,embedding_function=embedding_model)
    
    return vectorstore

def retrieve_documents(query, k=3):
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": k
        }
    )
    relevant_docs = retriever.invoke(query)

    return relevant_docs

def generate_answer(query):
    # Step 1:Retrieve relevant documents
    relevant_docs = retrieve_documents(query)


    # Step 2: Convert documents into context
    context = "\n\n".join(
        [
            doc.page_content
            for doc in relevant_docs
        ]
    )


    # Step 3:Create prompt
    combined_input = f"""
Answer the question using only the following documents.

Question:
{query}


Documents:

{context}


Instructions:

- Answer only from the provided documents.
- If the answer is not present, say:
"I don't have enough information to answer this question."
- Do not make up information.
"""


    # Step 4:Initialize LLM
    model = ChatOpenAI(model="gpt-4o",temperature=0)

    # Step 5:Send prompt
    messages = [
        SystemMessage(
            content=
            """
            You are a helpful assistant.Answer questions using retrieved documents only.
            """
        ),HumanMessage(content=combined_input)]
    
    response = model.invoke(messages)

    # Step 6: Return answer
    return {
    "answer": response.content,
    "sources": relevant_docs
}

if __name__ == "__main__":
    query = "Tell me about Jensen"
    result = generate_answer(query)

    print("\n----- ANSWER -----\n")
    print(result["answer"])
    print("\n----- SOURCES -----\n")

    for doc in result["sources"]:
        print(doc.metadata["source"])