from fastapi.encoders import jsonable_encoder
from starlette import status
from app.dictionary.schemas import DictionarySchema
from app.language.schemas import LanguageSchema
from app.tutorial.theme.schemas import ThemeSchema
from app.user.exceptions import AuthenticateExceptions, UserExceptions
from setup import Setup


class TestUrlsNegative:

    def test_wrong_url_negative(self):
        response = Setup.client.post("/lng/add", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = Setup.client.post("add", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_allowed_negative(self):
        response = Setup.client.post("/user/me", json={})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_not_found_negative(self):
        response = Setup.client.get("/user")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unprocessable_entity_negative(self):
        response = Setup.client.post("/lang/add", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestAddNewElementNegative:

    def test_add_language_negative(self):
        new_lang = jsonable_encoder(LanguageSchema(abbreviation="eng", lang_value="english", is_ui_lang=True))
        response = Setup.client.post("/lang/add", json=new_lang)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": AuthenticateExceptions.FAILED_TO_DECODE_TOKEN.detail}

    def test_add_dist_type_negative(self):
        new_dist_type = jsonable_encoder(DictionarySchema(lang_code=0, dict_value="free"))
        response = Setup.client.post("/tutorial/dist-type/add", json=new_dist_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": AuthenticateExceptions.FAILED_TO_DECODE_TOKEN.detail}

    def test_add_type_negative(self):
        new_type = jsonable_encoder(DictionarySchema(lang_code=0, dict_value="New Type"))
        response = Setup.client.post("/tutorial/type/add", json=new_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": AuthenticateExceptions.FAILED_TO_DECODE_TOKEN.detail}

    def test_add_theme_negative(self):
        new_theme = jsonable_encoder(ThemeSchema(lang_code=0, dict_value="Python", type_code=0))
        response = Setup.client.post("/tutorial/theme/add", json=new_theme)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": AuthenticateExceptions.FAILED_TO_DECODE_TOKEN.detail}
