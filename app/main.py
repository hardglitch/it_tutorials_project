# import uvicorn
from fastapi import FastAPI
from .router import MainRouter

# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


app = FastAPI(title="IT Tutorials")

# app.add_middleware(HTTPSRedirectMiddleware)   # for production
MainRouter(app)

# if __name__ == "__main__":
#     uvicorn.run(app, reload=True)
