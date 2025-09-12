"""
Development runner script for the GitHub Discord Webhook Bot.

This script provides a convenient way to run the bot in development mode
with proper error handling and logging.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from main import main

if __name__ == "__main__":
    """
    Run the bot in development mode.
    
    This script sets up proper logging and runs the bot with
    development-friendly settings.
    """
    # Set up logging
    config.setup_logging()
    logger = logging.getLogger(__name__)
    
    # Validate configuration
    try:
        config.validate()
        logger.info("✅ Configuration validated successfully")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    
    # Print startup information
    logger.info("🚀 Starting Patchy - GitHub Discord Webhook Bot in development mode...")
    logger.info(f"📡 Webhook server will be available at: http://{config.HOST}:{config.PORT}")
    logger.info(f"🔗 Webhook endpoint: http://{config.HOST}:{config.PORT}/webhook")
    logger.info(f"💬 Discord channel ID: {config.DISCORD_CHANNEL_ID}")
    logger.info(f"📊 Log level: {config.LOG_LEVEL}")
    
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Bot crashed: {e}")
        sys.exit(1)
