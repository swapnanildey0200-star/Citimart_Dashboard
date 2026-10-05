import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Citimart Retail Analytics Dashboard"
    APP_ENV: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Database
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "citimart_retail"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    
    # Business logic & formatting
    CURRENCY_CODE: str = "INR"
    CURRENCY_SYMBOL: str = "₹"
    NUMBER_FORMAT: str = "lakh_crore"
    
    # Security
    MAX_UPLOAD_SIZE_MB: int = 50
    SECRET_KEY: str = "citimart-secret-analytics-key"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()
