import streamlit as st
import os

from services.ingest import ingest_pdf
from services.rag_service import ask_question
from services.vectorstore_service import clear_vectorstore
from services.document_service import (
    get_uploaded_documents,
    clear_uploaded_documents
)

st.set_page_config(
    page_title="Chat With PDF",
    page_icon="📄",
    layout="wide"
)

st.title("~ Chat With PDF ~")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:

    st.header("Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Reset Knowledge Base"):

        clear_vectorstore()

        clear_uploaded_documents()

        st.session_state.messages = []

        st.success(
            "Knowledge base reset."
        )

    if uploaded_files:

        if st.button("Upload Documents"):

            for file in uploaded_files:

                os.makedirs(
                    "data/uploads",
                    exist_ok=True
                )

                for file in uploaded_files:

                    path = os.path.join(
                        "data/uploads",
                        file.name
                    )

                    with open(
                        path,
                        "wb"
                    ) as f:

                        f.write(
                            file.getvalue()
                        )

                    ingest_pdf(path)

            st.success("Documents uploaded successfully")
    
    st.divider()

    st.subheader("Loaded Documents")

    try:

        documents = get_uploaded_documents()

        if documents:

            for doc in documents:
                st.write(f"✓ {doc}")

        else:
            st.info("No documents loaded")

    except:

        st.error("Backend unavailable")

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

question = st.chat_input(
    "Ask a question about your PDFs"
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    result = ask_question(
        question,
        st.session_state.messages
    )

    answer = result["answer"]

    sources = result["sources"]
    
    retrieved_chunks = result.get(
        "retrieved_chunks",
        []
    )

    source_text = ""

    if sources:

        source_text = "\n\n### Sources\n"

        for source in sources:

            source_text += (
                f"- {source['pdf']} "
                f"(Page {source['page']})\n"
            )

    final_response = answer + source_text

    with st.chat_message("assistant"):
        st.markdown(final_response)

    if retrieved_chunks:

        with st.expander(
            "🔍 View Retrieved Context"
        ):

            for i, chunk in enumerate(
                retrieved_chunks,
                start=1
            ):

                st.markdown(
                    f"### Chunk {i}"
                )

                st.markdown(
                    f"**Source:** "
                    f"{chunk['pdf']} "
                    f"(Page {chunk['page']})"
                )

                st.code(
                    chunk["content"][:1000]
                )

                st.divider()
                
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_response
        }
    )