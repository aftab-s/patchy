"""
Railway Deployment Test Script
Test your deployed webhook endpoint on Railway
"""

import asyncio
import json
import hmac
import hashlib
import logging
import sys
import os
from typing import Dict, Any

import httpx

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Railway endpoint
RAILWAY_ENDPOINT = "https://web-production-13df.up.railway.app"

def generate_github_signature(payload: str, secret: str) -> str:
    """Generate GitHub webhook signature."""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

async def test_railway_webhook():
    """Test the Railway webhook endpoint."""
    
    # Get webhook secret from environment or prompt
    webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')
    if not webhook_secret:
        webhook_secret = input("Enter your GITHUB_WEBHOOK_SECRET: ")
    
    # Sample push payload
    payload = {
        "ref": "refs/heads/main",
        "repository": {
            "name": "patchy",
            "full_name": "aftab-s/patchy",
            "html_url": "https://github.com/aftab-s/patchy",
            "description": "Patchy - GitHub Discord Webhook Bot"
        },
        "pusher": {
            "name": "aftab-s",
            "avatar_url": "https://github.com/aftab-s.png"
        },
        "commits": [
            {
                "id": "railway123",
                "message": "🚀 Deploy to Railway - Production ready!",
                "url": "https://github.com/aftab-s/patchy/commit/railway123",
                "author": {
                    "name": "Aftab S",
                    "email": "aftab@example.com"
                },
                "added": [],
                "modified": ["README.md"],
                "removed": []
            }
        ],
        "compare": "https://github.com/aftab-s/patchy/compare/abc123...railway123"
    }
    
    payload_str = json.dumps(payload, separators=(',', ':'))
    signature = generate_github_signature(payload_str, webhook_secret)
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push",
        "X-Hub-Signature-256": signature,
        "User-Agent": "GitHub-Hookshot/test"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Test health endpoint
            logger.info("Testing Railway health endpoint...")
            health_response = await client.get(f"{RAILWAY_ENDPOINT}/health")
            logger.info(f"✅ Health check: {health_response.status_code}")
            logger.info(f"Response: {health_response.json()}")
            
            # Test webhook endpoint
            logger.info("Testing Railway webhook endpoint...")
            webhook_response = await client.post(
                f"{RAILWAY_ENDPOINT}/webhook",
                content=payload_str,
                headers=headers
            )
            
            if webhook_response.status_code == 200:
                logger.info(f"✅ Webhook test successful!")
                logger.info(f"Response: {webhook_response.json()}")
                logger.info("🎉 Your bot should have sent a message to Discord!")
            else:
                logger.error(f"❌ Webhook test failed: {webhook_response.status_code}")
                logger.error(f"Response: {webhook_response.text}")
                
        except Exception as e:
            logger.error(f"❌ Request failed: {e}")

async def main():
    """Main test function."""
    logger.info("🚀 Testing Railway Deployment")
    logger.info(f"Endpoint: {RAILWAY_ENDPOINT}")
    logger.info("=" * 50)
    
    await test_railway_webhook()
    
    logger.info("=" * 50)
    logger.info("Next steps:")
    logger.info("1. If test passed, configure GitHub webhook with:")
    logger.info(f"   URL: {RAILWAY_ENDPOINT}/webhook")
    logger.info("2. Make a real commit to test live webhook")
    logger.info("3. Check your Discord channel for notifications")

if __name__ == "__main__":
    asyncio.run(main())