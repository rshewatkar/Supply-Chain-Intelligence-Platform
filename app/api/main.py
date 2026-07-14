from fastapi import FastAPI

app = FastAPI(
    title="Supply Chain Intelligence Platform",
    version="0.1.0",
)

@app.get("/")
def health():
    return {
        "status": "running",
        "project": "Supply Chain Intelligence Platform",
    }