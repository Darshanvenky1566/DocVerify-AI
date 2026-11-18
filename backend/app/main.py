from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.applications import router as applications_router
from app.auth import router as auth_router
from app.documents import router as documents_router
from app.reviews import router as reviews_router
app = FastAPI(title="DocVerify AI API", version="0.1.0")

app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(documents_router)

app.include_router(reviews_router)
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "DocVerify AI"}


@app.get("/", include_in_schema=False)
def open_docs():
    return RedirectResponse(url="/docs")