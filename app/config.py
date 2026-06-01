from importlib.metadata import version, metadata
from pydantic_settings import BaseSettings, SettingsConfigDict


APP_NAME = metadata("sda-model-deployment")["Name"].title()
APP_VERSION = version("sda-model-deployment")
APP_DESCRIPTION = metadata("sda-model-deployment").get("Summary", "")


class Settings(BaseSettings):
    model_name: str = "my-model"
    temperature: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


SETTINGS = Settings()
