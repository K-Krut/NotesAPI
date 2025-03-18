from fastapi import FastAPI

from routes import auth, notes

app = FastAPI(title="Notes API")


app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
