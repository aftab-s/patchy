"""
Vercel serverless webhook handler for GitHub events.

This module handles GitHub webhook events in a serverless environment,
sending notifications directly to Discord without maintaining a persistent bot connection.
"""

import hashlib
import hmac
import json
import os
import logging
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """
    Verify the GitHub webhook signature to ensure authenticity.
    
    Args:
        payload (bytes): The raw request payload
        signature (str): The X-Hub-Signature-256 header value
        
    Returns:
        bool: True if the signature is valid, False otherwise
    """
    webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    
    if not webhook_secret:
        logger.warning("GitHub webhook secret not configured. Skipping signature verification.")
        return True
    
    if not signature.startswith('sha256='):
        logger.error("Invalid signature format")
        return False
    
    try:
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        received_signature = signature[7:]  # Remove 'sha256=' prefix
        
        return hmac.compare_digest(expected_signature, received_signature)
        
    except Exception as e:
        logger.error(f"Error verifying GitHub signature: {e}")
        return False


async def send_discord_message(embed_data: Dict[str, Any]) -> bool:
    """
    Send a message to Discord using webhook or direct API.
    
    Args:
        embed_data (Dict[str, Any]): The embed data to send
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    discord_token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    
    if not discord_token or not channel_id:
        logger.error("Discord token or channel ID not configured")
        return False
    
    try:
        # Discord API endpoint for sending messages
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        
        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "embeds": [embed_data]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                logger.info("Discord message sent successfully")
                return True
            else:
                logger.error(f"Failed to send Discord message: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        logger.error(f"Error sending Discord message: {e}")
        return False


def create_push_embed(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Discord embed for push events.
    
    Args:
        payload (Dict[str, Any]): The GitHub push event payload
        
    Returns:
        Dict[str, Any]: The formatted push event embed
    """
    repository = payload.get("repository", {})
    pusher = payload.get("pusher", {})
    commits = payload.get("commits", [])
    ref = payload.get("ref", "")
    compare_url = payload.get("compare", "")
    
    # Determine branch name
    branch = ref.replace("refs/heads/", "") if ref.startswith("refs/heads/") else ref
    
    # Create embed
    embed = {
        "title": f"📝 New Push to {branch}",
        "description": f"**{len(commits)} commit(s)** pushed to `{repository.get('name', 'Unknown')}`",
        "color": 0x28a745,  # Green color
        "url": compare_url,
        "fields": [
            {
                "name": "Repository",
                "value": f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
                "inline": True
            },
            {
                "name": "Pushed by",
                "value": pusher.get("name", "Unknown"),
                "inline": True
            },
            {
                "name": "Commits",
                "value": str(len(commits)),
                "inline": True
            }
        ],
        "author": {
            "name": pusher.get("name", "Unknown"),
            "icon_url": pusher.get("avatar_url", "")
        },
        "footer": {
            "text": "Patchy - GitHub Push Event"
        },
        "timestamp": None  # Will be set by Discord
    }
    
    # Add latest commit info if available
    if commits:
        latest_commit = commits[-1]
        commit_message = latest_commit.get("message", "No message")
        # Truncate long commit messages
        if len(commit_message) > 100:
            commit_message = commit_message[:97] + "..."
        
        embed["fields"].append({
            "name": "Latest Commit",
            "value": f"[{commit_message}]({latest_commit.get('url', '#')})",
            "inline": False
        })
    
    return embed


def create_pull_request_embed(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Discord embed for pull request events.
    
    Args:
        payload (Dict[str, Any]): The GitHub pull request event payload
        
    Returns:
        Dict[str, Any]: The formatted pull request event embed
    """
    pr = payload.get("pull_request", {})
    action = payload.get("action", "")
    repository = payload.get("repository", {})
    
    # Determine color based on action
    color_map = {
        "opened": 0x28a745,    # Green
        "closed": 0xdc3545,    # Red
        "merged": 0x6f42c1,    # Purple
        "reopened": 0x17a2b8,  # Blue
    }
    color = color_map.get(action, 0x6c757d)  # Default gray
    
    # Create embed
    embed = {
        "title": f"🔀 Pull Request {action.title()}",
        "description": f"**{pr.get('title', 'No title')}**",
        "color": color,
        "url": pr.get("html_url", "#"),
        "fields": [
            {
                "name": f"PR #{pr.get('number', '?')}",
                "value": f"**{pr.get('state', 'unknown').title()}**",
                "inline": True
            },
            {
                "name": "Repository",
                "value": f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
                "inline": True
            },
            {
                "name": "Author",
                "value": pr.get("user", {}).get("login", "Unknown"),
                "inline": True
            }
        ],
        "author": {
            "name": pr.get("user", {}).get("login", "Unknown"),
            "icon_url": pr.get("user", {}).get("avatar_url", "")
        },
        "footer": {
            "text": "Patchy - GitHub Pull Request Event"
        },
        "timestamp": None
    }
    
    # Add description if available
    body = pr.get("body", "")
    if body:
        # Truncate long descriptions
        if len(body) > 500:
            body = body[:497] + "..."
        embed["fields"].append({
            "name": "Description",
            "value": body,
            "inline": False
        })
    
    return embed


def create_issue_embed(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Discord embed for issue events.
    
    Args:
        payload (Dict[str, Any]): The GitHub issue event payload
        
    Returns:
        Dict[str, Any]: The formatted issue event embed
    """
    issue = payload.get("issue", {})
    action = payload.get("action", "")
    repository = payload.get("repository", {})
    
    # Determine color based on action
    color_map = {
        "opened": 0xdc3545,    # Red
        "closed": 0x28a745,    # Green
        "reopened": 0x17a2b8,  # Blue
    }
    color = color_map.get(action, 0x6c757d)  # Default gray
    
    # Create embed
    embed = {
        "title": f"🐛 Issue {action.title()}",
        "description": f"**{issue.get('title', 'No title')}**",
        "color": color,
        "url": issue.get("html_url", "#"),
        "fields": [
            {
                "name": f"Issue #{issue.get('number', '?')}",
                "value": f"**{issue.get('state', 'unknown').title()}**",
                "inline": True
            },
            {
                "name": "Repository",
                "value": f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
                "inline": True
            },
            {
                "name": "Author",
                "value": issue.get("user", {}).get("login", "Unknown"),
                "inline": True
            }
        ],
        "author": {
            "name": issue.get("user", {}).get("login", "Unknown"),
            "icon_url": issue.get("user", {}).get("avatar_url", "")
        },
        "footer": {
            "text": "Patchy - GitHub Issue Event"
        },
        "timestamp": None
    }
    
    # Add labels if available
    labels = issue.get("labels", [])
    if labels:
        label_names = [label.get("name", "") for label in labels[:5]]  # Limit to 5 labels
        embed["fields"].append({
            "name": "Labels",
            "value": ", ".join(label_names),
            "inline": False
        })
    
    return embed


def create_release_embed(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Discord embed for release events.
    
    Args:
        payload (Dict[str, Any]): The GitHub release event payload
        
    Returns:
        Dict[str, Any]: The formatted release event embed
    """
    release = payload.get("release", {})
    action = payload.get("action", "")
    repository = payload.get("repository", {})
    
    # Create embed
    embed = {
        "title": f"🚀 Release {action.title()}",
        "description": f"**{release.get('name', release.get('tag_name', 'No title'))}**",
        "color": 0xffc107,  # Yellow/Orange color
        "url": release.get("html_url", "#"),
        "fields": [
            {
                "name": "Tag",
                "value": release.get("tag_name", "No tag"),
                "inline": True
            },
            {
                "name": "Repository",
                "value": f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
                "inline": True
            },
            {
                "name": "Author",
                "value": release.get("author", {}).get("login", "Unknown"),
                "inline": True
            }
        ],
        "author": {
            "name": release.get("author", {}).get("login", "Unknown"),
            "icon_url": release.get("author", {}).get("avatar_url", "")
        },
        "footer": {
            "text": "Patchy - GitHub Release Event"
        },
        "timestamp": None
    }
    
    # Add description if available
    body = release.get("body", "")
    if body:
        # Truncate long descriptions
        if len(body) > 500:
            body = body[:497] + "..."
        embed["fields"].append({
            "name": "Description",
            "value": body,
            "inline": False
        })
    
    return embed


def create_event_embed(event_type: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Create a Discord embed based on the GitHub event type and payload.
    
    Args:
        event_type (str): The type of GitHub event
        payload (Dict[str, Any]): The GitHub webhook payload
        
    Returns:
        Optional[Dict[str, Any]]: The formatted embed or None if event type is not supported
    """
    try:
        if event_type == "push":
            return create_push_embed(payload)
        elif event_type == "pull_request":
            return create_pull_request_embed(payload)
        elif event_type == "issues":
            return create_issue_embed(payload)
        elif event_type == "release":
            return create_release_embed(payload)
        else:
            logger.info(f"Unsupported event type: {event_type}")
            return None
            
    except Exception as e:
        logger.error(f"Error creating embed for {event_type}: {e}")
        return None


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless webhook handler for GitHub events.
    
    Handles GitHub webhook events and sends formatted notifications to Discord.
    """
    
    def do_POST(self):
        """
        Handle POST requests for GitHub webhooks.
        
        Processes GitHub webhook events and sends Discord notifications.
        """
        try:
            if self.path != '/webhook':
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "error": "Not Found",
                    "message": "Webhook endpoint not found"
                }
                
                response = json.dumps(error_response, indent=2)
                self.wfile.write(response.encode('utf-8'))
                return
            
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the request body
            post_data = self.rfile.read(content_length)
            
            # Get headers
            signature = self.headers.get("X-Hub-Signature-256", "")
            event_type = self.headers.get("X-GitHub-Event", "")
            
            # Verify signature
            if not verify_github_signature(post_data, signature):
                logger.warning("Invalid GitHub webhook signature")
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "error": "Unauthorized",
                    "message": "Invalid signature"
                }
                
                response = json.dumps(error_response, indent=2)
                self.wfile.write(response.encode('utf-8'))
                return
            
            # Parse JSON payload
            try:
                payload = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON payload: {e}")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "error": "Bad Request",
                    "message": "Invalid JSON payload"
                }
                
                response = json.dumps(error_response, indent=2)
                self.wfile.write(response.encode('utf-8'))
                return
            
            # Log the event
            logger.info(f"Received {event_type} event from GitHub")
            
            # Create embed and send to Discord
            embed = create_event_embed(event_type, payload)
            
            if embed:
                # Send to Discord asynchronously
                import asyncio
                success = asyncio.run(send_discord_message(embed))
                
                if success:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    success_response = {
                        "message": "Event processed successfully",
                        "event_type": event_type
                    }
                    
                    response = json.dumps(success_response, indent=2)
                    self.wfile.write(response.encode('utf-8'))
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    error_response = {
                        "error": "Internal Server Error",
                        "message": "Failed to send Discord notification"
                    }
                    
                    response = json.dumps(error_response, indent=2)
                    self.wfile.write(response.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                success_response = {
                    "message": "Event received but not processed",
                    "event_type": event_type,
                    "reason": "Unsupported event type"
                }
                
                response = json.dumps(success_response, indent=2)
                self.wfile.write(response.encode('utf-8'))
                
        except Exception as e:
            logger.error(f"Unexpected error in webhook handler: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "error": "Internal Server Error",
                "message": str(e)
            }
            
            response = json.dumps(error_response, indent=2)
            self.wfile.write(response.encode('utf-8'))
    
    def do_GET(self):
        """
        Handle GET requests (redirect to health check).
        """
        self.send_response(302)
        self.send_header('Location', '/health')
        self.end_headers()
    
    def log_message(self, format, *args):
        """
        Override log_message to reduce noise in Vercel logs.
        """
        # Only log errors and warnings, not normal requests
        if "error" in format.lower() or "warning" in format.lower():
            super().log_message(format, *args)
