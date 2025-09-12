"""
Health check endpoint for Vercel deployment.

This module provides health check endpoints for monitoring the Vercel deployment.
"""

import os
from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    """
    Health check handler for Vercel serverless functions.
    
    Provides basic health check and detailed status information.
    """
    
    def do_GET(self):
        """
        Handle GET requests for health checks.
        
        Returns health status and configuration information.
        """
        try:
            # Basic health check
            if self.path == '/health' or self.path == '/':
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
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = json.dumps(health_data, indent=2)
                self.wfile.write(response.encode('utf-8'))
                
            else:
                # 404 for other paths
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "error": "Not Found",
                    "message": "The requested endpoint was not found",
                    "available_endpoints": ["/", "/health"]
                }
                
                response = json.dumps(error_response, indent=2)
                self.wfile.write(response.encode('utf-8'))
                
        except Exception as e:
            # Handle any errors
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "error": "Internal Server Error",
                "message": str(e)
            }
            
            response = json.dumps(error_response, indent=2)
            self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """
        Override log_message to reduce noise in Vercel logs.
        
        Args:
            format: Log message format
            *args: Log message arguments
        """
        # Only log errors and warnings, not normal requests
        if "error" in format.lower() or "warning" in format.lower():
            super().log_message(format, *args)
