from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from pydantic import EmailStr, HttpUrl, parse_obj_as
from app.common.constants import Credential
from app.dictionary.schemas import AddWordToDictionaryScheme
from app.language.schemas import LanguageScheme
from app.main import app, MainRouter
from app.tutorial.schemas import AddTutorialScheme
from app.tutorial.theme.schemas import AddTutorialThemeScheme
from app.user.exceptions import UserExceptions
from app.user.schemas import AddUserScheme

client = TestClient(app, base_url="http://localhost")
MainRouter(app)


class TestAddNewElementWithoutAdminCredential:

    def test_add_language_without_admin_credential(self):
        new_lang = jsonable_encoder(LanguageScheme(abbreviation="eng", value="english", is_ui_lang=True))
        response = client.post("/lang/add", json=new_lang)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": "Access denied"}
        # assert response.status_code is CommonResponses.CREATED.status_code

    def test_add_dist_type_without_admin_credential(self):
        new_dist_type = jsonable_encoder(AddWordToDictionaryScheme(lang_code=0, value="free"))
        response = client.post("/tutorial/dist-type/add", json=new_dist_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": "Access denied"}

    def test_add_type_without_admin_credential(self):
        new_type = jsonable_encoder(AddWordToDictionaryScheme(lang_code=0, value="New Type"))
        response = client.post("/tutorial/type/add", json=new_type)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": "Access denied"}

    def test_add_theme_without_admin_credential(self):
        new_theme = jsonable_encoder(AddTutorialThemeScheme(lang_code=0, value="Python", type_code=0))
        response = client.post("/tutorial/theme/add", json=new_theme)
        assert response.status_code == UserExceptions.ACCESS_DENIED.status_code
        assert response.json() == {"detail": "Access denied"}
