import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from services.vectorstore_service import retrieve_documents

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def ask_question(question):

    results = retrieve_documents(question)

    docs = [doc for doc, score in results]

    context = "\n\n".join(
        [doc.page_content for doc in docs]
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

Use ONLY the provided context.

If the answer is not present in the context, say:

"I could not find that information in the uploaded documents."

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