"""
Configuration management for the Discord GitHub Bot.

This module handles environment variable loading and provides centralized
configuration for the Discord bot and webhook server.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class that manages all environment variables and settings.
    
    This class provides a centralized way to access configuration values
    with proper validation and default values.
    """
    
    # Discord Configuration
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    
    # GitHub Webhook Configuration
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_discord_channel_id(cls) -> int:
        """Get Discord channel ID with proper error handling."""
        try:
            return int(os.getenv("DISCORD_CHANNEL_ID", "0"))
        except (ValueError, TypeError):
            return 0
    
    @classmethod
    def get_port(cls) -> int:
        """Get port with proper error handling."""
        try:
            return int(os.getenv("PORT", "8000"))
        except (ValueError, TypeError):
            return 8000
    
    # Properties for backward compatibility
    DISCORD_CHANNEL_ID: int = get_discord_channel_id()
    PORT: int = get_port()
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration values are present.
        
        Returns:
            bool: True if all required values are present, False otherwise
            
        Raises:
            ValueError: If required configuration values are missing
        """
        required_vars = {
            "DISCORD_TOKEN": cls.DISCORD_TOKEN,
            "DISCORD_CHANNEL_ID": cls.DISCORD_CHANNEL_ID,
            "GITHUB_WEBHOOK_SECRET": cls.GITHUB_WEBHOOK_SECRET,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file or environment variables."
            )
        
        return True
    
    @classmethod
    def setup_logging(cls) -> None:
        """
        Configure logging based on the LOG_LEVEL environment variable.
        
        Sets up structured logging with appropriate formatting and level.
        """
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Reduce noise from external libraries
        logging.getLogger("discord").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Global config instance
config = Config()
