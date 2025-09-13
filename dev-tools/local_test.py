"""
Local Development Testing Script for Patchy Discord Bot.

This script helps you test your webhook locally with various scenarios
and provides easy commands for local development.
"""

import asyncio
import json
import hmac
import hashlib
import logging
import sys
from typing import Dict, Any, Optional

import httpx
from config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_github_signature(payload: str, secret: str) -> str:
    """
    Generate GitHub webhook signature for testing.
    
    Args:
        payload: JSON payload as string
        secret: Webhook secret
        
    Returns:
        GitHub-compatible signature string
    """
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


async def test_webhook_with_signature(
    base_url: str = "http://localhost:8000",
    event_type: str = "push"
) -> None:
    """
    Test webhook endpoint with proper GitHub signature.
    
    Args:
        base_url: Base URL of your local webhook server
        event_type: GitHub event type to simulate
    """
    logger.info(f"Testing webhook endpoint: {base_url}")
    
    # Sample payloads for different event types
    payloads = {
        "push": {
            "ref": "refs/heads/main",
            "repository": {
                "name": "patchy-test",
                "full_name": "aftab-s/patchy-test",
                "html_url": "https://github.com/aftab-s/patchy-test",
                "description": "Test repository for Patchy Discord Bot"
            },
            "pusher": {
                "name": "aftab-s",
                "avatar_url": "https://github.com/aftab-s.png"
            },
            "commits": [
                {
                    "id": "abc123def456",
                    "message": "Add new feature: enhanced webhook processing",
                    "url": "https://github.com/aftab-s/patchy-test/commit/abc123def456",
                    "author": {
                        "name": "Aftab S",
                        "email": "aftab@example.com"
                    },
                    "added": ["src/new_feature.py"],
                    "modified": ["README.md"],
                    "removed": []
                }
            ],
            "compare": "https://github.com/aftab-s/patchy-test/compare/abc123...def456"
        },
        "pull_request": {
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "Add amazing new feature",
                "body": "This PR adds an amazing new feature that will revolutionize everything!",
                "html_url": "https://github.com/aftab-s/patchy-test/pull/42",
                "state": "open",
                "user": {
                    "login": "aftab-s",
                    "avatar_url": "https://github.com/aftab-s.png"
                },
                "head": {
                    "ref": "feature/amazing-feature",
                    "sha": "def456"
                },
                "base": {
                    "ref": "main"
                }
            },
            "repository": {
                "name": "patchy-test",
                "full_name": "aftab-s/patchy-test",
                "html_url": "https://github.com/aftab-s/patchy-test"
            }
        },
        "issues": {
            "action": "opened",
            "issue": {
                "number": 15,
                "title": "Bug: Application crashes on startup",
                "body": "The application crashes when starting with the latest version.",
                "html_url": "https://github.com/aftab-s/patchy-test/issues/15",
                "state": "open",
                "user": {
                    "login": "aftab-s",
                    "avatar_url": "https://github.com/aftab-s.png"
                }
            },
            "repository": {
                "name": "patchy-test",
                "full_name": "aftab-s/patchy-test",
                "html_url": "https://github.com/aftab-s/patchy-test"
            }
        }
    }
    
    if event_type not in payloads:
        logger.error(f"Unknown event type: {event_type}")
        logger.info(f"Available event types: {list(payloads.keys())}")
        return
    
    payload = payloads[event_type]
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # Generate proper signature
    signature = generate_github_signature(payload_str, config.GITHUB_WEBHOOK_SECRET)
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": event_type,
        "X-Hub-Signature-256": signature,
        "User-Agent": "GitHub-Hookshot/test"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Test health endpoint first
            health_response = await client.get(f"{base_url}/health")
            logger.info(f"✅ Health check: {health_response.status_code}")
            
            # Test webhook endpoint
            webhook_response = await client.post(
                f"{base_url}/webhook",
                content=payload_str,
                headers=headers,
                timeout=30.0
            )
            
            if webhook_response.status_code == 200:
                logger.info(f"✅ Webhook test successful: {event_type}")
                logger.info(f"Response: {webhook_response.json()}")
            else:
                logger.error(f"❌ Webhook test failed: {webhook_response.status_code}")
                logger.error(f"Response: {webhook_response.text}")
                
        except Exception as e:
            logger.error(f"❌ Request failed: {e}")


async def test_all_events(base_url: str = "http://localhost:8000") -> None:
    """Test all supported webhook event types."""
    events = ["push", "pull_request", "issues"]
    
    logger.info("Testing all webhook event types...")
    
    for event in events:
        logger.info(f"\n--- Testing {event} event ---")
        await test_webhook_with_signature(base_url, event)
        await asyncio.sleep(2)  # Wait between tests


def check_configuration() -> bool:
    """
    Check if all required configuration is present.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    logger.info("Checking configuration...")
    
    required_config = {
        "DISCORD_TOKEN": config.DISCORD_TOKEN,
        "DISCORD_CHANNEL_ID": config.DISCORD_CHANNEL_ID,
        "GITHUB_WEBHOOK_SECRET": config.GITHUB_WEBHOOK_SECRET,
    }
    
    missing = []
    for key, value in required_config.items():
        if not value:
            missing.append(key)
        else:
            logger.info(f"✅ {key}: {'*' * (len(str(value)) - 4)}{str(value)[-4:]}")
    
    if missing:
        logger.error(f"❌ Missing configuration: {', '.join(missing)}")
        logger.error("Please check your .env file")
        return False
    
    logger.info(f"✅ Configuration valid")
    return True


def print_ngrok_setup_instructions():
    """Print instructions for setting up ngrok."""
    print("""
🌐 NGROK SETUP INSTRUCTIONS

1. Install ngrok:
   - Go to https://ngrok.com and sign up
   - Download ngrok for Windows
   - Extract and add to PATH or place in project directory

2. Start your Discord bot:
   python main.py

3. In another terminal, start ngrok:
   ngrok http 8000

4. Copy the HTTPS URL from ngrok (e.g., https://abc123.ngrok-free.app)

5. Configure GitHub webhook:
   - Go to your repository → Settings → Webhooks
   - Add webhook with URL: https://abc123.ngrok-free.app/webhook
   - Content type: application/json
   - Secret: Your GITHUB_WEBHOOK_SECRET
   - Select events: push, pull_request, issues (or "Send me everything")

6. Test by making a commit or opening a PR!

💡 TIP: Keep ngrok web interface open at http://localhost:4040 to monitor requests
    """)


async def main():
    """Main function for local testing."""
    if len(sys.argv) < 2:
        print("""
🧪 PATCHY LOCAL TESTING UTILITY

Usage:
  python local_test.py config          - Check configuration
  python local_test.py test [event]    - Test webhook (default: push)
  python local_test.py test-all        - Test all event types
  python local_test.py ngrok-help      - Show ngrok setup instructions

Examples:
  python local_test.py test push
  python local_test.py test pull_request
  python local_test.py test issues
        """)
        return
    
    command = sys.argv[1]
    
    if command == "config":
        check_configuration()
    
    elif command == "test":
        if not check_configuration():
            return
        
        event_type = sys.argv[2] if len(sys.argv) > 2 else "push"
        base_url = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:8000"
        
        await test_webhook_with_signature(base_url, event_type)
    
    elif command == "test-all":
        if not check_configuration():
            return
        
        base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
        await test_all_events(base_url)
    
    elif command == "ngrok-help":
        print_ngrok_setup_instructions()
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())