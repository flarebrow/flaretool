from flaretool.settings import *


def test_base_settings_default():
    settings = BaseSettings()
    assert settings.api_key is None


def test_base_settings_env_file(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_api_key")
    settings = BaseSettings()
    assert settings.api_key == "test_api_key"


def test_get_settings():
    settings = get_settings()
    assert isinstance(settings, BaseSettings)
