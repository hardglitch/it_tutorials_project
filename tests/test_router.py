from fastapi.encoders import jsonable_encoder
from starlette import status
from app.dictionary.schemas import AddWordToDictionaryScheme
from app.language.schemas import LanguageScheme
from app.tutorial.theme.schemas import AddTutorialThemeScheme
from app.user.exceptions import UserExceptions
from setup import Setup


class TestUrlsNegative(Setup):

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

    def test_unprocessable_entity1_negative(self):
        response = Setup.client.post("/lang/add", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_unprocessable_entity2_negative(self):
        response = Setup.client.put("/lang/edit", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_negative(self):
        response = Setup.client.delete("/lang/asd")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAddNewElementNegative(Setup):

    def test_add_language_negative(self):
        new_lang = jsonable_encoder(LanguageScheme(abbreviation="eng", value="english", is_ui_lang=True))
        response = Setup.client.post("/lang/add", json=new_lang)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": UserExceptions.ACCESS_DENIED.detail}

    def test_add_dist_type_negative(self):
        new_dist_type = jsonable_encoder(AddWordToDictionaryScheme(lang_code=0, value="free"))
        response = Setup.client.post("/tutorial/dist-type/add", json=new_dist_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": UserExceptions.ACCESS_DENIED.detail}

    def test_add_type_negative(self):
        new_type = jsonable_encoder(AddWordToDictionaryScheme(lang_code=0, value="New Type"))
        response = Setup.client.post("/tutorial/type/add", json=new_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": UserExceptions.ACCESS_DENIED.detail}

    def test_add_theme_negative(self):
        new_theme = jsonable_encoder(AddTutorialThemeScheme(lang_code=0, value="Python", type_code=0))
        response = Setup.client.post("/tutorial/theme/add", json=new_theme)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": UserExceptions.ACCESS_DENIED.detail}
