# 🧪 Local Webhook Testing Guide

> **Quick Start**: Use `ngrok http 8000` to make your local bot accessible to GitHub webhooks

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Method 1: ngrok (Recommended)](#method-1-ngrok-recommended)
4. [Method 2: LocalTunnel (Alternative)](#method-2-localtunnel-alternative)
5. [Method 3: Manual Testing](#method-3-manual-testing)
6. [Method 4: Docker Testing](#method-4-docker-testing)
7. [Development Workflow](#development-workflow)
8. [Testing Checklist](#testing-checklist)
9. [Troubleshooting](#troubleshooting)
10. [Production Transition](#production-transition)

---

## 🎯 Overview

Testing GitHub webhooks locally requires making your local application accessible from the internet, since GitHub needs to send HTTP requests to your webhook endpoint.

### 🏗️ Testing Architecture

```
GitHub → Internet → Tunnel Service → Your Local Bot
                      (ngrok)         (localhost:8000)
                         │
                         ▼
                   Discord Channel
```

### ✨ Why Local Testing?

- 🚀 **Faster Development**: Test changes immediately without deployment
- 🐛 **Easy Debugging**: Full access to logs and debugging tools
- 💰 **Cost Effective**: No cloud resources needed for development
- 🔄 **Iteration Speed**: Quick feedback loop for webhook development

---

## 🔧 Prerequisites

Before starting local testing, ensure you have:

- ✅ **Python 3.11+** installed
- ✅ **Discord bot** created and token obtained
- ✅ **GitHub repository** with webhook events to test
- ✅ **Environment variables** configured in `.env` file
- ✅ **Bot dependencies** installed: `pip install -r requirements.txt`
- ✅ **Discord bot** added to your server with proper permissions

### 📋 Required Environment Variables

Create or verify your `.env` file contains:

```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here

# GitHub Configuration
GITHUB_WEBHOOK_SECRET=your_secure_webhook_secret_here

# Optional - Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
HOST=0.0.0.0
PORT=8000
```

---

## 🚀 Method 1: ngrok (Recommended)

**Best for**: Most reliable, professional tunneling service with excellent debugging tools

### 📦 Step 1: Install ngrok

1. **Sign up for ngrok**: Go to [ngrok.com](https://ngrok.com) and create a free account
2. **Download ngrok**: Download ngrok for Windows  
3. **Install ngrok**: Extract to a folder in your PATH or project directory
4. **Authenticate**: Run `ngrok config add-authtoken YOUR_AUTHTOKEN`

### ⚡ Step 2: Start Your Local Application

```powershell
# Terminal 1: Start your Discord bot
cd "s:\Env0-Lite\discord-bot"
python main.py
```

You should see output like:
```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 🌐 Step 3: Create ngrok Tunnel

```powershell
# Terminal 2: Create tunnel to your local app
ngrok http 8000
```

**Expected Output**:
```
ngrok                                                          
                                                               
Session Status                online                           
Account                       your-email@example.com          
Version                       3.x.x                           
Region                        United States (us)              
Latency                       45ms                            
Web Interface                 http://127.0.0.1:4040          
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90  
                              0       0       0.00    0.00    0.00    0.00 
```

**📝 Important**: Copy the `https://abc123.ngrok-free.app` URL - this is your webhook endpoint!

### 🔧 Step 4: Configure GitHub Webhook

1. **Go to your GitHub repository**
2. **Navigate**: Settings → Webhooks → Add webhook
3. **Configure webhook**:
   ```
   Payload URL: https://abc123.ngrok-free.app/webhook
   Content type: application/json
   Secret: [Your GITHUB_WEBHOOK_SECRET from .env]
   
   Which events would you like to trigger this webhook?
   ☑️ Pushes
   ☑️ Pull requests
   ☑️ Issues
   ☑️ Issue comments
   ☑️ Pull request reviews
   
   ☑️ Active
   ```
4. **Click "Add webhook"**

### 🧪 Step 5: Test the Webhook

#### **Option A: Make a Real Commit**
```powershell
# Make a test change to your repository
echo "Test commit for webhook" >> test.txt
git add test.txt
git commit -m "Test webhook notification"
git push
```

#### **Option B: GitHub Webhook Test**
1. Go to Settings → Webhooks → [Your webhook]  
2. Click "Recent Deliveries"
3. Click "Redeliver" on any previous delivery

#### **Option C: Monitor in Real-Time**
- **Bot Logs**: Watch Terminal 1 for webhook processing
- **ngrok Web UI**: Open `http://localhost:4040` for request details
- **Discord Channel**: Check for notification messages

### 📊 ngrok Web Interface

Access `http://localhost:4040` for:
- 📋 **Request History**: All webhook requests received
- 🔍 **Request Details**: Headers, payload, response
- 🔄 **Replay Requests**: Re-send requests for testing
- 📈 **Performance Stats**: Timing and status codes

---

## 🌐 Method 2: LocalTunnel (Alternative)

**Best for**: npm users, quick testing, no account required

### 📦 Installation & Setup

```powershell
# Install LocalTunnel globally via npm
npm install -g localtunnel

# Start your Discord bot
python main.py

# In another terminal, create tunnel with custom subdomain
lt --port 8000 --subdomain patchy-bot-yourname
```

### 🔗 Configuration

Use `https://patchy-bot-yourname.loca.lt/webhook` as your GitHub webhook URL

### ⚠️ Limitations
- Less reliable than ngrok
- Subdomain availability not guaranteed
- No built-in web interface for debugging
- May require CAPTCHA verification

---

## 🔧 Method 3: Manual Testing

**Best for**: Testing webhook processing without real GitHub events

### 🧪 PowerShell Test Script

Create `test_local_webhook.ps1`:

```powershell
# Test your local webhook endpoint with simulated GitHub data

$headers = @{
    "Content-Type" = "application/json"
    "X-GitHub-Event" = "push"
    "X-Hub-Signature-256" = "sha256=test-signature"  # Replace with real signature
    "User-Agent" = "GitHub-Hookshot/abc123"
}

$testPayload = @{
    repository = @{
        name = "test-repo"
        full_name = "your-username/test-repo"
        html_url = "https://github.com/your-username/test-repo"
    }
    pusher = @{
        name = "Test User"
        email = "test@example.com"
    }
    commits = @(
        @{
            id = "abc123def456"
            message = "Test commit for local webhook testing"
            author = @{
                name = "Test Author"
                email = "author@example.com"
            }
            url = "https://github.com/your-username/test-repo/commit/abc123def456"
            timestamp = "2025-09-13T12:00:00Z"
        }
    )
    compare = "https://github.com/your-username/test-repo/compare/old...new"
} | ConvertTo-Json -Depth 10

# Send test webhook
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/webhook" -Method POST -Headers $headers -Body $testPayload
    Write-Host "✅ Webhook test successful!" -ForegroundColor Green
    Write-Host "Response: $response" -ForegroundColor Yellow
} catch {
    Write-Host "❌ Webhook test failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

### 🏃‍♂️ Run Test Script

```powershell
# Make script executable and run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
./test_local_webhook.ps1
```

### 📋 Alternative curl Testing

If you have curl available:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -H "X-Hub-Signature-256: sha256=your-calculated-signature" \
  -d @test_payload.json
```

---

## 🐳 Method 4: Docker Testing

**Best for**: Testing in containerized environment, production-like setup

### 🚀 Docker Compose Testing

```powershell
# Terminal 1: Start bot with Docker
docker-compose up --build

# Terminal 2: Create ngrok tunnel
ngrok http 8000
```

### 🔧 Manual Docker Testing

```powershell
# Build and run Docker container
docker build -t patchy-discord-bot .
docker run -p 8000:8000 --env-file .env patchy-discord-bot

# Then use ngrok to tunnel to localhost:8000
ngrok http 8000
```

### 📊 Docker Benefits
- ✅ **Production Parity**: Same environment as deployment  
- ✅ **Dependency Isolation**: Clean Python environment
- ✅ **Port Management**: Consistent port mapping
- ❌ **Slower Iteration**: Requires rebuild for code changes

---

## 💼 Development Workflow

### 🏗️ Recommended Setup

**Terminal Layout**:
```
┌─────────────────┬─────────────────┬─────────────────┐
│   Terminal 1    │   Terminal 2    │   Terminal 3    │
│                 │                 │                 │
│  Discord Bot    │  ngrok Tunnel   │  Git Commands   │  
│  python main.py │  ngrok http 8000│  git commit     │
│                 │                 │  git push       │
└─────────────────┴─────────────────┴─────────────────┘
```

### 🔄 Development Cycle

1. **🚀 Start Services**
   ```powershell
   # Terminal 1
   python main.py
   
   # Terminal 2  
   ngrok http 8000
   ```

2. **⚙️ Configure Webhook**
   - Copy ngrok URL from Terminal 2
   - Update GitHub webhook URL
   - Verify webhook is active

3. **🧪 Test Changes**
   ```powershell
   # Terminal 3
   git add .
   git commit -m "Test webhook changes"
   git push
   ```

4. **🔍 Monitor Results**
   - Check Terminal 1 for webhook processing logs
   - Check Discord channel for notifications
   - Check ngrok web UI (`http://localhost:4040`) for request details

### 📝 Environment Variables for Development

Add these to your `.env` file for enhanced debugging:

```env
# Enhanced logging for development
DEBUG=true
LOG_LEVEL=DEBUG

# Optional development tweaks
HOST=0.0.0.0
PORT=8000

# Your existing production variables
DISCORD_TOKEN=your_token
DISCORD_CHANNEL_ID=your_channel_id  
GITHUB_WEBHOOK_SECRET=your_secret
```

---

## ✅ Testing Checklist

Use this checklist before and during testing to ensure everything works properly:

### 🔧 Pre-Testing Setup
- [ ] **Local application running**: `python main.py` shows server started
- [ ] **Environment variables configured**: `.env` file exists with all required values
- [ ] **Discord bot permissions verified**: Bot can send messages and embeds
- [ ] **ngrok tunnel active**: Shows forwarding URL (e.g., `https://abc123.ngrok-free.app`)
- [ ] **GitHub webhook configured**: Payload URL points to ngrok tunnel + `/webhook`
- [ ] **Webhook secret matches**: GitHub secret equals `GITHUB_WEBHOOK_SECRET`

### 🧪 During Testing
- [ ] **Make test commit**: Push changes to repository
- [ ] **Check Discord notification**: Message appears in target channel
- [ ] **Review bot logs**: No errors in Terminal 1
- [ ] **Check ngrok logs**: Request appears in `http://localhost:4040`
- [ ] **Verify webhook delivery**: GitHub shows successful delivery (green checkmark)

### 🔍 Post-Testing Validation
- [ ] **Response codes**: GitHub webhook delivery shows HTTP 200
- [ ] **Message formatting**: Discord message shows expected content and embeds
- [ ] **Error handling**: Test with invalid payloads (should not crash bot)
- [ ] **Rate limiting**: Multiple quick commits handled gracefully
- [ ] **Security**: Webhook signature validation working

---

## 🔧 Troubleshooting

### ❓ Common Issues & Solutions

#### 🔴 "Webhook delivery failed"
**Symptoms**: GitHub shows red X, failed delivery

```powershell
# Check if local app is running  
# Look for this output:
# INFO: Uvicorn running on http://0.0.0.0:8000

# Verify ngrok tunnel is active
# Should show: Forwarding https://xxx.ngrok-free.app -> http://localhost:8000

# Test endpoint manually
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

**Common Causes**:
- Bot application not running
- ngrok tunnel disconnected  
- Wrong port (should be 8000)
- Firewall blocking connections

#### 🔴 "Discord notifications not appearing"  
**Symptoms**: Webhook received but no Discord message

```powershell
# Check Discord token and channel ID
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Token length:', len(os.getenv('DISCORD_TOKEN', '')))
print('Channel ID:', os.getenv('DISCORD_CHANNEL_ID', ''))
"

# Test Discord connection
python -c "
import discord
import os
from dotenv import load_dotenv
load_dotenv()
print('Testing Discord connection...')
# This will show if token is valid
"
```

**Common Causes**:  
- Invalid Discord token
- Wrong channel ID (try right-clicking channel → Copy ID)
- Missing bot permissions ("Send Messages", "Embed Links")
- Bot not added to Discord server

#### 🔴 "Signature verification fails"
**Symptoms**: Bot logs show signature mismatch errors

```powershell
# Verify webhook secret matches exactly
$githubSecret = "your_webhook_secret_here"
$envSecret = Get-Content .env | Select-String "GITHUB_WEBHOOK_SECRET"
Write-Host "GitHub: $githubSecret"
Write-Host "Environment: $envSecret"
```

**Common Causes**:
- Extra spaces or newlines in secret
- Different secrets between GitHub and `.env`
- Secret not properly URL-encoded

#### 🔴 "ngrok tunnel keeps disconnecting"
**Symptoms**: ngrok URL changes frequently

```powershell
# ngrok Free Plan Limitations:
# - Tunnel expires after 2 hours  
# - URL changes on restart
# - Limited concurrent tunnels

# Solutions:
# 1. Restart ngrok when needed
ngrok http 8000

# 2. Use persistent ngrok domain (paid plan)
ngrok http 8000 --domain=your-domain.ngrok.app

# 3. Update GitHub webhook URL when ngrok restarts
```

### 🛠️ Debugging Tools

#### 📊 ngrok Web Interface
Access `http://localhost:4040` for:
- Request history and payload inspection
- Response codes and timing
- Request replay functionality
- Traffic statistics

#### 📋 Application Logs
```powershell
# Enable verbose logging in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Monitor logs for webhook processing
python main.py | Tee-Object -FilePath webhook_logs.txt
```

#### 🔍 GitHub Webhook Logs
1. Go to repository Settings → Webhooks
2. Click on your webhook  
3. Check "Recent Deliveries" tab
4. Click individual deliveries to see request/response details

### 🧹 Reset Instructions

If everything breaks and you need to start fresh:

```powershell  
# 1. Stop all running processes
# Ctrl+C in terminals running python main.py and ngrok

# 2. Restart local application
python main.py

# 3. Restart ngrok (get new URL)  
ngrok http 8000

# 4. Update GitHub webhook URL with new ngrok URL

# 5. Test with a simple commit
git commit --allow-empty -m "Test webhook reset"
git push
```

---

## 🚀 Production Transition

Once your local testing is complete and working perfectly:

### 🌟 Next Steps

1. **🔄 Deploy to Production Platform**
   - **Railway**: Follow [`docs/RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md)
   - **Vercel**: Follow [`docs/VERCEL_DEPLOYMENT.md`](./VERCEL_DEPLOYMENT.md)  
   - **Docker**: Follow [`docs/DOCKER.md`](./DOCKER.md)

2. **📝 Update GitHub Webhook URL**
   ```
   # Change from ngrok URL:
   https://abc123.ngrok-free.app/webhook
   
   # To production URL:  
   https://your-app.railway.app/webhook
   ```

3. **🔒 Production Security**  
   - Use different webhook secrets for dev/production
   - Set up proper SSL certificates (automatic with cloud providers)
   - Configure monitoring and alerting
   - Set up log aggregation

4. **📊 Production Monitoring**
   - Health check endpoints
   - Webhook delivery monitoring
   - Discord message delivery tracking
   - Error rate monitoring

### 💡 Development Best Practices

1. **🔄 Use Different Webhooks**
   ```
   Development: https://abc123.ngrok-free.app/webhook  
   Production:  https://your-app.railway.app/webhook
   ```

2. **🌍 Environment Separation**  
   ```
   .env.development    # Local testing
   .env.production     # Live deployment
   ```

3. **📋 Testing Strategy**
   - Test locally with ngrok first
   - Deploy to staging environment  
   - Finally deploy to production
   - Always test webhook delivery after deployment

---

## 📚 Additional Resources

- **🐳 Docker Guide**: [`docs/DOCKER.md`](./DOCKER.md) - Containerized testing and deployment
- **⚡ Railway Deployment**: [`docs/RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md) - Production deployment guide
- **☁️ Vercel Deployment**: [`docs/VERCEL_DEPLOYMENT.md`](./VERCEL_DEPLOYMENT.md) - Serverless deployment option
- **🔧 Environment Variables**: [`docs/DOCKER_ENV.md`](./DOCKER_ENV.md) - Managing environment variables

---

> **🎉 Success!** Your local testing setup is complete! You can now develop and test webhook functionality with real-time feedback before deploying to production.