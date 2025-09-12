# Local Development Helper Script for Patchy Discord Bot
# This script provides easy commands for local webhook testing

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$EventType = "push",
    
    [string]$Url = "http://localhost:8000"
)

function Show-Help {
    Write-Host @"
🧪 PATCHY LOCAL TESTING UTILITY

Commands:
  .\local-dev.ps1 start          - Start the Discord bot
  .\local-dev.ps1 config         - Check configuration
  .\local-dev.ps1 test [event]   - Test webhook (events: push, pull_request, issues)
  .\local-dev.ps1 test-all       - Test all event types
  .\local-dev.ps1 ngrok          - Show ngrok setup instructions
  .\local-dev.ps1 help           - Show this help

Examples:
  .\local-dev.ps1 start
  .\local-dev.ps1 test push
  .\local-dev.ps1 test pull_request
  .\local-dev.ps1 config

For webhook testing with ngrok:
  1. Run: .\local-dev.ps1 start
  2. In another terminal: ngrok http 8000
  3. Configure GitHub webhook with ngrok URL
"@
}

function Start-Bot {
    Write-Host "🚀 Starting Patchy Discord Bot..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    python main.py
}

function Test-Configuration {
    Write-Host "🔧 Checking configuration..." -ForegroundColor Blue
    python local_test.py config
}

function Test-Webhook {
    param([string]$Event)
    Write-Host "🧪 Testing webhook with event: $Event" -ForegroundColor Blue
    python local_test.py test $Event $Url
}

function Test-AllWebhooks {
    Write-Host "🧪 Testing all webhook events..." -ForegroundColor Blue
    python local_test.py test-all $Url
}

function Show-NgrokInstructions {
    Write-Host @"
🌐 NGROK SETUP FOR LOCAL WEBHOOK TESTING

Step 1: Install ngrok
  - Go to https://ngrok.com and create account
  - Download ngrok.exe for Windows
  - Place in this directory or add to PATH

Step 2: Start your bot (in this terminal)
  .\local-dev.ps1 start

Step 3: Start ngrok (in new terminal)
  ngrok http 8000

Step 4: Configure GitHub webhook
  - Repository → Settings → Webhooks → Add webhook
  - URL: https://YOUR-SUBDOMAIN.ngrok-free.app/webhook
  - Content type: application/json
  - Secret: Your GITHUB_WEBHOOK_SECRET from .env
  - Events: Select push, pull requests, issues

Step 5: Test
  - Make a commit or open a PR
  - Check Discord for notifications
  - Monitor requests at http://localhost:4040

💡 Pro Tips:
  - Keep ngrok terminal open to see the public URL
  - Use ngrok web interface (localhost:4040) to debug
  - Test locally first with: .\local-dev.ps1 test push
"@ -ForegroundColor Cyan
}

# Main script logic
switch ($Command.ToLower()) {
    "start" { Start-Bot }
    "config" { Test-Configuration }
    "test" { Test-Webhook -Event $EventType }
    "test-all" { Test-AllWebhooks }
    "ngrok" { Show-NgrokInstructions }
    "help" { Show-Help }
    "" { Show-Help }
    default { 
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}