from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    qbit_url: str = "http://localhost:8080"
    qbit_username: str = "admin"
    qbit_password: str = "change_me"

    downloads_dir: Path = Path(__file__).resolve().parent.parent.parent / "data" / "downloads"
    # Path where the qBittorrent container sees the same volume (docker-compose.yml: ./data/downloads -> /downloads)
    qbit_container_downloads_path: str = "/downloads"

    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
