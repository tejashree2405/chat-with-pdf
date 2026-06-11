from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Creates and returns the embedding model used
    throughout the application.
    """

    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)