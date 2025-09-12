# Deploying Patchy to Vercel

This guide will help you deploy Patchy - GitHub Discord Webhook Bot to Vercel's serverless platform.

## 🚀 Quick Start

### Prerequisites

- A Vercel account (free tier available)
- A Discord bot token
- A GitHub repository
- Git installed on your machine

### 1. Prepare Your Repository

1. **Clone or create your repository** with the Patchy bot code
2. **Ensure you have the Vercel-specific files**:
   - `vercel.json` - Vercel configuration
   - `api/webhook.py` - Webhook handler
   - `api/health.py` - Health check endpoint
   - `requirements-vercel.txt` - Simplified dependencies

### 2. Set Up Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy the bot token
4. Invite the bot to your server with "Send Messages" permission
5. Get your Discord channel ID (right-click channel → Copy ID)

### 3. Deploy to Vercel

#### Option A: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy your project**:
   ```bash
   vercel
   ```

4. **Set environment variables**:
   ```bash
   vercel env add DISCORD_TOKEN
   vercel env add DISCORD_CHANNEL_ID
   vercel env add GITHUB_WEBHOOK_SECRET
   ```

5. **Redeploy with environment variables**:
   ```bash
   vercel --prod
   ```

#### Option B: Deploy via Vercel Dashboard

1. **Connect your GitHub repository**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure the project**:
   - Framework Preset: "Other"
   - Root Directory: `./` (default)
   - Build Command: Leave empty
   - Output Directory: Leave empty

3. **Set environment variables**:
   - Go to Project Settings → Environment Variables
   - Add the following variables:
     - `DISCORD_TOKEN`: Your Discord bot token
     - `DISCORD_CHANNEL_ID`: Your Discord channel ID
     - `GITHUB_WEBHOOK_SECRET`: A secure random string

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete

### 4. Set Up GitHub Webhook

1. **Get your Vercel URL**:
   - After deployment, you'll get a URL like `https://your-project.vercel.app`
   - Your webhook endpoint will be: `https://your-project.vercel.app/webhook`

2. **Configure GitHub webhook**:
   - Go to your GitHub repository
   - Navigate to Settings → Webhooks → Add webhook
   - Set Payload URL: `https://your-project.vercel.app/webhook`
   - Set Content type: `application/json`
   - Set Secret: The same value you used for `GITHUB_WEBHOOK_SECRET`
   - Select events: Push, Pull requests, Issues, Releases
   - Click "Add webhook"

### 5. Test Your Deployment

1. **Health check**:
   ```bash
   curl https://your-project.vercel.app/health
   ```

2. **Test webhook** (optional):
   ```bash
   curl -X POST https://your-project.vercel.app/webhook \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Event: push" \
     -d '{"test": "payload"}'
   ```

3. **Make a test commit** to your GitHub repository and check Discord for notifications

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_TOKEN` | Your Discord bot token | Yes |
| `DISCORD_CHANNEL_ID` | Discord channel ID for notifications | Yes |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook verification | Yes |

### Vercel Configuration

The `vercel.json` file configures:
- **Builds**: Python functions for webhook and health endpoints
- **Routes**: URL routing for the API endpoints
- **Environment**: Variable mapping for secrets

## 📊 Monitoring

### Health Checks

- **Basic health**: `GET /health`
- **Detailed status**: Includes environment variable status

### Logs

- View logs in Vercel Dashboard → Functions → View Function Logs
- Logs include webhook processing and Discord API calls

### Analytics

- Vercel provides built-in analytics for function invocations
- Monitor webhook success rates and response times

## 🚨 Troubleshooting

### Common Issues

1. **"Invalid signature" error**:
   - Verify `GITHUB_WEBHOOK_SECRET` matches in both Vercel and GitHub
   - Check that the webhook URL is correct

2. **Discord messages not sending**:
   - Verify `DISCORD_TOKEN` is correct
   - Check `DISCORD_CHANNEL_ID` is valid
   - Ensure bot has permission to send messages

3. **Function timeout**:
   - Vercel has a 10-second timeout for hobby plans
   - Check logs for slow Discord API responses

4. **Cold start delays**:
   - First request after inactivity may be slower
   - Consider upgrading to Pro plan for better performance

### Debug Mode

Enable detailed logging by checking Vercel function logs:
```bash
vercel logs
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
