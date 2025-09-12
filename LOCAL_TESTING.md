# Local Webhook Testing Guide

## Overview
Testing GitHub webhooks locally requires making your local application accessible from the internet, since GitHub needs to send HTTP requests to your webhook endpoint.

## Method 1: Using ngrok (Recommended)

### Step 1: Install ngrok
1. Go to https://ngrok.com and create a free account
2. Download ngrok for Windows
3. Extract and add to your PATH, or place in your project directory

### Step 2: Start Your Local Application
```powershell
# In one terminal, start your Discord bot
cd "s:\Env0-Lite\discord-bot"
python main.py
```

Your app will be running on `http://localhost:8000`

### Step 3: Create ngrok Tunnel
```powershell
# In a second terminal, create tunnel to your local app
ngrok http 8000
```

You'll see output like:
```
Session Status                online
Account                       your-account
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000
```

### Step 4: Configure GitHub Webhook
1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. **Payload URL**: `https://abc123.ngrok-free.app/webhook`
4. **Content type**: `application/json`
5. **Secret**: Your `GITHUB_WEBHOOK_SECRET` from `.env`
6. **Events**: Select the events you want (push, pull requests, etc.)
7. Click "Add webhook"

### Step 5: Test the Webhook
1. Make a commit or create a pull request in your repo
2. Check your Discord channel for notifications
3. Check ngrok web interface at `http://localhost:4040` for request details

---

## Method 2: Using LocalTunnel (Alternative)

### Install and Use LocalTunnel
```powershell
# Install localtunnel globally
npm install -g localtunnel

# Start your app
python main.py

# In another terminal, create tunnel
lt --port 8000 --subdomain your-bot-name
```

Then use `https://your-bot-name.loca.lt/webhook` as your GitHub webhook URL.

---

## Method 3: Manual Testing with curl

For testing without actual GitHub events, you can simulate webhook requests:

### Test Script (PowerShell)
```powershell
# Test your webhook endpoint locally
$headers = @{
    "Content-Type" = "application/json"
    "X-GitHub-Event" = "push"
    "X-Hub-Signature-256" = "sha256=your-calculated-signature"
}

$body = @{
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
            id = "abc123"
            message = "Test commit"
            author = @{
                name = "Test Author"
                email = "author@example.com"
            }
            url = "https://github.com/your-username/test-repo/commit/abc123"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/webhook" -Method POST -Headers $headers -Body $body
```

---

## Method 4: Docker with Port Forwarding

If you prefer using Docker:

```powershell
# Build the Docker image
docker build -t patchy-discord-bot .

# Run with port forwarding
docker run -p 8000:8000 --env-file .env patchy-discord-bot

# Then use ngrok to tunnel to localhost:8000
ngrok http 8000
```

---

## Development Workflow

### Recommended Setup
1. **Terminal 1**: Run your Discord bot
   ```powershell
   python main.py
   ```

2. **Terminal 2**: Run ngrok tunnel
   ```powershell
   ngrok http 8000
   ```

3. **Browser**: Keep ngrok web interface open at `http://localhost:4040`

### Environment Variables for Testing
Add these to your `.env` file:
```env
# Your existing variables
DISCORD_TOKEN=your_token
DISCORD_CHANNEL_ID=your_channel_id
GITHUB_WEBHOOK_SECRET=your_secret

# Optional: Enable debug mode for more detailed logs
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## Troubleshooting

### Common Issues

1. **Webhook delivery fails**
   - Check if your local app is running
   - Verify ngrok tunnel is active
   - Check GitHub webhook delivery logs

2. **Discord notifications not appearing**
   - Verify Discord token and channel ID
   - Check bot permissions in Discord server
   - Review application logs

3. **Signature verification fails**
   - Ensure `GITHUB_WEBHOOK_SECRET` matches exactly
   - Check that secret is set correctly in GitHub webhook

### Debugging Tools

1. **ngrok Web Interface**: `http://localhost:4040`
   - View all HTTP requests
   - Inspect headers and payloads
   - Replay requests for testing

2. **Application Logs**: Enable debug logging
   ```python
   LOG_LEVEL=DEBUG
   ```

3. **GitHub Webhook Logs**:
   - Go to repository Settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" tab

---

## Testing Checklist

Before testing:
- [ ] Local application is running (`python main.py`)
- [ ] ngrok tunnel is active and showing forwarding URL
- [ ] GitHub webhook is configured with correct URL
- [ ] Discord bot has proper permissions
- [ ] All environment variables are set correctly

During testing:
- [ ] Make a test commit or PR
- [ ] Check Discord for notification
- [ ] Review ngrok logs for webhook delivery
- [ ] Check application logs for any errors

---

## Production Considerations

Once your local testing is complete:
1. Deploy to a cloud service (Railway, Heroku, etc.)
2. Update GitHub webhook URL to production endpoint
3. Use proper SSL certificates (automatic with cloud providers)
4. Set up monitoring and logging for production webhooks

Remember: ngrok free tier URLs change each time you restart. For persistent testing, consider ngrok's paid plans or deploy to a development server.