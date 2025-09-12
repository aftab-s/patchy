"""
FastAPI webhook server for receiving GitHub webhook events.

This module provides a REST API endpoint that receives GitHub webhook events,
validates them, and forwards formatted notifications to the Discord bot.
"""

import hashlib
import hmac
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import discord
from discord_bot import get_bot
from config import config

# Set up logging
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Patchy - GitHub Discord Webhook Bot",
    description="Patchy's webhook server for receiving GitHub events and sending Discord notifications",
    version="1.0.0"
)


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """
    Verify the GitHub webhook signature to ensure authenticity.
    
    Args:
        payload (bytes): The raw request payload
        signature (str): The X-Hub-Signature-256 header value
        
    Returns:
        bool: True if the signature is valid, False otherwise
    """
    if not config.GITHUB_WEBHOOK_SECRET:
        logger.warning("GitHub webhook secret not configured. Skipping signature verification.")
        return True
    
    if not signature.startswith('sha256='):
        logger.error("Invalid signature format")
        return False
    
    try:
        expected_signature = hmac.new(
            config.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        received_signature = signature[7:]  # Remove 'sha256=' prefix
        
        return hmac.compare_digest(expected_signature, received_signature)
        
    except Exception as e:
        logger.error(f"Error verifying GitHub signature: {e}")
        return False


async def process_github_event(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Process a GitHub webhook event and send appropriate Discord notification.
    
    Args:
        event_type (str): The type of GitHub event (push, pull_request, etc.)
        payload (Dict[str, Any]): The GitHub webhook payload
    """
    try:
        bot = await get_bot()
        
        # Create appropriate embed based on event type
        embed = await create_event_embed(event_type, payload)
        
        if embed:
            success = await bot.send_github_notification(embed)
            if not success:
                logger.error(f"Failed to send notification for {event_type} event")
        else:
            logger.warning(f"No embed created for {event_type} event")
            
    except Exception as e:
        logger.error(f"Error processing {event_type} event: {e}")
        # Try to send error notification to Discord
        try:
            bot = await get_bot()
            await bot.send_error_notification(str(e), event_type)
        except Exception as notify_error:
            logger.error(f"Failed to send error notification: {notify_error}")


async def create_event_embed(event_type: str, payload: Dict[str, Any]) -> Optional[discord.Embed]:
    """
    Create a Discord embed based on the GitHub event type and payload.
    
    Args:
        event_type (str): The type of GitHub event
        payload (Dict[str, Any]): The GitHub webhook payload
        
    Returns:
        Optional[discord.Embed]: The formatted embed or None if event type is not supported
    """
    try:
        if event_type == "push":
            return await create_push_embed(payload)
        elif event_type == "pull_request":
            return await create_pull_request_embed(payload)
        elif event_type == "issues":
            return await create_issue_embed(payload)
        elif event_type == "release":
            return await create_release_embed(payload)
        elif event_type == "create":
            return await create_create_embed(payload)
        elif event_type == "delete":
            return await create_delete_embed(payload)
        else:
            logger.info(f"Unsupported event type: {event_type}")
            return None
            
    except Exception as e:
        logger.error(f"Error creating embed for {event_type}: {e}")
        return None


async def create_push_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for push events.
    
    Args:
        payload (Dict[str, Any]): The GitHub push event payload
        
    Returns:
        discord.Embed: The formatted push event embed
    """
    repository = payload.get("repository", {})
    pusher = payload.get("pusher", {})
    commits = payload.get("commits", [])
    ref = payload.get("ref", "")
    compare_url = payload.get("compare", "")
    
    # Determine branch name
    branch = ref.replace("refs/heads/", "") if ref.startswith("refs/heads/") else ref
    
    # Create embed
    embed = discord.Embed(
        title=f"📝 New Push to {branch}",
        description=f"**{len(commits)} commit(s)** pushed to `{repository.get('name', 'Unknown')}`",
        color=0x28a745,  # Green color
        url=compare_url
    )
    
    # Add repository info
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add pusher info
    embed.add_field(
        name="Pushed by",
        value=pusher.get("name", "Unknown"),
        inline=True
    )
    
    # Add commit count
    embed.add_field(
        name="Commits",
        value=str(len(commits)),
        inline=True
    )
    
    # Add latest commit info if available
    if commits:
        latest_commit = commits[-1]
        commit_message = latest_commit.get("message", "No message")
        # Truncate long commit messages
        if len(commit_message) > 100:
            commit_message = commit_message[:97] + "..."
        
        embed.add_field(
            name="Latest Commit",
            value=f"[{commit_message}]({latest_commit.get('url', '#')})",
            inline=False
        )
    
    # Set author and timestamp
    embed.set_author(
        name=pusher.get("name", "Unknown"),
        icon_url=pusher.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Push Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


async def create_pull_request_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for pull request events.
    
    Args:
        payload (Dict[str, Any]): The GitHub pull request event payload
        
    Returns:
        discord.Embed: The formatted pull request event embed
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
    embed = discord.Embed(
        title=f"🔀 Pull Request {action.title()}",
        description=f"**{pr.get('title', 'No title')}**",
        color=color,
        url=pr.get("html_url", "#")
    )
    
    # Add PR number and status
    embed.add_field(
        name="PR #" + str(pr.get("number", "?")),
        value=f"**{pr.get('state', 'unknown').title()}**",
        inline=True
    )
    
    # Add repository
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add author
    user = pr.get("user", {})
    embed.add_field(
        name="Author",
        value=user.get("login", "Unknown"),
        inline=True
    )
    
    # Add description if available
    body = pr.get("body", "")
    if body:
        # Truncate long descriptions
        if len(body) > 500:
            body = body[:497] + "..."
        embed.add_field(
            name="Description",
            value=body,
            inline=False
        )
    
    # Set author and timestamp
    embed.set_author(
        name=user.get("login", "Unknown"),
        icon_url=user.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Pull Request Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


async def create_issue_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for issue events.
    
    Args:
        payload (Dict[str, Any]): The GitHub issue event payload
        
    Returns:
        discord.Embed: The formatted issue event embed
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
    embed = discord.Embed(
        title=f"🐛 Issue {action.title()}",
        description=f"**{issue.get('title', 'No title')}**",
        color=color,
        url=issue.get("html_url", "#")
    )
    
    # Add issue number and state
    embed.add_field(
        name="Issue #" + str(issue.get("number", "?")),
        value=f"**{issue.get('state', 'unknown').title()}**",
        inline=True
    )
    
    # Add repository
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add author
    user = issue.get("user", {})
    embed.add_field(
        name="Author",
        value=user.get("login", "Unknown"),
        inline=True
    )
    
    # Add labels if available
    labels = issue.get("labels", [])
    if labels:
        label_names = [label.get("name", "") for label in labels[:5]]  # Limit to 5 labels
        embed.add_field(
            name="Labels",
            value=", ".join(label_names),
            inline=False
        )
    
    # Set author and timestamp
    embed.set_author(
        name=user.get("login", "Unknown"),
        icon_url=user.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Issue Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


async def create_release_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for release events.
    
    Args:
        payload (Dict[str, Any]): The GitHub release event payload
        
    Returns:
        discord.Embed: The formatted release event embed
    """
    release = payload.get("release", {})
    action = payload.get("action", "")
    repository = payload.get("repository", {})
    
    # Create embed
    embed = discord.Embed(
        title=f"🚀 Release {action.title()}",
        description=f"**{release.get('name', release.get('tag_name', 'No title'))}**",
        color=0xffc107,  # Yellow/Orange color
        url=release.get("html_url", "#")
    )
    
    # Add tag name
    embed.add_field(
        name="Tag",
        value=release.get("tag_name", "No tag"),
        inline=True
    )
    
    # Add repository
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add author
    author = release.get("author", {})
    embed.add_field(
        name="Author",
        value=author.get("login", "Unknown"),
        inline=True
    )
    
    # Add description if available
    body = release.get("body", "")
    if body:
        # Truncate long descriptions
        if len(body) > 500:
            body = body[:497] + "..."
        embed.add_field(
            name="Description",
            value=body,
            inline=False
        )
    
    # Set author and timestamp
    embed.set_author(
        name=author.get("login", "Unknown"),
        icon_url=author.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Release Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


async def create_create_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for create events (branches, tags).
    
    Args:
        payload (Dict[str, Any]): The GitHub create event payload
        
    Returns:
        discord.Embed: The formatted create event embed
    """
    ref = payload.get("ref", "")
    ref_type = payload.get("ref_type", "")
    repository = payload.get("repository", {})
    sender = payload.get("sender", {})
    
    # Determine emoji based on ref type
    emoji_map = {
        "branch": "🌿",
        "tag": "🏷️",
    }
    emoji = emoji_map.get(ref_type, "📝")
    
    # Create embed
    embed = discord.Embed(
        title=f"{emoji} {ref_type.title()} Created",
        description=f"**{ref}** created in `{repository.get('name', 'Unknown')}`",
        color=0x17a2b8,  # Blue color
        url=repository.get("html_url", "#")
    )
    
    # Add repository
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add creator
    embed.add_field(
        name="Created by",
        value=sender.get("login", "Unknown"),
        inline=True
    )
    
    # Set author and timestamp
    embed.set_author(
        name=sender.get("login", "Unknown"),
        icon_url=sender.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Create Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


async def create_delete_embed(payload: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for delete events (branches, tags).
    
    Args:
        payload (Dict[str, Any]): The GitHub delete event payload
        
    Returns:
        discord.Embed: The formatted delete event embed
    """
    ref = payload.get("ref", "")
    ref_type = payload.get("ref_type", "")
    repository = payload.get("repository", {})
    sender = payload.get("sender", {})
    
    # Determine emoji based on ref type
    emoji_map = {
        "branch": "🗑️",
        "tag": "🗑️",
    }
    emoji = emoji_map.get(ref_type, "🗑️")
    
    # Create embed
    embed = discord.Embed(
        title=f"{emoji} {ref_type.title()} Deleted",
        description=f"**{ref}** deleted from `{repository.get('name', 'Unknown')}`",
        color=0xdc3545,  # Red color
        url=repository.get("html_url", "#")
    )
    
    # Add repository
    embed.add_field(
        name="Repository",
        value=f"[{repository.get('full_name', 'Unknown')}]({repository.get('html_url', '#')})",
        inline=True
    )
    
    # Add deleter
    embed.add_field(
        name="Deleted by",
        value=sender.get("login", "Unknown"),
        inline=True
    )
    
    # Set author and timestamp
    embed.set_author(
        name=sender.get("login", "Unknown"),
        icon_url=sender.get("avatar_url", "")
    )
    embed.set_footer(text="Patchy - GitHub Delete Event")
    embed.timestamp = discord.utils.utcnow()
    
    return embed


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Patchy - GitHub Discord Webhook Bot is running!", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "Patchy - GitHub Discord Webhook Bot",
        "version": "1.0.0"
    }


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Main webhook endpoint for receiving GitHub events.
    
    This endpoint receives GitHub webhook events, validates the signature,
    and processes the event in the background.
    """
    try:
        # Get the raw body for signature verification
        body = await request.body()
        
        # Get headers
        signature = request.headers.get("X-Hub-Signature-256", "")
        event_type = request.headers.get("X-GitHub-Event", "")
        
        # Verify signature
        if not verify_github_signature(body, signature):
            logger.warning("Invalid GitHub webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse JSON payload
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Log the event
        logger.info(f"Received {event_type} event from GitHub")
        
        # Process the event in the background
        background_tasks.add_task(process_github_event, event_type, payload)
        
        return {"message": "Event received and queued for processing", "event_type": event_type}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in webhook endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler with logging."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {exc} - {request.url}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500}
    )
