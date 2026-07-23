from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import OPENAI_MODEL
from RetrievalPipeline.retriever import retrieve_documents

# ---------------------------------------------------------
# Generate Answer
# ---------------------------------------------------------

def generate_answer(query):
    """
    Retrieve documents and generate an answer.
    """

    # Step 1: Retrieve relevant documents
    documents = retrieve_documents(query)

    # Step 2: Build context
    context = "\n\n".join(
    f"""
    Source File: {doc.metadata.get('source')}
    Page Number: {doc.metadata.get('page_number', 'N/A')}

    Content:
    {doc.page_content}
    """
        for doc in documents
    )

    # Step 3: Create prompt
    prompt = f"""
You are an AI Research Assistant.

Answer the user's question ONLY using the provided context.

User Question:
{query}

Retrieved Context:
{context}

Instructions:

- Answer only from the provided context.
- Do not make up information.
- If the answer is not present, respond with:
  "I don't have enough information to answer this question."

- If possible, mention the source file and page number
  naturally in your answer.

- Keep the answer clear, concise, and factual.
"""

    # Step 4: Initialize LLM
    model = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0
    )

    # Step 5: Messages
    messages = [
        SystemMessage(
            content="""
You are a helpful AI Research Assistant.

Only answer using the supplied context.

Never hallucinate.

If the information is unavailable,
say that you don't have enough information.
"""
        ),
        HumanMessage(content=prompt)
    ]

    # Step 6: Generate response
    response = model.invoke(messages)

    # Step 7: Return answer + retrieved documents
    return {
        "answer": response.content,
        "sources": documents
    }


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    query = "Tell me about Jensen Huang"

    result = generate_answer(query)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for i, doc in enumerate(result["sources"], start=1):

        print(f"\nDocument {i}")

        print(f"Source : {doc.metadata.get('source')}")
        print(f"Title  : {doc.metadata.get('title')}")
        print(f"Page   : {doc.metadata.get('page_number')}")
        print(f"Type   : {doc.metadata.get('file_type')}")