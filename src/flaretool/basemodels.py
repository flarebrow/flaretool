"""Base data models for flaretool services."""

from pydantic import BaseModel


class BaseDataModel(BaseModel):
    def __trace__(self) -> str:
        return "\n".join(
            f"{key}='{val}'"
            for key, val in self.__dict__.items()
            if not key.startswith("_")
        )

    def __str__(self) -> str:
        columns = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"{self.__class__.__name__}({columns})"
