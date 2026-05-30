from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

# Connect docuemnt to db
persist_directory = "db/chroma_db"
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)


# Set up AI model
chat_history = []
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

def ask_question(user_question):

    # Step 1: Make the question clear using conversation history
    if chat_history:
        # Ask the AI to make standalone question
        messages = [
            SystemMessage(content="Given the chat history, reqrite the new question to be standalone and searchable. Just rewrite the question, do not answer it."),
        ] + chat_history + [
            HumanMessage(content = f"New Question: {user_question}")
        ]

        result = model.invoke(messages)
        search_question = result.content.strip()
        print(f"Rewritten question for search: {search_question}")
    else:
        search_question = user_question

    # Step 2: Retrieve relevant documents using the rewritten question
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs= retriever.invoke(search_question)

    print(f"Retrieved {len(docs)} documents for the question.")
    for i, doc in enumerate(docs, 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc.metadata['source']}")
        print(f"Content preview: {doc.page_content[:200]}...")

    # Step 3: Answer the question using the retrieved documents and conversation history
    combined_input = f""" Based on the following retrieved documents, answer the question: {user_question}
    documents:
    {"\n".join([f"- {doc.page_content}" for doc in docs])}
    
    Please provide a clear, helpful answer using only the information fom these docuemnts.
    """

    # Step 4: Get the answer
    messages = [
        SystemMessage(content="You are a helpful assistant that answers questions based on the provided documents. Use only the information from the documents to answer the question."),
    ] + chat_history + [
        HumanMessage(content = combined_input)
    ]

    result = model.invoke(messages)
    answer = result.content

    # Step 5: Get the answer from the model
    chat_history.append(HumanMessage(content=user_question))
    chat_history.append(AIMessage(content=answer))

    print(f"Answer: {answer}")
    return answer



def ask_question(user_question):
    print(f"Ask me questions :) , Press quit to exit!")

    while True:
        question = input("Your question: ")

        if question.lower() == "quit":
            print("Exiting...")
            break

        ask_question(question)

if __name__ == "__main__":
    ask_question()