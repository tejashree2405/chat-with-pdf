import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/documents")
def get_documents():

    upload_folder = "data/uploads"

    if not os.path.exists(upload_folder):
        return {
            "documents": []
        }

    documents = [
        file
        for file in os.listdir(upload_folder)
        if file.endswith(".pdf")
    ]

    return {
        "documents": documents
    }