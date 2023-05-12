import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app


# class Setup:
client = TestClient(app=app, base_url="https://localhost")


def clean_schema(response: dict):
    return {key:value for key, value in response.items() if value is not None}


# @pytest.fixture(scope="function")
# async def get_client():
#     async with AsyncClient(app=app, base_url="https://localhost") as client:
#         return client
