import os
import shutil

from fastapi import APIRouter

from langchain_community.vectorstores import Chroma
from services.embedding_service import get_embedding_model

router = APIRouter()


@router.post("/reset")
def reset_database():

    try:

        # Clear Chroma collection
        embeddings = get_embedding_model()

        db = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )

        try:
            db.delete_collection()
        except Exception:
            pass

        # Delete uploaded PDFs
        upload_folder = "data/uploads"

        if os.path.exists(upload_folder):

            for file in os.listdir(upload_folder):

                file_path = os.path.join(
                    upload_folder,
                    file
                )

                if os.path.isfile(file_path):
                    os.remove(file_path)

        return {
            "message": "Knowledge base reset successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }