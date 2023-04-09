import uvicorn
from fastapi import FastAPI
from src.router import MainRouter

app = FastAPI(title="IT Tutorials")
MainRouter(app)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
