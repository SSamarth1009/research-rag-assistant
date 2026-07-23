import os
import streamlit as st

from RetrievalPipeline.prompt_builder import generate_answer

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Research Paper RAG",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 Research Paper RAG Assistant")
st.caption("Ask questions about your uploaded research papers.")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Available Documents")

docs_folder = "docs"

if os.path.exists(docs_folder):

    documents = sorted(os.listdir(docs_folder))

    for document in documents:
        st.sidebar.write(f"📄 {document}")

else:
    st.sidebar.warning("No documents found.")

# --------------------------------------------------
# Query Input
# --------------------------------------------------

query = st.text_input(
    "Enter your question:"
)

# --------------------------------------------------
# Search Button
# --------------------------------------------------

if st.button("Search", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching..."):

        result = generate_answer(query)

    # -------------------------
    # Answer
    # -------------------------

    st.subheader("Answer")

    st.write(result["answer"])

    # -------------------------
    # Sources
    # -------------------------

    st.subheader("Retrieved Sources")

    unique_sources = []

    for doc in result["sources"]:

        source = doc.metadata.get("source")

        if source not in unique_sources:
            unique_sources.append(source)

    for source in unique_sources:
        st.write(f"📄 {source}")