"""
Configuration settings for the Secretaria El Cano application.
This module handles all configuration from environment variables and provides defaults.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    url: str
    init_db: bool
    host: str
    port: int
    database: str
    username: str
    password: str

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create database configuration from environment variables."""
        host = os.getenv("DB_HOST", "localhost")
        port = int(os.getenv("DB_PORT", "3306"))
        database = os.getenv("DB_NAME", "secretaria-el-cano")
        username = os.getenv("DB_USERNAME", "root")
        password = os.getenv("DB_PASSWORD", "nolasabrasnunca1970")
        
        url = os.getenv(
            "DATABASE_URL",
            f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        )
        
        return cls(
            url=url,
            init_db=os.getenv("INIT_DB", "False").lower() == "true",
            host=host,
            port=port,
            database=database,
            username=username,
            password=password
        )


@dataclass
class AuthConfig:
    """Authentication configuration settings."""
    
    cookie_name: str
    secret_key: str
    cookie_expiry_days: int

    @classmethod
    def from_env(cls) -> 'AuthConfig':
        """Create authentication configuration from environment variables."""
        return cls(
            cookie_name=os.getenv("AUTH_COOKIE_NAME", "falla_cookie"),
            secret_key=os.getenv("AUTH_SECRET_KEY", "auth_secret_key"),
            cookie_expiry_days=int(os.getenv("AUTH_COOKIE_EXPIRY_DAYS", "1"))
        )


@dataclass
class AppConfig:
    """Main application configuration."""
    
    app_name: str
    app_icon: str
    layout: str
    logo_path: str
    debug: bool

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create application configuration from environment variables."""
        return cls(
            app_name=os.getenv("APP_NAME", "Secretaría El Cano"),
            app_icon=os.getenv("APP_ICON", "🔥"),
            layout=os.getenv("APP_LAYOUT", "wide"),
            logo_path=os.getenv("LOGO_PATH", "assets/logo.png"),
            debug=os.getenv("DEBUG", "False").lower() == "true"
        )


class Settings:
    """Application settings container."""
    
    def __init__(self):
        self.database = DatabaseConfig.from_env()
        self.auth = AuthConfig.from_env()
        self.app = AppConfig.from_env()

    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return self.database

    def get_auth_config(self) -> AuthConfig:
        """Get authentication configuration."""
        return self.auth

    def get_app_config(self) -> AppConfig:
        """Get application configuration."""
        return self.app


# Global settings instance
settings = Settings()