import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Configuration
    api_title: str = "RhymeslikeDimes API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True
    
    # CORS Configuration
    cors_origins: list = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://*.vercel.app",
        "https://rhymeslikedimes.vercel.app"
    ]
    
    # Redis Configuration (optional)
    redis_url: Optional[str] = None
    cache_ttl: int = 3600  # 1 hour
    
    # Datamuse Configuration
    datamuse_max_results: int = 50
    datamuse_timeout: int = 10
    
    # WebSocket Configuration
    ws_heartbeat_interval: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()