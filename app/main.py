# import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
# from starlette.staticfiles import StaticFiles
from .router import MainRouter
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .startup import lifespan


app = FastAPI(title="IT Tutorials", lifespan=lifespan)
templates_dir = Path(__name__.split(".")[0]).joinpath("templates")
templates = Jinja2Templates(directory=templates_dir)
# app.mount("/static", StaticFiles(directory=Path(__name__.split(".")[0]).joinpath("static")), name="static")

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])  # "example.com", "*.example.com"
app.add_middleware(GZipMiddleware)
MainRouter(app=app, templates=templates)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80, reload=True, root_path="")
