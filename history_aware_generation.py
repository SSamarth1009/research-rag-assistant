from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)

# ============================================================
# STEP 1: Load environment variables
# ============================================================
load_dotenv()


# ============================================================
# STEP 2: Connect to existing Chroma vector database
# ============================================================

persist_directory = "db/chroma_db"

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)


# ============================================================
# STEP 3: Create LLM
# ============================================================

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

# Stores the conversation history
chat_history = []


# ============================================================
# STEP 4: Main RAG Function
# ============================================================

def answer_question(user_question):
    """
    Handles:
    1. Query rewriting
    2. Retrieval
    3. Answer generation
    4. Chat history updates
    """

    # ========================================================
    # STEP 4A: Rewrite follow-up questions
    # ========================================================
    # Example:
    #
    # User: Tell me about Microsoft
    # User: When was it founded?
    #
    # Rewritten:
    # "When was Microsoft founded?"
    #
    # This improves retrieval quality.
    # ========================================================

    if chat_history:

        rewrite_messages = [
            SystemMessage(
                content="""
                Given the chat history and the new question,
                rewrite the question so it is:

                - standalone
                - complete
                - searchable

                Only return the rewritten question.
                Do not answer it.
                """
            )
        ] + chat_history + [
            HumanMessage(
                content=f"New Question: {user_question}"
            )
        ]

        rewrite_result = model.invoke(rewrite_messages)

        search_question = rewrite_result.content.strip()

        print("\nRewritten Search Query:")
        print(search_question)

    else:
        search_question = user_question

    # ========================================================
    # STEP 4B: Retrieve relevant chunks
    # ========================================================

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(search_question)

    print(f"\nRetrieved {len(docs)} document(s)")

    # Show retrieved context
    for i, doc in enumerate(docs, start=1):

        print(f"\n----- Document {i} -----")

        print(
            f"Source: "
            f"{doc.metadata.get('source', 'Unknown')}"
        )

        print(
            f"Preview: "
            f"{doc.page_content[:200]}..."
        )

    # ========================================================
    # STEP 4C: Build context for the LLM
    # ========================================================
    # We include source information so the model can
    # mention where the answer came from.
    # ========================================================

    retrieved_context = "\n\n".join(

        [
            f"""
Source: {doc.metadata.get('source', 'Unknown')}

Content:
{doc.page_content}
"""
            for doc in docs
        ]
    )

    # ========================================================
    # STEP 4D: Build final prompt
    # ========================================================

    combined_input = f"""
Question:
{user_question}

Retrieved Documents:

{retrieved_context}

Instructions:

- Answer ONLY using the retrieved documents.
- If the answer is not contained in the documents,
  say:

  "I don't have enough information in the retrieved documents."

- Do not make up facts.
- Be concise and helpful.
"""

    # ========================================================
    # STEP 4E: Generate answer
    # ========================================================

    answer_messages = [
        SystemMessage(
            content="""
            You are a helpful assistant.

            Answer questions ONLY using the
            provided retrieved documents.

            Never invent information.
            """
        )
    ] + chat_history + [
        HumanMessage(content=combined_input)
    ]

    result = model.invoke(answer_messages)

    answer = result.content

    # ========================================================
    # STEP 4F: Save conversation history
    # ========================================================
    # This allows future follow-up questions
    # to be rewritten correctly.
    # ========================================================

    chat_history.append(
        HumanMessage(content=user_question)
    )

    chat_history.append(
        AIMessage(content=answer)
    )

    print("\n===== ANSWER =====")
    print(answer)

    return answer


# ============================================================
# STEP 5: Chat Loop
# ============================================================

def chat():
    """
    Interactive command-line chatbot.
    """

    print("\nResearch Assistant Ready!")
    print("Type 'quit' to exit.\n")

    while True:

        question = input("Your Question: ")

        if question.lower() == "quit":
            print("Goodbye!")
            break

        answer_question(question)


# ============================================================
# STEP 6: Application Entry Point
# ============================================================

if __name__ == "__main__":
    chat()