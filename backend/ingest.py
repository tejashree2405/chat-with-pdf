import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from services.embedding_service import get_embedding_model


def ingest_pdf(pdf_path):

    print("Loading PDF...")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    pdf_name = os.path.basename(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["source"] = pdf_name

    embeddings = get_embedding_model()

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    vectorstore.add_documents(chunks)

    print(f"Added {pdf_name} successfully")

if __name__ == "__main__":
    ingest_pdf("data/uploads/Dictionaries.pdf")