# ☁️ Vercel Serverless Deployment Guide

> **Serverless Discord Bot**: Deploy Patchy as serverless functions on Vercel's edge network

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Deployment Methods](#deployment-methods)
5. [Environment Configuration](#environment-configuration)  
6. [GitHub Webhook Setup](#github-webhook-setup)
7. [Testing & Verification](#testing--verification)
8. [Troubleshooting](#troubleshooting)
9. [Limitations & Considerations](#limitations--considerations)
10. [Advanced Configuration](#advanced-configuration)

---

## 🎯 Overview

Vercel deployment transforms your Discord bot into serverless functions that run on-demand. This approach is cost-effective and automatically scales with your webhook traffic.

### 🏗️ Serverless Architecture

```
GitHub Webhook → Vercel Edge Function → Discord API
                      ↓
               /api/webhook.py (Serverless Function)
               /api/health.py  (Health Check Function)
```

### ✨ Vercel Benefits

- 🚀 **Zero Cold Start**: Edge functions start instantly  
- 💰 **Cost Effective**: Pay only for actual usage
- 🌍 **Global CDN**: Fast response times worldwide
- 🔄 **Auto Scaling**: Handles traffic spikes automatically
- 📊 **Built-in Analytics**: Request metrics and performance monitoring

### ⚠️ Important Note

Vercel is designed for **stateless serverless functions**. The Discord bot connection cannot persist between requests, so each webhook creates a temporary Discord client connection.

---

## 🔧 Prerequisites

Before deploying to Vercel, ensure you have:

- ✅ **Vercel account** ([sign up free](https://vercel.com/signup))
- ✅ **Discord bot** created with token
- ✅ **GitHub repository** with your bot code
- ✅ **Node.js/npm** installed (for Vercel CLI)
- ✅ **Git** installed and configured

### 📦 Required Files

Your project should include these Vercel-specific files (located in `optional/deployments/`):

```
optional/deployments/
├── vercel.json                 # Vercel configuration
├── requirements-vercel.txt     # Serverless dependencies  
├── deploy-vercel.ps1          # PowerShell deployment script
├── deploy-vercel.sh           # Bash deployment script  
└── api/                       # Serverless functions
    ├── webhook.py             # Webhook handler function
    ├── health.py              # Health check function
    └── requirements.txt       # API dependencies
```

---

## 📁 Project Structure  

### 🔄 File Preparation

Before deploying, you need to organize files for Vercel's serverless architecture:

```powershell
# Copy Vercel-specific files to root directory
Copy-Item "optional/deployments/vercel.json" -Destination "."
Copy-Item "optional/deployments/requirements-vercel.txt" -Destination "."  
Copy-Item "optional/deployments/api" -Destination "." -Recurse
```

### 📂 Expected Structure

After preparation, your root should look like:

```
discord-bot/
├── 📄 vercel.json              # Vercel configuration
├── 📄 requirements-vercel.txt  # Serverless dependencies  
├── 📁 api/                     # Serverless functions
│   ├── 🐍 webhook.py           # Main webhook handler
│   ├── 🏥 health.py            # Health check endpoint
│   └── 📄 requirements.txt     # Function dependencies
├── 📁 optional/                # Original files (keep for reference)
└── 📄 [other core files...]    # Your existing bot files
```

### 🔧 Configuration Files

#### `vercel.json` Configuration
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/webhook",
      "dest": "/api/webhook.py"
    },
    {
      "src": "/health", 
      "dest": "/api/health.py"
    }
  ]
}
```

#### Serverless Dependencies
`requirements-vercel.txt` contains minimal dependencies for serverless:
```
discord.py==2.3.2
pydantic==2.5.0  
cryptography==41.0.7
```

---

## 🚀 Deployment Methods

### 🎯 Method 1: Vercel CLI (Recommended)

#### Step 1: Install Vercel CLI
```powershell
# Install Vercel CLI globally
npm install -g vercel

# Verify installation
vercel --version
```

#### Step 2: Login to Vercel
```powershell
# Login to your Vercel account
vercel login

# Follow the browser authentication flow
```

#### Step 3: Prepare Project
```powershell
# Copy Vercel files to root (if not done already)
./optional/deployments/deploy-vercel.ps1 prepare

# Or manually:
Copy-Item "optional/deployments/*" -Destination "." -Recurse -Force
```

#### Step 4: Deploy
```powershell
# First deployment (interactive setup)
vercel

# Follow prompts:
# ? Set up and deploy "patchy-discord-bot"? [Y/n] Y
# ? Which scope do you want to deploy to? [Your account]  
# ? Link to existing project? [N/y] N
# ? What's your project's name? patchy-discord-bot
# ? In which directory is your code located? ./

# Production deployment
vercel --prod
```

### 🎯 Method 2: Vercel Dashboard

#### Step 1: Connect GitHub Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. **Import Git Repository** → Select your GitHub repo
4. Click **"Import"**

#### Step 2: Configure Project
```
🏷️ Project Name: patchy-discord-bot
📁 Framework Preset: Other  
🔧 Root Directory: ./
📦 Build Command: (leave empty)
📂 Output Directory: (leave empty)
🔗 Install Command: pip install -r requirements-vercel.txt
```

---

## 🌍 Environment Configuration

### 🔑 Required Environment Variables

These must be configured in Vercel for your bot to function:

| Variable | Description | How to Get |
|----------|-------------|------------|
| `DISCORD_TOKEN` | Discord bot token | Discord Developer Portal → Bot → Token |
| `DISCORD_CHANNEL_ID` | Target channel ID | Right-click Discord channel → Copy ID |
| `GITHUB_WEBHOOK_SECRET` | Webhook security secret | Generate secure random string |

### ⚙️ Setting Environment Variables

#### Method 1: Vercel CLI
```powershell
# Set environment variables via CLI
vercel env add DISCORD_TOKEN
# Enter your Discord bot token when prompted

vercel env add DISCORD_CHANNEL_ID  
# Enter your Discord channel ID when prompted

vercel env add GITHUB_WEBHOOK_SECRET
# Enter your webhook secret when prompted

# Redeploy with new environment variables
vercel --prod
```

#### Method 2: Vercel Dashboard
1. Go to your project in [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable:
   - **Name**: Variable name (e.g., `DISCORD_TOKEN`)
   - **Value**: Your actual value  
   - **Environment**: Select "Production" and "Preview"
   - Click **Save**

#### Method 3: Bulk Import
```powershell
# Create .env.vercel file (gitignored)
DISCORD_TOKEN=your_discord_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here

# Import all variables at once
vercel env pull .env.vercel
```

### 🔐 Security Best Practices

- ✅ **Never commit secrets** to your repository
- ✅ **Use strong webhook secrets** (32+ characters)
- ✅ **Different secrets per environment** (dev vs production)
- ✅ **Rotate secrets regularly** (every 6 months)
- ✅ **Limit environment access** in Vercel team settings

---

## 🔗 GitHub Webhook Setup

### 📝 Configure Repository Webhook

1. **Navigate to Your Repository**
   - Go to your GitHub repository
   - Click **Settings** tab

2. **Access Webhooks**
   - Click **Webhooks** in left sidebar
   - Click **Add webhook** button

3. **Configure Webhook**
   ```
   📡 Payload URL: https://your-project.vercel.app/webhook
   📋 Content type: application/json
   🔐 Secret: [Your GITHUB_WEBHOOK_SECRET]
   
   🎯 Which events would you like to trigger this webhook?
   ☑️ Pushes              # Code commits
   ☑️ Pull requests       # PR lifecycle  
   ☑️ Issues              # Issue creation/updates
   ☑️ Issue comments      # Comments on issues
   ☑️ Pull request reviews # Code reviews
   ☑️ Releases           # Version releases
   
   ☑️ Active (webhook is active)
   ```

4. **Save and Test**
   - Click **Add webhook**
   - GitHub sends a test ping
   - Look for ✅ green checkmark indicating success

### 🌐 Finding Your Vercel URL

After deployment, find your URL in:

#### Vercel CLI
```powershell
# Get deployment URL
vercel ls

# View project details
vercel inspect your-project-name
```

#### Vercel Dashboard
1. Go to your project dashboard
2. Copy the **Production** domain
3. Your webhook endpoint: `https://your-domain.vercel.app/webhook`

### 🔧 Custom Domain (Optional)

```powershell
# Add custom domain
vercel domains add your-bot.yourdomain.com

# Update webhook URL to:
# https://your-bot.yourdomain.com/webhook
```
---

## 🧪 Testing & Verification

### 🏥 Health Check

After deployment, verify your serverless functions are working:

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "https://your-project.vercel.app/health"

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-09-13T12:34:56Z",
#   "vercel": true,
#   "environment_check": "✅ All required variables present"
# }
```

### 🧪 Webhook Testing

#### Method 1: Real GitHub Event
```powershell
# Make a test commit to trigger webhook
echo "Testing Vercel deployment: $(Get-Date)" >> test.txt
git add test.txt  
git commit -m "Test Vercel serverless webhook"
git push

# Watch for Discord notification
```

#### Method 2: Manual Webhook Test
```powershell
# Simulate GitHub webhook payload
$headers = @{
    "Content-Type" = "application/json"
    "X-GitHub-Event" = "push"
    "X-Hub-Signature-256" = "sha256=test-signature"
}

$payload = @{
    repository = @{
        name = "test-repo"
        full_name = "user/test-repo"
    }
    commits = @(@{
        id = "abc123"
        message = "Test commit"
        author = @{ name = "Test User" }
    })
} | ConvertTo-Json -Depth 5

# Send test webhook
Invoke-RestMethod -Uri "https://your-project.vercel.app/webhook" -Method POST -Headers $headers -Body $payload
```

#### Method 3: GitHub Webhook Redeliver
1. Go to Repository **Settings** → **Webhooks**
2. Click your webhook
3. Scroll to **Recent Deliveries**
4. Click **Redeliver** on any delivery
5. Check Discord for notification

### � Vercel Analytics

Monitor your deployment performance:

1. **Vercel Dashboard** → **Analytics**
   - Function invocation count
   - Average execution time
   - Error rates
   - Geographic distribution

2. **Function Logs**
   - Go to **Functions** tab in Vercel dashboard
   - Click **View Function Logs**
   - Monitor webhook processing logs

### 🔍 Testing Checklist

- [ ] **Health endpoint responding**: `GET /health` returns 200
- [ ] **Environment variables loaded**: No missing variable errors
- [ ] **GitHub webhook configured**: Webhook URL points to Vercel
- [ ] **Webhook signature validation**: Security working correctly
- [ ] **Discord notifications working**: Messages appear in channel
- [ ] **Function logs clean**: No errors in Vercel function logs

---

## 🔧 Troubleshooting

### ❓ Common Issues & Solutions

#### 🔴 "Invalid signature" Error
**Symptoms**: Webhook receives request but returns 401/403

```powershell
# Check if webhook secrets match
# In Vercel Dashboard → Settings → Environment Variables
# Verify GITHUB_WEBHOOK_SECRET matches GitHub webhook secret exactly

# Test signature validation
# Check Vercel function logs for signature details
vercel logs --function=api/webhook.py
```

**Solutions**:
- Ensure webhook secret has no extra spaces/newlines
- Verify secret is identical in both GitHub and Vercel
- Re-add environment variable in Vercel if needed

#### 🔴 Discord Messages Not Sending  
**Symptoms**: Webhook processes successfully but no Discord notification

```powershell
# Check Discord token validity
# Test in Vercel function logs for Discord API errors
vercel logs | Select-String "discord"
```

**Common Causes**:
- Invalid Discord token (regenerate in Developer Portal)
- Wrong channel ID (right-click channel → Copy ID)  
- Missing bot permissions ("Send Messages", "Embed Links")
- Bot not added to Discord server

#### 🔴 Function Timeout
**Symptoms**: Webhook requests time out (10 second limit on hobby plan)

```powershell
# Check function execution time in Vercel dashboard
# Functions that take >10 seconds will timeout
```

**Solutions**:
- Optimize Discord API calls
- Upgrade to Vercel Pro plan (30 second limit)
- Consider using Railway or Docker for persistent connections

#### 🔴 Cold Start Delays
**Symptoms**: First webhook after inactivity is slow

**This is normal behavior for serverless**:
- Vercel spins down functions after inactivity
- First request wakes up the function (cold start)
- Subsequent requests are fast (warm start)

**Solutions**:
- Expect 1-3 second delays for first request
- Pro plan has faster cold starts
- Consider Railway for always-on deployment

#### 🔴 Build/Deployment Failures

```powershell
# Check build logs in Vercel dashboard
# Common issues:

# 1. Missing requirements-vercel.txt
# Copy from optional/deployments/requirements-vercel.txt

# 2. Wrong Python version  
# Vercel uses Python 3.9 by default
# Add runtime configuration if needed

# 3. Import errors in serverless functions
# Check api/webhook.py and api/health.py
```

### 🛠️ Debug Tools

#### Vercel CLI Debugging
```powershell
# View recent deployments
vercel ls

# Get detailed logs
vercel logs

# Inspect specific function
vercel logs --function=api/webhook.py

# Check environment variables
vercel env ls
```

#### Function Testing
```powershell
# Test functions locally (if vercel dev is available)
vercel dev

# Test health endpoint locally
Invoke-WebRequest -Uri "http://localhost:3000/api/health.py"
```

### 🧹 Reset & Redeploy

If issues persist, try a clean redeploy:

```powershell
# 1. Remove old deployment
vercel remove your-project-name

# 2. Clear any cached data
Remove-Item .vercel -Recurse -Force

# 3. Redeploy from scratch
vercel --prod

# 4. Re-add environment variables
vercel env add DISCORD_TOKEN
vercel env add DISCORD_CHANNEL_ID
vercel env add GITHUB_WEBHOOK_SECRET
```

---

## ⚠️ Limitations & Considerations

### 🕐 Serverless Constraints

#### Function Limits
| Limit | Hobby Plan | Pro Plan |
|-------|------------|----------|
| **Execution Time** | 10 seconds | 30 seconds |
| **Memory** | 1008 MB | 1008 MB |
| **Payload Size** | 5 MB | 5 MB |
| **Invocations/month** | 100,000 | 1,000,000 |

#### Cold Start Behavior
- ❄️ **First request**: 1-3 second delay (function initialization)
- 🔥 **Subsequent requests**: <100ms (function already warm)
- 🕐 **Idle timeout**: Functions sleep after ~5 minutes of inactivity

### 💰 Cost Considerations

#### Vercel Pricing
- **Hobby Plan**: Free
  - 100,000 function invocations/month
  - Good for personal projects/testing
- **Pro Plan**: $20/month
  - 1M function invocations/month
  - Faster cold starts, better analytics

#### Usage Estimation
```
Average Discord Bot Usage:
- 10 commits/day × 30 days = 300 webhook invocations/month
- Well within free tier limits!

High Activity Repository:  
- 100 commits/day × 30 days = 3,000 invocations/month
- Still within free tier, but consider traffic spikes
```

### � Serverless vs Always-On Comparison

| Feature | Vercel Serverless | Railway Always-On |
|---------|-------------------|-------------------|
| **Cost** | $0 (low usage) | $5+/month |
| **Cold Starts** | 1-3 seconds | None |
| **Scaling** | Automatic | Manual/Auto |
| **Persistent State** | None | Full |
| **Setup Complexity** | Medium | Low |
| **Best For** | Low/medium traffic | High traffic, complex bots |

### 📊 When to Choose Vercel

✅ **Choose Vercel if:**
- Webhook traffic is low-to-medium volume
- Cost is a primary concern
- You want automatic scaling  
- Cold start delays are acceptable (1-3 seconds)

❌ **Consider alternatives if:**
- Need persistent Discord bot connection
- High-frequency webhook traffic (>1000/day)
- Need sub-second response times
- Complex bot functionality beyond webhooks

---

## ⚙️ Advanced Configuration

### 🔧 Custom Vercel Configuration

#### Enhanced `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python@3.1.0",
      "config": {
        "runtime": "python3.9",
        "maxDuration": 30
      }
    }
  ],
  "routes": [
    {
      "src": "/webhook",
      "dest": "/api/webhook.py",
      "headers": {
        "cache-control": "no-cache"
      }
    },
    {
      "src": "/health",
      "dest": "/api/health.py",
      "headers": {
        "cache-control": "s-maxage=60"
      }
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.9"
  }
}
```

### 🌍 Edge Function Optimization

#### Regional Deployment
```json
{
  "functions": {
    "api/webhook.py": {
      "regions": ["iad1", "sfo1", "lhr1"]
    }
  }
}
```

#### Memory Configuration  
```json
{
  "functions": {
    "api/webhook.py": {
      "memory": 1008
    }
  }
}
```

### 📊 Monitoring & Analytics

#### Custom Analytics
```python
# In api/webhook.py
import time
from datetime import datetime

def track_webhook_metrics(event_type, processing_time):
    print(f"WEBHOOK_METRIC: {event_type} processed in {processing_time:.2f}s at {datetime.utcnow().isoformat()}")
    
# Use in webhook handler
start_time = time.time()
# ... process webhook ...
processing_time = time.time() - start_time
track_webhook_metrics(github_event, processing_time)
```

#### Error Tracking Integration
```python
# Optional: Add Sentry or similar error tracking
# pip install sentry-sdk in requirements-vercel.txt

import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")

# Automatic error tracking in serverless functions
```

---

## 🎯 Next Steps

### 🚀 Production Optimizations

1. **⚡ Performance Tuning**
   ```python
   # Optimize Discord API calls
   # Cache bot connections between invocations (if possible)
   # Minimize function execution time
   ```

2. **📊 Enhanced Monitoring**
   - Set up Vercel webhook alerts
   - Integrate with external monitoring (Datadog, New Relic)
   - Create custom dashboards for webhook metrics

3. **🔒 Security Enhancements**
   - Implement rate limiting for webhook endpoint
   - Add IP allowlisting for GitHub webhooks
   - Set up anomaly detection for unusual traffic

### 🔄 Migration Considerations

#### From Vercel to Always-On (if needed)
```powershell
# If you outgrow serverless limitations:
# 1. Export Vercel environment variables
vercel env pull .env.production

# 2. Deploy to Railway using existing code  
# 3. Update GitHub webhook URL
# 4. Test thoroughly before switching
```

#### Multi-Platform Strategy
```
Development: Local testing with ngrok
Staging: Vercel serverless (cost-effective testing)
Production: Railway always-on (if high traffic)
```

---

## 📚 Related Resources

- **🧪 Local Testing**: [`docs/LOCAL_TESTING.md`](./LOCAL_TESTING.md) - Test before deploying
- **🚀 Railway Alternative**: [`docs/RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md) - Always-on deployment
- **🐳 Docker Option**: [`docs/DOCKER.md`](./DOCKER.md) - Containerized deployment
- **🔧 Environment Variables**: [`docs/DOCKER_ENV.md`](./DOCKER_ENV.md) - Configuration management
- **📖 Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **🐍 Vercel Python Runtime**: [vercel.com/docs/functions/serverless-functions/runtimes/python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

---

> **🎉 Success!** Your Patchy Discord Bot is now deployed as serverless functions on Vercel's global edge network!
```

## 💰 Cost Considerations

### Vercel Free Tier Limits

- **Function invocations**: 100,000 per month
- **Function execution time**: 10 seconds max
- **Bandwidth**: 100GB per month

### For Internal Use

The free tier should be sufficient for internal use with moderate GitHub activity. Monitor your usage in the Vercel dashboard.

## 🔄 Updates and Maintenance

### Updating the Bot

1. **Make changes** to your code
2. **Commit and push** to your repository
3. **Vercel automatically redeploys** (if connected to GitHub)

### Environment Variable Updates

1. **Via CLI**:
   ```bash
   vercel env add VARIABLE_NAME
   vercel --prod
   ```

2. **Via Dashboard**:
   - Go to Project Settings → Environment Variables
   - Update values and redeploy

## 🆚 Vercel vs Other Platforms

### Advantages of Vercel

- ✅ **Free tier** with generous limits
- ✅ **Automatic deployments** from GitHub
- ✅ **Global CDN** for fast response times
- ✅ **Built-in analytics** and monitoring
- ✅ **Easy environment variable management**

### Limitations

- ❌ **No persistent connections** (serverless only)
- ❌ **10-second timeout** on free tier
- ❌ **Cold start delays** for inactive functions

### When to Use Vercel

Vercel is perfect for:
- Internal tools with moderate usage
- Projects that don't need persistent connections
- Teams that want easy deployment and monitoring

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Discord Bot API](https://discord.com/developers/docs/intro)
- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)

## 🎉 Success!

Once deployed, Patchy will:
- ✅ Receive GitHub webhook events
- ✅ Send beautiful Discord notifications
- ✅ Handle errors gracefully
- ✅ Scale automatically with usage

Your internal team will now get real-time notifications about GitHub activity in your Discord server!
