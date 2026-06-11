import os

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from ingest import ingest_pdf

router = APIRouter()

UPLOAD_FOLDER = "data/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    ingest_pdf(file_path)

    return {
        "message": f"{file.filename} indexed successfully"
    }