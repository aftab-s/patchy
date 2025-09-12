from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        health_data = {
            "status": "healthy",
            "service": "Patchy - GitHub Discord Webhook Bot",
            "version": "1.0.0",
            "platform": "Vercel Serverless",
            "environment": {
                "discord_token_configured": bool(os.getenv("DISCORD_TOKEN")),
                "discord_channel_configured": bool(os.getenv("DISCORD_CHANNEL_ID")),
                "github_secret_configured": bool(os.getenv("GITHUB_WEBHOOK_SECRET"))
            }
        }
        
        self.wfile.write(json.dumps(health_data, indent=2).encode())
