from langchain_community.vectorstores import Chroma
from services.embedding_service import get_embedding_model


CHROMA_DB_PATH = "chroma_db"


def get_vectorstore():
    """
    Load the existing Chroma database.
    """

    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )


def retrieve_documents(question, k=4):
    """
    Retrieve the most relevant documents for a question.
    Returns documents along with similarity scores.
    """

    db = get_vectorstore()

    results = db.similarity_search_with_score(
        question,
        k=k
    )

    return results


def retrieve_context(question, k=4):
    """
    Returns only the documents without scores.
    Useful when building context for the LLM.
    """

    results = retrieve_documents(question, k)

    docs = [doc for doc, score in results]

    return docs

def clear_vectorstore():

    db = get_vectorstore()

    try:

        db.delete_collection()

    except:

        pass