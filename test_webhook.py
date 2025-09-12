"""
Test script for the GitHub Discord Webhook Bot.

This script provides utilities to test the webhook endpoint locally
and verify that the bot is working correctly.
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any

import httpx
import discord
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_webhook_endpoint(base_url: str = "http://localhost:8000") -> None:
    """
    Test the webhook endpoint with sample GitHub payloads.
    
    Args:
        base_url (str): The base URL of the webhook server
    """
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        try:
            response = await client.get(f"{base_url}/health")
            logger.info(f"Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return
        
        # Test webhook endpoint with sample push event
        sample_payload = {
            "ref": "refs/heads/main",
            "repository": {
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "html_url": "https://github.com/testuser/test-repo"
            },
            "pusher": {
                "name": "testuser",
                "avatar_url": "https://github.com/testuser.png"
            },
            "commits": [
                {
                    "id": "abc123",
                    "message": "Test commit message",
                    "url": "https://github.com/testuser/test-repo/commit/abc123",
                    "author": {
                        "name": "Test User",
                        "email": "test@example.com"
                    }
                }
            ],
            "compare": "https://github.com/testuser/test-repo/compare/abc123"
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-GitHub-Event": "push",
            "X-Hub-Signature-256": "sha256=test"  # This will fail signature verification, but that's OK for testing
        }
        
        try:
            response = await client.post(
                f"{base_url}/webhook",
                json=sample_payload,
                headers=headers
            )
            logger.info(f"Webhook test: {response.status_code} - {response.json()}")
        except Exception as e:
            logger.error(f"Webhook test failed: {e}")


async def test_discord_connection() -> None:
    """
    Test the Discord bot connection.
    
    This function verifies that the bot can connect to Discord
    and access the target channel.
    """
    try:
        from discord_bot import GitHubNotificationBot
        
        logger.info("Testing Discord bot connection...")
        
        # Create bot instance
        bot = GitHubNotificationBot()
        
        # Start bot
        await bot.start(config.DISCORD_TOKEN)
        
        # Wait a moment for connection
        await asyncio.sleep(2)
        
        # Check if bot is ready
        if bot.is_ready():
            logger.info("✅ Discord bot connected successfully!")
            
            # Test sending a message
            if bot.target_channel:
                embed = discord.Embed(
                    title="🧪 Test Message",
                    description="This is a test message from Patchy - GitHub Discord Webhook Bot!",
                    color=0x00ff00
                )
                await bot.send_github_notification(embed)
                logger.info("✅ Test message sent successfully!")
            else:
                logger.warning("⚠️ Target channel not found")
        else:
            logger.error("❌ Discord bot failed to connect")
        
        # Close bot
        await bot.close()
        
    except Exception as e:
        logger.error(f"❌ Discord connection test failed: {e}")


def print_config_status() -> None:
    """
    Print the current configuration status.
    
    This helps verify that all required environment variables are set.
    """
    logger.info("Configuration Status:")
    logger.info(f"  Discord Token: {'✅ Set' if config.DISCORD_TOKEN else '❌ Missing'}")
    logger.info(f"  Discord Channel ID: {'✅ Set' if config.DISCORD_CHANNEL_ID else '❌ Missing'}")
    logger.info(f"  GitHub Webhook Secret: {'✅ Set' if config.GITHUB_WEBHOOK_SECRET else '❌ Missing'}")
    logger.info(f"  Host: {config.HOST}")
    logger.info(f"  Port: {config.PORT}")
    logger.info(f"  Debug: {config.DEBUG}")
    logger.info(f"  Log Level: {config.LOG_LEVEL}")


async def main() -> None:
    """
    Main test function.
    
    Runs all tests to verify the bot is working correctly.
    """
    logger.info("Starting Patchy - GitHub Discord Webhook Bot tests...")
    
    # Print configuration status
    print_config_status()
    
    # Test Discord connection
    await test_discord_connection()
    
    # Test webhook endpoint (only if server is running)
    logger.info("Testing webhook endpoint...")
    logger.info("Note: Make sure the webhook server is running (python main.py)")
    await test_webhook_endpoint()
    
    logger.info("Tests completed!")


if __name__ == "__main__":
    """
    Run tests when executed directly.
    
    Usage: python test_webhook.py
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Tests interrupted by user")
    except Exception as e:
        logger.error(f"Tests failed: {e}")
        sys.exit(1)
