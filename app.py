import streamlit as st
import os
from retrieval_pipeline import generate_answer

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="Research Paper RAG",
    layout="wide"
)


# ------------------------
# Title
# ------------------------
st.title("📚 Research Paper RAG Assistant")


# ------------------------
# Sidebar - Sources
# ------------------------
st.sidebar.title("Sources")
sources = os.listdir("docs")

for source in sources:
    st.sidebar.write(
        "📄",
        source
    )


for source in sources:
    st.sidebar.write(
        "📄",
        source
    )

# ------------------------
# User Query
# ------------------------
query = st.text_input(
    "Ask a question about your documents"
)



if st.button("Search"):
    if query:
        with st.spinner(
            "Searching documents..."
        ):
            result = generate_answer(query)


        # Answer
        st.subheader("Answer")
        st.write(result["answer"])

        # Sources
        st.subheader("Sources")

        for doc in result["sources"]:
            st.write( "📄",doc.metadata["source"])