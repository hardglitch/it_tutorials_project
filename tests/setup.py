from fastapi.testclient import TestClient
from app.main import app


class Setup:
    client = TestClient(app, base_url="http://localhost")
