# import uvicorn
from fastapi import FastAPI
from .router import MainRouter
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .startup import lifespan
from pydantic import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"  # "/openapi.json" by default. It's nulled for safety.


settings = Settings()
app = FastAPI(title="IT Tutorials", lifespan=lifespan, openapi_url=settings.openapi_url)

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])  # "example.com", "*.example.com"
app.add_middleware(GZipMiddleware)
MainRouter(app=app)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80, reload=True, root_path="")
