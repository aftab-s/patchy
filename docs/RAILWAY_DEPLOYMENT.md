# 🚀 Railway Deployment Guide

> **Status**: ✅ **LIVE & OPERATIONAL** - Your bot is successfully deployed!

## � Table of Contents

1. [Deployment Status](#deployment-status)
2. [Quick Setup](#quick-setup)
3. [GitHub Webhook Configuration](#github-webhook-configuration)
4. [Testing Your Deployment](#testing-your-deployment)
5. [Environment Variables](#environment-variables)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Updates & Redeployment](#updates--redeployment)
9. [Advanced Configuration](#advanced-configuration)

---

## 🎯 Deployment Status

### ✅ Live Application
- **🌍 Railway Endpoint**: `https://web-production-13df.up.railway.app/`
- **🏥 Health Check**: `https://web-production-13df.up.railway.app/health` - ✅ **Healthy**
- **🪝 Webhook Endpoint**: `https://web-production-13df.up.railway.app/webhook`
- **📊 Status**: **OPERATIONAL**

### 📈 Application Info
```
🔧 Platform: Railway  
🐍 Runtime: Python 3.11
🌍 Region: United States
⚡ Build: Auto-deploy from GitHub
🔄 Status: Running
📦 Memory: 512MB allocated
```

---

## ⚡ Quick Setup

If you're setting up from scratch or need to redeploy:

### 🚀 Option 1: One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/patchy-discord-bot)

### 🔧 Option 2: Manual Deployment

1. **Connect GitHub Repository**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `patchy-discord-bot` repository

2. **Configure Environment Variables** (see [Environment Variables](#environment-variables))

3. **Deploy**:
   - Railway will automatically detect Python and deploy
   - Build process will install dependencies from `requirements.txt`
   - Application starts with `python main.py`

---

## � GitHub Webhook Configuration

### 📝 Step-by-Step Webhook Setup

1. **📂 Go to Your GitHub Repository**
   - Navigate to your repository on GitHub
   - Click on **Settings** tab (repository settings, not account settings)

2. **🪝 Access Webhooks**  
   - In the left sidebar, click **Webhooks**
   - Click **Add webhook** button

3. **⚙️ Configure Webhook Settings**:
   ```
   📡 Payload URL: https://web-production-13df.up.railway.app/webhook
   📋 Content type: application/json  
   🔐 Secret: [Your GITHUB_WEBHOOK_SECRET]
   
   🎯 Which events would you like to trigger this webhook?
   ☑️ Pushes                    # New commits
   ☑️ Pull requests            # PR opened/closed/merged
   ☑️ Issues                   # Issues created/closed
   ☑️ Issue comments          # Comments on issues
   ☑️ Pull request reviews    # PR reviews
   ☑️ Releases                # New releases (optional)
   
   ☑️ Active (webhook is active)
   ```

4. **✅ Save Webhook**
   - Click **Add webhook**  
   - GitHub will send a test ping - you should see a ✅ green checkmark

### 🎯 Event Types Explained

| Event | When It Triggers | Discord Notification |
|-------|------------------|---------------------|
| **Pushes** | New commits pushed | Shows commit details, author, changes |
| **Pull Requests** | PR opened/merged/closed | Shows PR title, author, status |
| **Issues** | Issue created/closed | Shows issue title, author, labels |
| **Issue Comments** | Comments on issues | Shows comment author, issue link |
| **PR Reviews** | Code reviews submitted | Shows reviewer, approval status |
| **Releases** | New version released | Shows release notes, version tag |

---

## 🧪 Testing Your Deployment

### 🎯 Method 1: Automated Test Script

Use the included test script:

```powershell
# Test your Railway deployment with real webhook simulation
python dev-tools/test_railway.py
```

**Expected Output**:
```
🚀 Testing Railway deployment...
✅ Health check passed
🧪 Testing webhook endpoint...
✅ Webhook test successful!
📱 Check your Discord channel for test notification
```

### 🎯 Method 2: Real GitHub Event

Make a real change to test the complete workflow:

```powershell
# Create a test commit
echo "Testing webhook: $(Get-Date)" >> test_webhook.md
git add test_webhook.md
git commit -m "Test Railway webhook deployment"
git push
```

**What Should Happen**:
1. ⚡ GitHub sends webhook to Railway
2. 🤖 Railway processes webhook  
3. 💬 Discord receives notification
4. ✅ You see the commit notification in Discord

### 🎯 Method 3: GitHub Webhook Test

1. **Go to Repository Settings → Webhooks**
2. **Click on your webhook URL**
3. **Scroll to "Recent Deliveries"**
4. **Click "Redeliver"** on any previous delivery
5. **Check Discord** for the notification

### 🎯 Method 4: Manual Health Check

```powershell
# Test the health endpoint
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"

# Expected response:
# StatusCode: 200
# Content: {"status":"healthy","timestamp":"2025-09-13T..."}
```

---

## 🌍 Environment Variables

### 🔑 Required Variables

These **must** be configured in your Railway deployment:

| Variable | Description | Example | Status |
|----------|-------------|---------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | `MTIzNDU2Nzg5MA.GhI...` | ✅ Configured |
| `DISCORD_CHANNEL_ID` | Target Discord channel ID | `1234567890123456789` | ✅ Configured |
| `GITHUB_WEBHOOK_SECRET` | GitHub webhook secret for security | `my-secure-webhook-secret` | ✅ Configured |

### ⚙️ Optional Variables

These have sensible defaults but can be customized:

| Variable | Default | Description | Railway Override |
|----------|---------|-------------|------------------|
| `HOST` | `0.0.0.0` | Server host address | ✅ Auto-configured |
| `PORT` | `8000` | Server port | ✅ Auto-assigned by Railway |
| `DEBUG` | `false` | Enable debug logging | Recommend `false` in production |
| `LOG_LEVEL` | `INFO` | Logging verbosity | `INFO` or `WARNING` for production |

### 🔧 Setting Environment Variables in Railway

#### Method 1: Railway Dashboard
1. Go to your project in Railway dashboard
2. Click **Variables** tab  
3. Add each variable:
   - Click **New Variable**
   - Enter variable name and value
   - Click **Add**

#### Method 2: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link to your project
railway login
railway link

# Set environment variables
railway variables set DISCORD_TOKEN="your_token_here"
railway variables set DISCORD_CHANNEL_ID="your_channel_id"  
railway variables set GITHUB_WEBHOOK_SECRET="your_secret"
```

#### Method 3: Import from File
```bash
# Create railway.env file with your variables
DISCORD_TOKEN=your_token_here
DISCORD_CHANNEL_ID=your_channel_id
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# Import to Railway
railway variables set --from-file railway.env
```

### 🔒 Security Best Practices

- ✅ **Never commit secrets** to your repository
- ✅ **Use different secrets** for development vs production  
- ✅ **Rotate secrets regularly** (at least every 6 months)
- ✅ **Use strong webhook secrets** (32+ characters, mix of letters/numbers/symbols)
- ✅ **Monitor failed webhook attempts** for potential security issues

### 📋 Environment Variables Checklist

```powershell
# Verify all required variables are set
railway variables

# Should show:
# DISCORD_TOKEN=MTIzNDU2Nzg5... (truncated for security)
# DISCORD_CHANNEL_ID=1234567890123456789
# GITHUB_WEBHOOK_SECRET=****************
```

---

## 📊 Monitoring & Maintenance

### 🏥 Health Monitoring

#### Automated Health Checks
Railway automatically monitors your application health:

```powershell
# Manual health check
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"

# Expected healthy response:
# {
#   "status": "healthy",
#   "timestamp": "2025-09-13T12:34:56Z", 
#   "uptime": "2 hours, 15 minutes"
# }
```

#### Railway Dashboard Monitoring
Access your [Railway Dashboard](https://railway.app/dashboard) to monitor:
- 📈 **CPU & Memory Usage**: Resource consumption graphs
- 📊 **Request Metrics**: HTTP request volume and response times  
- 🔄 **Deployment History**: Build logs and deployment timeline
- ⚠️ **Error Logs**: Application errors and crashes

### 🪝 Webhook Monitoring

#### GitHub Webhook Status
1. **Go to Repository Settings → Webhooks**
2. **Check webhook status**:
   - ✅ **Green checkmark**: Webhook working correctly
   - ❌ **Red X**: Webhook delivery failing
   - 🟡 **Yellow warning**: Intermittent issues

3. **Review Recent Deliveries**:
   - Click webhook URL to see delivery history
   - Check response codes (should be 200)
   - Review response times (should be <5 seconds)

#### Discord Notification Monitoring
Monitor your Discord channel for:
- ✅ **Consistent notifications** for all repository events
- 🎨 **Proper message formatting** with embeds and colors
- ⏱️ **Timely delivery** (within 10 seconds of GitHub event)
- 📝 **Complete information** (commit details, author, links)

### 📊 Application Metrics

#### Railway Metrics Dashboard
Key metrics to monitor:

| Metric | Healthy Range | Action Required |
|--------|---------------|-----------------|
| **CPU Usage** | < 50% | Scale up if consistently >80% |
| **Memory Usage** | < 80% | Investigate memory leaks if >90% |
| **Response Time** | < 2 seconds | Optimize code if >5 seconds |
| **Error Rate** | < 1% | Debug issues if >5% |
| **Uptime** | > 99% | Investigate if <95% |

#### Log Monitoring
```bash
# View Railway logs via CLI
railway logs

# Filter for errors
railway logs | grep ERROR

# Monitor webhook processing
railway logs | grep "webhook"
```

### 🚨 Setting Up Alerts

#### Railway Alerts
1. Go to Railway project settings
2. Enable notifications for:
   - Deployment failures
   - High resource usage  
   - Application crashes
   - Extended downtime

#### External Monitoring
Consider setting up external monitoring:

```powershell
# Simple PowerShell monitoring script
function Test-BotHealth {
    try {
        $response = Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Bot is healthy" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Bot health check failed!" -ForegroundColor Red
        # Send alert (email, Slack, etc.)
    }
}

# Run every 5 minutes
while ($true) {
    Test-BotHealth
    Start-Sleep 300
}
```

---

## � Troubleshooting

### ❓ Common Issues & Solutions

#### 🔴 Webhook Delivery Fails (HTTP 500/400)
**Symptoms**: GitHub shows red X, error responses from Railway

```powershell
# 1. Check Railway logs for errors
railway logs --tail=50

# 2. Verify environment variables are set
railway variables

# 3. Test health endpoint
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"
```

**Common Causes & Solutions**:
- **Missing environment variables**: Add required variables in Railway dashboard
- **Invalid Discord token**: Regenerate token in Discord Developer Portal  
- **Wrong channel ID**: Right-click Discord channel → Copy ID
- **Application crash**: Check Railway logs for Python errors

#### 🔴 Discord Notifications Not Appearing
**Symptoms**: Webhook received successfully but no Discord message

```powershell
# Debug Discord connection
# Check Railway logs for Discord-related errors
railway logs | Select-String "discord"
```

**Common Causes & Solutions**:

| Problem | Solution |
|---------|----------|
| **Invalid Discord token** | Regenerate token in Discord Developer Portal |
| **Wrong channel ID** | Get channel ID: Right-click channel → Copy ID |
| **Missing bot permissions** | Add "Send Messages" and "Embed Links" permissions |
| **Bot not in server** | Re-invite bot with correct permissions |
| **Rate limited** | Wait 1 hour, then spread out webhook events |

#### 🔴 Signature Verification Fails  
**Symptoms**: Railway logs show "Invalid signature" errors

```powershell
# 1. Verify webhook secret matches exactly
# Check Railway variables
railway variables | Select-String "WEBHOOK_SECRET"

# 2. Check GitHub webhook settings
# Repository Settings → Webhooks → [Your webhook]
# Ensure secret field matches Railway variable
```

**Common Causes**:
- Different secrets in GitHub vs Railway
- Extra spaces/newlines in secret  
- Secret not properly saved in Railway

#### 🔴 Railway App Not Responding
**Symptoms**: 502/503 errors, timeouts

```powershell
# 1. Check deployment status
railway status

# 2. View recent deployments  
railway deployments

# 3. Check for build failures
railway logs --deployment [deployment-id]
```

**Common Causes**:
- **Build failure**: Missing dependencies in `requirements.txt`
- **Port binding issues**: Railway auto-assigns PORT variable
- **Memory limit exceeded**: Upgrade Railway plan if needed
- **Startup crash**: Check logs for Python errors during startup

### 🛠️ Debugging Commands

```powershell
# Railway CLI debugging toolkit

# View current status
railway status

# Real-time logs
railway logs --follow

# View specific deployment logs
railway deployments
railway logs --deployment <deployment-id>

# Check environment variables
railway variables

# Test local connection to Railway
Test-NetConnection web-production-13df.up.railway.app -Port 443

# Manual webhook test
$headers = @{ "X-GitHub-Event" = "ping"; "Content-Type" = "application/json" }
Invoke-RestMethod -Uri "https://web-production-13df.up.railway.app/webhook" -Method POST -Headers $headers -Body "{}"
```

### 🩺 Health Check Troubleshooting

#### Health Endpoint Not Responding
```powershell
# Test different endpoints
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/"        # Root endpoint
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"  # Health check
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/docs"    # API docs (if enabled)
```

#### Intermittent Health Check Failures
- **Cold starts**: Railway may pause apps on free tier
- **Resource limits**: Check memory/CPU usage in Railway dashboard  
- **Network issues**: Test from different locations/networks

### 📞 Getting Help

#### Railway Support Resources
- **📚 Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **💬 Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **🐛 Railway GitHub Issues**: [github.com/railwayapp/railway-issues](https://github.com/railwayapp/railway-issues)

#### Debug Information to Collect
When seeking help, provide:

```powershell
# Collect debug information
Write-Host "=== Railway Debug Info ==="
railway status
railway variables
railway logs --tail=20

Write-Host "`n=== Health Check ==="
try { Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health" } catch { $_.Exception.Message }

Write-Host "`n=== GitHub Webhook Status ==="
# Check GitHub webhook delivery logs manually
```

---

## 🔄 Updates & Redeployment

### 🚀 Automatic Deployment

Railway automatically redeploys when you push changes to your connected GitHub repository:

```powershell
# Make changes to your code
# Edit discord_bot.py, webhook_server.py, etc.

# Commit and push changes  
git add .
git commit -m "Update bot functionality"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Builds the new version
# 3. Deploys to production
# 4. Health checks the deployment
```

### ⚡ Manual Deployment

#### Via Railway CLI
```bash
# Deploy current local code
railway up

# Deploy specific branch
railway up --branch feature/new-webhooks

# Force redeploy without changes
railway redeploy
```

#### Via Railway Dashboard
1. Go to your Railway project
2. Click **Deployments** tab
3. Click **Deploy** button
4. Monitor build logs in real-time

### 📊 Deployment Process

Railway follows this deployment process:

```
1. 📥 Code Detection    # Detects changes in GitHub
2. 🏗️ Build Process     # Installs dependencies, runs build
3. 🧪 Health Checks     # Verifies app starts correctly  
4. 🔄 Rolling Deploy    # Replaces old version with new
5. 📊 Monitoring        # Tracks deployment success
```

### 🔍 Deployment Verification

After each deployment, verify everything works:

```powershell
# 1. Check health endpoint
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"

# 2. Test webhook with a commit
git commit --allow-empty -m "Test deployment webhook"
git push

# 3. Verify Discord notification appears

# 4. Check Railway logs for any errors
railway logs --tail=20
```

### �️ Rollback Strategy

If a deployment fails:

#### Automatic Rollback
Railway automatically rolls back if:
- Application fails to start
- Health checks fail repeatedly  
- Critical errors detected

#### Manual Rollback
```bash
# View deployment history
railway deployments

# Rollback to specific deployment  
railway rollback <deployment-id>

# Or via Railway Dashboard:
# 1. Go to Deployments tab
# 2. Click on previous successful deployment
# 3. Click "Redeploy" button
```

---

## ⚙️ Advanced Configuration

### 🔧 Railway Configuration File

Create `railway.json` in your project root for advanced settings:

```json
{
  "$schema": "https://railway.app/railway.schema.json", 
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  },
  "build": {
    "buildCommand": "pip install -r requirements.txt"
  }
}
```

### 📦 Custom Build Process

#### Custom Start Command
```json
{
  "deploy": {
    "startCommand": "python main.py --host 0.0.0.0 --port $PORT"
  }
}
```

#### Build Optimizations
```json
{
  "build": {
    "buildCommand": "pip install --no-cache-dir -r requirements.txt"
  }
}
```

### 🌍 Environment-Specific Deployments

#### Staging Environment
1. Create staging branch: `git checkout -b staging`
2. Deploy staging: Connect Railway to staging branch
3. Use staging webhook URL for testing

#### Production Environment  
1. Keep production on `main` branch
2. Use production webhook URL
3. Implement proper release workflow

### 📊 Resource Management

#### Memory Optimization
```python
# In main.py - optimize for Railway
import uvicorn
import os

if __name__ == "__main__":
    # Railway-optimized settings
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        workers=1,  # Single worker for Railway
        loop="uvloop",  # Performance optimization
        http="httptools"  # HTTP performance
    )
```

#### Resource Monitoring
```bash
# Monitor resource usage
railway metrics

# View resource limits  
railway info
```

---

## 🎯 Next Steps

### 🚀 Enhance Your Bot

1. **📈 Add More Webhook Events**
   ```python
   # Add support for:
   - Repository stars/forks
   - Wiki updates  
   - Security alerts
   - Dependabot updates
   ```

2. **🎨 Customize Discord Messages**
   ```python
   # Add features:
   - Custom embed colors per event type
   - Emoji reactions
   - Thread creation for discussions
   - Role mentions for important events
   ```

3. **🔍 Add Filtering**
   ```python
   # Filter webhooks by:
   - Branch names (only main/production)  
   - Author names (ignore bot commits)
   - File paths (only specific directories)
   - Keywords in commit messages
   ```

### 📊 Production Improvements

1. **🔐 Security Enhancements**
   - Rate limiting for webhook endpoints
   - IP allowlisting for GitHub IPs
   - Enhanced logging for security events
   - Regular secret rotation

2. **📈 Monitoring & Observability**
   - Application performance monitoring (APM)
   - Custom metrics and dashboards
   - Alert integrations (email, Slack, PagerDuty)
   - Log aggregation and analysis

3. **🔄 CI/CD Pipeline** 
   - Automated testing before deployment
   - Staging environment for testing
   - Blue-green deployments
   - Automated rollback on failures

---

## 📚 Related Documentation

- **🧪 Local Testing**: [`docs/LOCAL_TESTING.md`](./LOCAL_TESTING.md) - Test webhooks locally before deployment
- **🐳 Docker Deployment**: [`docs/DOCKER.md`](./DOCKER.md) - Containerized deployment options  
- **☁️ Vercel Deployment**: [`docs/VERCEL_DEPLOYMENT.md`](./VERCEL_DEPLOYMENT.md) - Serverless alternative
- **🔧 Environment Variables**: [`docs/DOCKER_ENV.md`](./DOCKER_ENV.md) - Managing environment configuration

---

> **🎉 Congratulations!** Your Patchy Discord Bot is successfully deployed on Railway and ready to notify your Discord server about all GitHub activities!