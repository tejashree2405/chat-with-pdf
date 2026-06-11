from fastapi import FastAPI

from routes.upload import router as upload_router
from routes.chat import router as chat_router
from routes.reset import router as reset_router
from routes.documents import router as documents_router

app = FastAPI(
    title="Chat With PDF API"
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(reset_router)
app.include_router(documents_router)

@app.get("/")
def root():

    return {
        "message": "Backend Running"
    }