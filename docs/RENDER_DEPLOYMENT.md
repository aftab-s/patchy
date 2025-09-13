# 🚀 Render Docker Deployment Guide

> **Status**: Ready for deployment - Deploy your Discord bot to Render with Docker!

## 📋 Table of Contents

1. [Deployment Status](#deployment-status)
2. [Quick Setup](#quick-setup)
3. [GitHub Webhook Configuration](#github-webhook-configuration)
4. [Testing Your Deployment](#testing-your-deployment)
5. [Environment Variables](#environment-variables)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Updates & Redeployment](#updates--redeployment)
9. [Render vs Other Platforms](#render-vs-other-platforms)

---

## 🎯 Deployment Status

### ✅ Your Deployed Application
- **🌍 Render Endpoint**: `https://your-app-name.onrender.com`
- **🏥 Health Check**: `https://your-app-name.onrender.com/health`
- **🪝 Webhook Endpoint**: `https://your-app-name.onrender.com/webhook`
- **📊 Status**: Check your Render dashboard for live status

### 📈 Application Info
```
🔧 Platform: Render (Docker)
🐳 Container: Custom Docker image
🐍 Runtime: Python 3.11
🌍 Region: Oregon, USA (default)
⚡ Build: Docker build from GitHub
🔄 Status: Running (check your dashboard)
📦 Memory: 512MB allocated
💰 Plan: Free tier (750 hours/month)
```

---

## ⚡ Quick Setup

If you're setting up from scratch or need to redeploy:

### 🚀 Option 1: One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR-USERNAME/YOUR-REPO-NAME)

### 🔧 Option 2: Manual Deployment

1. **Connect GitHub Repository**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **🔧 Configure Docker Service**:
   ```
   🏷️ Name: your-discord-bot-name
   📁 Root Directory: ./
   🐳 Environment: Docker  
   📦 Dockerfile Path: ./Dockerfile
   🌍 Region: Oregon (US West)
   💰 Instance Type: Free
   ```

3. **Set Environment Variables** (see [Environment Variables](#environment-variables))

4. **Deploy**:
   - Render automatically builds and deploys your Docker container
   - Build process takes 2-5 minutes

---

## 🔗 GitHub Webhook Configuration

### 📝 Step-by-Step Webhook Setup

1. **📂 Go to Your GitHub Repository**
   - Navigate to your repository on GitHub
   - Click on **Settings** tab

2. **🪝 Access Webhooks**  
   - In the left sidebar, click **Webhooks**
   - Click **Add webhook** button

3. **⚙️ Configure Webhook Settings**:
   ```
   📡 Payload URL: https://your-app-name.onrender.com/webhook
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

### 🎯 Update Existing Webhook

If you were previously using Railway or another platform:

1. **Go to Repository Settings → Webhooks**
2. **Click on your existing webhook**
3. **Update Payload URL**: Change to `https://your-app-name.onrender.com/webhook`
4. **Click "Update webhook"**
5. **Test**: Click "Recent Deliveries" → "Redeliver" to test

---

## 🧪 Testing Your Deployment

### 🎯 Method 1: Health Check

```powershell
# Test the health endpoint
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/health"

# Expected response:
# {
#   "message": "Patchy - GitHub Discord Webhook Bot is running!",
#   "status": "healthy"
# }
```

### 🎯 Method 2: Real GitHub Event

Make a real change to test the complete workflow:

```powershell
# Create a test commit
echo "Testing Render deployment: $(Get-Date)" >> test_render.md
git add test_render.md
git commit -m "Test Render webhook deployment"
git push
```

**What Should Happen**:
1. ⚡ GitHub sends webhook to Render
2. 🤖 Render processes webhook  
3. 💬 Discord receives notification
4. ✅ You see the commit notification in Discord

### 🎯 Method 3: Manual Webhook Test

```powershell
# Simulate GitHub webhook
$headers = @{
    "Content-Type" = "application/json"
    "X-GitHub-Event" = "push"
    "X-Hub-Signature-256" = "sha256=test-signature"
}

$payload = @{
    repository = @{
        name = "your-repo-name"
        full_name = "your-username/your-repo-name"
        html_url = "https://github.com/your-username/your-repo-name"
    }
    commits = @(@{
        id = "abc123"
        message = "Test Render deployment"
        author = @{ name = "Test User" }
        url = "https://github.com/your-username/your-repo-name/commit/abc123"
    })
} | ConvertTo-Json -Depth 5

# Send test webhook
Invoke-RestMethod -Uri "https://your-app-name.onrender.com/webhook" -Method POST -Headers $headers -Body $payload
```

---

## 🌍 Environment Variables

### 🔑 Required Variables

Configure these in your Render service:

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | `MTIzNDU2Nzg5MA.GhI...` |
| `DISCORD_CHANNEL_ID` | Target Discord channel ID | `1234567890123456789` |
| `GITHUB_WEBHOOK_SECRET` | GitHub webhook secret | `my-secure-webhook-secret` |

### ⚙️ Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host (Render handles this) |
| `PORT` | `8000` | Server port (Render auto-assigns) |
| `DEBUG` | `false` | Debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

### 🔧 Setting Environment Variables in Render

1. **Go to Render Dashboard** → Your service
2. **Click "Environment"** tab
3. **Add variables**:
   - Click **Add Environment Variable**
   - Enter **Key** and **Value**
   - Click **Save Changes**
4. **Redeploy**: Render automatically redeploys with new variables

### 🔒 Security Best Practices

- ✅ **Environment variables are encrypted** at rest in Render
- ✅ **Never commit secrets** to your repository
- ✅ **Use different secrets** for different environments
- ✅ **Monitor failed webhook attempts** for security

---

## 📊 Monitoring & Maintenance

### 🏥 Health Monitoring

```powershell
# Check service health
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/health"

# Monitor uptime and response times in Render dashboard
```

### 📊 Render Dashboard Monitoring

Access your [Render Dashboard](https://dashboard.render.com) to monitor:
- 📈 **CPU & Memory Usage**: Resource consumption
- 📊 **Request Metrics**: HTTP traffic and response times
- 🔄 **Deploy History**: Build logs and deployment timeline
- ⚠️ **Logs**: Application logs and errors
- 💰 **Usage**: Free tier hours remaining

### 🪝 Webhook Monitoring

- **GitHub**: Repository Settings → Webhooks → Check delivery status
- **Discord**: Verify notifications appear in your channel
- **Render Logs**: Check application logs for webhook processing

### 🚨 Render Free Tier Considerations

**Free Tier Limits**:
- 750 hours per month (31 days × 24 hours = 744 hours)
- Service sleeps after 15 minutes of inactivity
- Cold start delay: 10-30 seconds to wake up

**Cold Start Behavior**:
- ❄️ **First request after sleep**: 10-30 second delay
- 🔥 **Subsequent requests**: Normal speed
- 💡 **Tip**: Paid plans ($7/month) eliminate cold starts

---

## 🔧 Troubleshooting

### ❓ Common Issues & Solutions

#### 🔴 Service Won't Start / Build Failures
**Symptoms**: Build fails, service stuck in "Building" state

```bash
# Check Render build logs:
# 1. Go to Render Dashboard → Your service
# 2. Click "Logs" tab
# 3. Look for build errors

# Common fixes:
# - Verify Dockerfile syntax
# - Check requirements.txt dependencies
# - Ensure all required files are in repository
```

#### 🔴 Cold Start Delays
**Symptoms**: First webhook after inactivity is slow

```
This is normal behavior for Render free tier:
- Service sleeps after 15 minutes of inactivity
- First request takes 10-30 seconds to wake up
- Consider paid plan ($7/month) to eliminate cold starts
```

#### 🔴 Environment Variables Not Working
**Symptoms**: Bot can't connect to Discord

```bash
# Check environment variables in Render:
# 1. Dashboard → Your service → Environment tab
# 2. Verify all required variables are set
# 3. Check for typos in variable names
# 4. Redeploy after changing variables
```

#### 🔴 Webhook Delivery Fails
**Symptoms**: GitHub shows failed deliveries

```bash
# Check webhook URL is correct:
# https://your-app-name.onrender.com/webhook

# Verify service is running:
# curl https://your-app-name.onrender.com/health

# Check Render logs for errors:
# Dashboard → Logs → Filter for "webhook" or "error"
```

### 🛠️ Debug Commands

```powershell
# Health check
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/health"

# Test webhook endpoint (should return method not allowed for GET)
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/webhook"

# Check response headers
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/health" -Method HEAD
```

---

## 🔄 Updates & Redeployment

### 🚀 Automatic Deployment

Render automatically redeploys when you push to your connected branch:

```powershell
# Make changes to your code
# Edit discord_bot.py, webhook_server.py, etc.

# Commit and push changes
git add .
git commit -m "Update bot functionality"
git push origin main

# Render automatically:
# 1. Detects the push
# 2. Builds new Docker image
# 3. Deploys to production
# 4. Health checks the deployment
```

### ⚡ Manual Deployment

```bash
# Via Render Dashboard:
# 1. Go to your service
# 2. Click "Manual Deploy" → "Deploy latest commit"
# 3. Monitor build logs
```

### 📊 Deployment Verification

```powershell
# After deployment, verify:

# 1. Health check passes
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/health"

# 2. Test webhook with commit
git commit --allow-empty -m "Test Render deployment"
git push

# 3. Check Discord for notification

# 4. Verify in Render logs
# Dashboard → Logs → Look for successful webhook processing
```

---

## ⚖️ Render vs Other Platforms

### 🔄 Platform Comparison

| Feature | **Render (Current)** | Railway | Vercel | Docker Local |
|---------|---------------------|---------|--------|--------------|
| **Cost** | Free (750h/month) | $5+/month | Free (functions) | Free |
| **Cold Starts** | 10-30 seconds | None | 1-3 seconds | None |
| **Docker Support** | ✅ Full Docker | ✅ Native | ❌ Functions only | ✅ Full |
| **Persistent Storage** | ✅ Yes | ✅ Yes | ❌ Serverless | ✅ Yes |
| **Automatic Scaling** | ✅ Vertical | ✅ Yes | ✅ Serverless | ❌ Manual |
| **Setup Complexity** | 🟡 Medium | 🟢 Easy | 🟡 Medium | 🔴 Complex |

### 🎯 Why Render is Great for Your Bot

✅ **Advantages**:
- Full Docker support (exactly what you built)
- No cold starts on paid plan
- Persistent connections (good for Discord bots)
- Simple deployment from GitHub
- Built-in SSL certificates
- Good free tier for development

⚠️ **Considerations**:
- Cold starts on free tier (paid plan fixes this)
- Limited free tier hours (750/month)
- Build times can be slower than Railway

---

## 📚 Related Documentation

- **🧪 Local Testing**: [`docs/LOCAL_TESTING.md`](./LOCAL_TESTING.md) - Test before deploying
- **🐳 Docker Guide**: [`docs/DOCKER.md`](./DOCKER.md) - Docker containerization
- **⚡ Railway Alternative**: [`docs/RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md) - Alternative platform
- **☁️ Vercel Option**: [`docs/VERCEL_DEPLOYMENT.md`](./VERCEL_DEPLOYMENT.md) - Serverless functions
- **🔧 Environment Variables**: [`docs/DOCKER_ENV.md`](./DOCKER_ENV.md) - Environment management

---

> **🎉 Congratulations!** Your Discord Bot is successfully deployed on Render with Docker containerization!