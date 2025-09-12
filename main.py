"""
Main application entry point for the GitHub Discord Webhook Bot.

This module orchestrates the Discord bot and webhook server, handling
startup, shutdown, and error management.
"""

import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from webhook_server import app as webhook_app
from discord_bot import start_bot, stop_bot
from config import config, setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for FastAPI.
    
    Handles startup and shutdown of the Discord bot alongside the webhook server.
    
    Args:
        app (FastAPI): The FastAPI application instance
        
    Yields:
        None: Control to the application
    """
    # Startup
    logger.info("Starting Patchy - GitHub Discord Webhook Bot...")
    
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated successfully")
        
        # Start Discord bot in background
        bot_task = asyncio.create_task(start_bot())
        logger.info("Discord bot startup task created")
        
        # Wait a moment for bot to initialize
        await asyncio.sleep(2)
        
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)
    
    # Yield control to the application
    yield
    
    # Shutdown
    logger.info("Shutting down Patchy - GitHub Discord Webhook Bot...")
    
    try:
        # Stop Discord bot
        await stop_bot()
        logger.info("Discord bot stopped successfully")
        
        # Cancel bot task if still running
        if 'bot_task' in locals():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Application shutdown completed successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="Patchy - GitHub Discord Webhook Bot",
    description="Patchy's webhook server for receiving GitHub events and sending Discord notifications",
    version="1.0.0",
    lifespan=lifespan
)

# Include webhook routes
app.include_router(webhook_app.router)


def setup_signal_handlers() -> None:
    """
    Set up signal handlers for graceful shutdown.
    
    Handles SIGINT (Ctrl+C) and SIGTERM signals to ensure
    proper cleanup when the application is terminated.
    """
    def signal_handler(signum: int, frame) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main() -> None:
    """
    Main application entry point.
    
    Sets up signal handlers and starts the webhook server.
    """
    try:
        # Set up signal handlers
        setup_signal_handlers()
        
        # Configure uvicorn server
        config_uvicorn = uvicorn.Config(
            app=app,
            host=config.HOST,
            port=config.PORT,
            log_level=config.LOG_LEVEL.lower(),
            access_log=True,
            reload=config.DEBUG,
        )
        
        # Create and run server
        server = uvicorn.Server(config_uvicorn)
        logger.info(f"Starting webhook server on {config.HOST}:{config.PORT}")
        
        await server.serve()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """
    Run the application when executed directly.
    
    This allows the application to be run with: python main.py
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)
