"""
Application configuration loaded from environment variables and .env file.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    server_port: int = 8081

    # MongoDB
    mongodb_uri: str = "mongodb+srv://hemanthjanapana:hemu4125@cluster0.fsdukc9.mongodb.net/leafai_hub"
    mongodb_database: str = "leafai_hub"

    # JWT
    jwt_secret: str = "leafai-hub-secret-key-change-in-production-min-256-bits"
    jwt_expiration: int = 86400000  # milliseconds (24 hours)

    # File Upload
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB

    # ML Service
    ml_service_url: str = "http://localhost:5000"
    ml_service_timeout: int = 30000  # milliseconds

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def jwt_expiration_seconds(self) -> int:
        return self.jwt_expiration // 1000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
