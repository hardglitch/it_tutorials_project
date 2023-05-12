import pytest
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr, SecretStr
from starlette import status
from app.common.constants import DecodedCredential
from app.user.schemas import UserSchema
from conftest import clean_schema, client


class TestUser:

    test_user_id = 0

    def test_user_registration_positive(self):
        new_user = UserSchema(
            name="Test_Paul",
            email=EmailStr("test-paul@email.com"),
            password=SecretStr("0987654321"),
        )
        response = client.post("/user/reg", data=jsonable_encoder(new_user))
        assert response.status_code == status.HTTP_200_OK or \
               response.status_code == status.HTTP_304_NOT_MODIFIED
               # if this user already exists after some other test,
               # so that this exception doesn't break the test

        user_data = UserSchema(
            name="Test_Paul",
            decoded_credential=DecodedCredential.user,
            rating=0,
        )

        if response.status_code == status.HTTP_200_OK:
            self.test_user_id = user_data.id = response.json()["id"]
            assert response.json() == clean_schema(jsonable_encoder(user_data))

    def test_duplicate_user_negative(self):
        new_user = jsonable_encoder(
            UserSchema(
                name="Test_Paul",
                email=EmailStr("test-paul@email.com"),
                password=SecretStr("0987654321"),
            )
        )

        response = client.post("/user/reg", data=new_user)
        assert response.status_code == status.HTTP_304_NOT_MODIFIED

    # def test_get_user_positive(self, get_client):
    #     user_data = jsonable_encoder(
    #         UserSchema(
    #             id=self.test_user_id,
    #             name="Test_Paul",
    #             decoded_credential=DecodedCredential.user,
    #             rating=0,
    #         )
    #     )
    #
    #     client = get_client
    #     response = client.get(f"/user/{self.test_user_id}")
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == Setup.clean_schema(user_data)

