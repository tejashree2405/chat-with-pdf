import os
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_FOLDER = "data/uploads"


def get_uploaded_documents():

    if not os.path.exists(
        UPLOAD_FOLDER
    ):
        return []

    return [
        file
        for file in os.listdir(
            UPLOAD_FOLDER
        )
        if file.endswith(".pdf")
    ]


def clear_uploaded_documents():

    if not os.path.exists(
        UPLOAD_FOLDER
    ):
        return

    for file in os.listdir(
        UPLOAD_FOLDER
    ):

        path = os.path.join(
            UPLOAD_FOLDER,
            file
        )

        os.remove(path)


def load_all_documents():

    documents = {}

    if not os.path.exists(
        UPLOAD_FOLDER
    ):
        return documents

    for filename in os.listdir(
        UPLOAD_FOLDER
    ):

        if filename.endswith(".pdf"):

            path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            loader = PyPDFLoader(path)

            pages = loader.load()

            text = "\n".join(
                page.page_content
                for page in pages
            )

            documents[filename] = text

    return documents