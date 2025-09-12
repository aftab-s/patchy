"""
Discord Bot for GitHub Webhook Notifications.

This module contains the Discord bot implementation that receives GitHub webhook
events and posts formatted notifications to a Discord channel.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
import discord
from discord.ext import commands
from config import config

# Set up logging
logger = logging.getLogger(__name__)


class GitHubNotificationBot(commands.Bot):
    """
    Discord bot that handles GitHub webhook notifications.
    
    This bot connects to Discord and provides methods to send formatted
    notifications about GitHub events to a specific channel.
    """
    
    def __init__(self):
        """
        Initialize the Discord bot with appropriate intents and settings.
        
        Configures the bot with necessary intents for sending messages
        and managing webhook notifications.
        """
        # Define intents for the bot
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,  # Disable default help command
            case_insensitive=True
        )
        
        self.target_channel: Optional[discord.TextChannel] = None
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging for the Discord bot."""
        logger.info("Initializing Discord bot...")
    
    async def on_ready(self) -> None:
        """
        Event handler called when the bot is ready and connected to Discord.
        
        This method sets up the target channel and logs the bot's status.
        """
        logger.info(f"Discord bot logged in as {self.user} (ID: {self.user.id})")
        
        # Get the target channel
        try:
            self.target_channel = self.get_channel(config.DISCORD_CHANNEL_ID)
            if self.target_channel is None:
                logger.error(f"Could not find channel with ID: {config.DISCORD_CHANNEL_ID}")
                return
            
            logger.info(f"Bot ready! Monitoring channel: {self.target_channel.name}")
            
            # Send a startup message
            await self._send_startup_message()
            
        except Exception as e:
            logger.error(f"Error setting up target channel: {e}")
    
    async def _send_startup_message(self) -> None:
        """
        Send a startup message to indicate the bot is online.
        
        This helps verify that the bot is working correctly and can
        send messages to the target channel.
        """
        try:
            embed = discord.Embed(
                title="🤖 Patchy - GitHub Notification Bot",
                description="Patchy is now online and ready to receive GitHub webhook notifications!",
                color=0x00ff00  # Green color
            )
            embed.add_field(
                name="Status",
                value="✅ Connected and monitoring",
                inline=False
            )
            embed.set_footer(text="Patchy - GitHub Webhook Bot")
            embed.timestamp = discord.utils.utcnow()
            
            await self.target_channel.send(embed=embed)
            logger.info("Startup message sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
    
    async def send_github_notification(self, embed: discord.Embed) -> bool:
        """
        Send a GitHub notification embed to the target channel.
        
        Args:
            embed (discord.Embed): The formatted embed to send
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if self.target_channel is None:
            logger.error("Target channel not set. Cannot send notification.")
            return False
        
        try:
            await self.target_channel.send(embed=embed)
            logger.info("GitHub notification sent successfully")
            return True
            
        except discord.Forbidden:
            logger.error("Bot doesn't have permission to send messages to the target channel")
            return False
        except discord.HTTPException as e:
            logger.error(f"HTTP error while sending notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while sending notification: {e}")
            return False
    
    async def send_error_notification(self, error_message: str, event_type: str = "Unknown") -> None:
        """
        Send an error notification to the Discord channel.
        
        Args:
            error_message (str): The error message to display
            event_type (str): The type of event that caused the error
        """
        if self.target_channel is None:
            logger.error("Target channel not set. Cannot send error notification.")
            return
        
        try:
            embed = discord.Embed(
                title="⚠️ Webhook Processing Error",
                description=f"An error occurred while processing a {event_type} event:",
                color=0xff0000  # Red color
            )
            embed.add_field(
                name="Error Details",
                value=f"```{error_message[:1000]}```",  # Limit to 1000 chars
                inline=False
            )
            embed.set_footer(text="GitHub Webhook Bot - Error Handler")
            embed.timestamp = discord.utils.utcnow()
            
            await self.target_channel.send(embed=embed)
            logger.info("Error notification sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
    
    async def close(self) -> None:
        """
        Clean shutdown of the Discord bot.
        
        Sends a shutdown message and properly closes the bot connection.
        """
        if self.target_channel is not None:
            try:
                embed = discord.Embed(
                    title="🔴 Patchy - GitHub Notification Bot",
                    description="Patchy is shutting down. Webhook notifications will be paused.",
                    color=0xff0000  # Red color
                )
                embed.set_footer(text="Patchy - GitHub Webhook Bot")
                embed.timestamp = discord.utils.utcnow()
                
                await self.target_channel.send(embed=embed)
                logger.info("Shutdown message sent successfully")
                
            except Exception as e:
                logger.error(f"Failed to send shutdown message: {e}")
        
        await super().close()
        logger.info("Discord bot connection closed")


# Global bot instance
bot_instance: Optional[GitHubNotificationBot] = None


async def get_bot() -> GitHubNotificationBot:
    """
    Get or create the global bot instance.
    
    Returns:
        GitHubNotificationBot: The bot instance
    """
    global bot_instance
    if bot_instance is None:
        bot_instance = GitHubNotificationBot()
    return bot_instance


async def start_bot() -> None:
    """
    Start the Discord bot.
    
    This function initializes and starts the bot connection to Discord.
    """
    global bot_instance
    try:
        bot_instance = GitHubNotificationBot()
        await bot_instance.start(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token. Please check your DISCORD_TOKEN environment variable.")
        raise
    except Exception as e:
        logger.error(f"Failed to start Discord bot: {e}")
        raise


async def stop_bot() -> None:
    """
    Stop the Discord bot gracefully.
    
    This function properly closes the bot connection and cleans up resources.
    """
    global bot_instance
    if bot_instance is not None:
        await bot_instance.close()
        bot_instance = None
        logger.info("Discord bot stopped")
