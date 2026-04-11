from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    yandex_disk_token: str
    base_url: str = "https://cloud-api.yandex.net/v1/disk"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
