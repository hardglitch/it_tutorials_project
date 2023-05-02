from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from starlette import status
from app.common.constants import Credential
from app.user.schemas import AddUserScheme, GetUserScheme
from setup import Setup


class TestUser(Setup):

    def test_user_registration_positive(self):
        new_user = jsonable_encoder(
            AddUserScheme(
                name="Paul",
                credential=Credential.user,
                email=EmailStr("paul@email.com"),
                password="0987654321",
            )
        )

        user_data = GetUserScheme(
            id=0,
            name="Paul",
            decoded_credential="user",
            rating=0
        )

        response = Setup.client.post("/user/reg", json=new_user)
        assert response.status_code == status.HTTP_200_OK
        user_data.id = response.json()["id"]
        assert response.json() == jsonable_encoder(user_data)

    def test_duplicate_user_negative(self):
        new_user = jsonable_encoder(
            AddUserScheme(
                name="Paul",
                credential=Credential.user,
                email=EmailStr("paul@email.com"),
                password="0987654321",
            )
        )

        response = Setup.client.post("/user/reg", json=new_user)
        assert response.status_code == status.HTTP_304_NOT_MODIFIED

