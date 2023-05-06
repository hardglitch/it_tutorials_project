import uvicorn
from fastapi import FastAPI
from app.router import MainRouter

app = FastAPI(title="IT Tutorials")
MainRouter(app)

if __name__ == "__main__":
    uvicorn.run(app, reload=True)
