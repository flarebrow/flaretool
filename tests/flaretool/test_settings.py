from flaretool.settings import *


def test_get_settings():
    settings = get_settings()
    assert isinstance(settings, BaseSettings)
    assert settings.api_key == None
    assert isinstance(settings.get(), BaseSettings)
    assert settings.Config._load_env_file() == None
    assert settings.Config._get_environment_variable(
        "API_KEY", None) == settings.api_key
