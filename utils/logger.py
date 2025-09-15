"""
Logging configuration for the Secretaria El Cano application.

This module provides centralized logging configuration with appropriate
formatters and handlers for development and production environments.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from config.settings import settings


class Logger:
    """Centralized logger configuration."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Get a configured logger instance.
        
        Args:
            name: Name of the logger.
            
        Returns:
            Configured logger instance.
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            cls._configure_logger(logger)
        
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def _configure_logger(cls, logger: logging.Logger) -> None:
        """
        Configure a logger with appropriate handlers and formatters.
        
        Args:
            logger: Logger instance to configure.
        """
        app_config = settings.get_app_config()
        level = logging.DEBUG if app_config.debug else logging.INFO
        
        logger.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
        # File handler for production
        if not app_config.debug:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_dir / "app.log")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Prevent duplicate logs
        logger.propagate = False


# Convenience function for getting a logger
def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger.
        
    Returns:
        Configured logger instance.
    """
    return Logger.get_logger(name)