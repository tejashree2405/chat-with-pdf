import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from services.document_service import load_all_documents
from services.vectorstore_service import retrieve_documents

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def ask_question(question):

    question_lower = question.lower()
    
    is_multi_doc_summary = any(
        phrase in question_lower
        for phrase in [
            "summarize all",
            "summarise all",
            "summarize both",
            "summarise both",
            "all files",
            "all documents",
            "all pdfs",
            "compare both",
            "compare all"
        ]
    )

    print("Multi-document summary:", is_multi_doc_summary)

    if is_multi_doc_summary:

        all_documents = load_all_documents()
        print("\n===== DOCUMENTS LOADED =====")

        for pdf_name, text in all_documents.items():

            print(f"\nPDF: {pdf_name}")
            print(f"Characters: {len(text)}")
            print(text[:300])

        print("\n============================\n")

        if not all_documents:
            return {
                "answer": "No documents uploaded.",
                "sources": []
            }

        context = ""

        for pdf_name, text in all_documents.items():

            context += f"\n\nPDF: {pdf_name}\n"

            context += text

        prompt = f"""
    You are analyzing multiple PDFs.

    The context is organized by PDF name.

    If asked to summarize:
    - Summarize EACH PDF separately.

    If asked to compare:
    - Compare ALL PDFs.
    - Mention similarities.
    - Mention differences.

    Context:
    {context}

    Question:
    {question}
    """

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": [
                {
                    "pdf": filename,
                    "page": "N/A"
                }
                for filename in all_documents.keys()
            ],
            "retrieved_chunks": 0
        }
    
    results = retrieve_documents(question, k=4)

    docs = [doc for doc, score in results]

    documents = {}

    for doc in docs:

        pdf_name = doc.metadata.get(
            "source",
            "Unknown"
        )

        if pdf_name not in documents:
            documents[pdf_name] = []

        documents[pdf_name].append(
            doc.page_content
        )

    context = ""

    for pdf_name, chunks in documents.items():

        context += f"\n\nPDF: {pdf_name}\n"

        context += "\n".join(
            chunks[:5]
        )

    sources = []

    for doc in docs:

        sources.append({
            "pdf": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "Unknown")
        })

    if not docs:
        return {
            "answer": "I could not find that information in the uploaded documents.",
            "sources": []
        }

    prompt = f"""
You are a helpful PDF assistant.

The context may contain information
from multiple PDFs.

If multiple PDFs are present:

- Identify each PDF separately.
- Summarize each PDF separately.
- Compare them when appropriate.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources,
        "retrieved_chunks": len(docs)
    }