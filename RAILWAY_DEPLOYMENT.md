# Railway Deployment Guide

## 🚀 Your Bot is Live!

**Railway Endpoint**: `https://web-production-13df.up.railway.app/`

### Health Check
- **URL**: `https://web-production-13df.up.railway.app/health`
- **Status**: ✅ Healthy (verified)

### Webhook Endpoint  
- **URL**: `https://web-production-13df.up.railway.app/webhook`

## 📝 GitHub Webhook Configuration

### Configure Your Repository Webhook:

1. **Go to your GitHub repository**
2. **Settings** → **Webhooks** → **Add webhook**
3. **Fill in the details**:
   ```
   Payload URL: https://web-production-13df.up.railway.app/webhook
   Content type: application/json
   Secret: [Your GITHUB_WEBHOOK_SECRET]
   
   Which events would you like to trigger this webhook?
   ☑️ Pushes
   ☑️ Pull requests  
   ☑️ Issues
   
   ☑️ Active (webhook is active)
   ```
4. **Click "Add webhook"**

### Test Your Webhook

#### Option 1: Test with Script
```powershell
# Test your Railway deployment
python test_railway.py
```

#### Option 2: Make a Real Commit
1. Make any change to your repository
2. Commit and push the changes
3. Check your Discord channel for the notification
4. Monitor webhook deliveries in GitHub Settings → Webhooks

#### Option 3: Manual Test via GitHub
1. Go to your webhook settings in GitHub
2. Click on your webhook
3. Scroll to "Recent Deliveries"  
4. Click "Redeliver" on any previous delivery

## 🔧 Railway Environment Variables

Make sure these are set in your Railway deployment:

**Required:**
- `DISCORD_TOKEN` - Your Discord bot token
- `DISCORD_CHANNEL_ID` - Target Discord channel ID  
- `GITHUB_WEBHOOK_SECRET` - Secret for webhook verification

**Optional:**
- `HOST=0.0.0.0` (default)
- `PORT=8000` (Railway will override this)
- `DEBUG=false` (default)
- `LOG_LEVEL=INFO` (default)

## 📊 Monitoring Your Deployment

### Railway Dashboard
- **Deployment URL**: https://railway.app/project/[your-project-id]
- Monitor logs, metrics, and deployments

### Health Monitoring
```powershell
# Check if your bot is running
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"
```

### GitHub Webhook Monitoring
- GitHub Repository → Settings → Webhooks
- Click your webhook to see delivery history
- Check "Recent Deliveries" for success/failure status

## 🐛 Troubleshooting

### Common Issues & Solutions

**1. Webhook delivery fails (HTTP 500/400)**
- Check Railway logs for errors
- Verify environment variables are set correctly
- Ensure Discord bot has proper permissions

**2. Discord notifications not appearing**
- Verify `DISCORD_TOKEN` is correct
- Check `DISCORD_CHANNEL_ID` is valid
- Ensure bot is in the Discord server and channel

**3. Signature verification fails**
- Verify `GITHUB_WEBHOOK_SECRET` matches exactly
- Check for extra spaces or newlines in secret

**4. Railway app not responding**
- Check Railway deployment status
- Look at Railway logs for startup errors
- Verify `requirements.txt` is correct

### Debugging Commands

```powershell
# Test webhook endpoint
python test_railway.py

# Check health endpoint
Invoke-WebRequest -Uri "https://web-production-13df.up.railway.app/health"

# Test with curl (if available)
curl -X GET https://web-production-13df.up.railway.app/health
```

## 🔄 Updating Your Deployment

When you make changes to your bot:

1. **Commit changes to your repository**
2. **Railway auto-deploys** from your connected GitHub repository
3. **No manual deployment needed** (if auto-deploy is enabled)

### Manual Deployment (if needed)
```bash
# Using Railway CLI (optional)
railway deploy
```

## 📈 Next Steps

### Enhance Your Bot
- Add more webhook events (releases, forks, etc.)
- Customize Discord message formatting
- Add emoji reactions and rich embeds
- Implement webhook filtering by branch

### Monitoring & Observability  
- Set up Railway alerts
- Monitor Discord message delivery rates
- Track webhook response times
- Add custom metrics and logging

### Security
- Rotate webhook secrets regularly
- Monitor failed webhook attempts
- Set up rate limiting if needed
- Review Discord bot permissions

## 🎉 Success!

Your Patchy Discord Bot is now live and ready to notify your Discord channel about GitHub events!

**Live Endpoints:**
- 🏥 Health: `https://web-production-13df.up.railway.app/health`
- 🪝 Webhook: `https://web-production-13df.up.railway.app/webhook`

Make a commit to see it in action! 🚀