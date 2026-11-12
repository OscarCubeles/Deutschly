from fastapi import FastAPI
from app.api import lessons

app = FastAPI(
    title="Deutschly",
    description="Deutschly is a language learning platform that helps users learn German through interactive exercises",
    version="0.1.0"
)


app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])

@app.get("/")
def root():
    return {"message": "Welcome to Deutschly!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
