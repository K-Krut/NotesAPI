from fastapi import FastAPI

from app.routes import notes, auth

app = FastAPI(title="Notes API")


app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}

