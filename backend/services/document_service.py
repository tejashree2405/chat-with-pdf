from langchain_community.document_loaders import PyPDFLoader
import os

UPLOAD_FOLDER = "data/uploads"


def load_all_documents():

    documents = {}

    for filename in os.listdir(UPLOAD_FOLDER):

        if filename.endswith(".pdf"):

            path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            loader = PyPDFLoader(path)

            pages = loader.load()

            text = "\n".join(
                page.page_content
                for page in pages[:3]
            )

            documents[filename] = text

    return documents