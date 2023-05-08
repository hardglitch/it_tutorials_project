# import uvicorn
from fastapi import FastAPI
from .router import MainRouter
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(title="IT Tutorials")

# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
# app.add_middleware(GZipMiddleware)
MainRouter(app)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80, reload=True, root_path="")
