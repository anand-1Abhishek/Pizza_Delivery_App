# core/config.py
import secrets
from typing import Optional
from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Order Management System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle special characters in password by using urllib.parse.quote_plus
        from urllib.parse import quote_plus
        password = quote_plus(self.POSTGRES_PASSWORD)
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()