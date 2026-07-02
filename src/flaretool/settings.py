"""flaretool settings loaded from the environment / ``.env`` file."""

from functools import lru_cache

from pydantic_settings import BaseSettings as _PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_PydanticBaseSettings):
    """flaretool settings.

    The class is named ``BaseSettings`` for backwards compatibility;
    prefer the ``FlareToolSettings`` alias in new code.
    """

    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


FlareToolSettings = BaseSettings


@lru_cache(maxsize=1)
def get_settings() -> BaseSettings:
    """Return the (cached) settings instance.

    The environment / ``.env`` file is read once per process; construct
    ``BaseSettings()`` directly if a fresh read is needed.
    """
    return BaseSettings()
