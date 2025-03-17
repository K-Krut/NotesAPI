from fastapi import FastAPI

from routes import notes

app = FastAPI(title="Notes API")
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

