# Patchy - GitHub Discord Webhook Bot

A production-ready Discord bot named "Patchy" that receives GitHub webhook events and sends beautifully formatted notifications to your Discord server. Built with Python, FastAPI, and discord.py.

![ThumbNail](<Patchy Thumb Nail.png>)

## Features

- 🚀 **Real-time Notifications**: Get instant Discord notifications for GitHub events
- 🎨 **Beautiful Embeds**: Rich, formatted messages with colors, links, and detailed information
- 🔒 **Secure**: GitHub webhook signature verification for security
- 📊 **Comprehensive Event Support**: Push, Pull Requests, Issues, Releases, Branch/Tag creation/deletion
- 🛡️ **Production Ready**: Comprehensive error handling, logging, and monitoring
- 🚢 **Easy Deployment**: Ready for Render (Docker), Railway, Vercel (serverless), and Docker
- 💰 **Cost-Effective**: Free tier options available for internal use

## 📁 Project Structure

This project is organized into a clean structure:

```
discord-bot/
├── 📄 Core Files (Essential)     # Main application files
├── � Docker Files (Important)  # Container setup & orchestration
├── �📚 docs/                     # Documentation guides
├── 🛠️ dev-tools/               # Testing & development utilities  
└── 📦 optional/                 # Alternative deployments
    └── deployments/             # Vercel, Render, etc.
```

**📖 See [`STRUCTURE.md`](STRUCTURE.md) for detailed information about the project organization.**

## Supported GitHub Events

- **Push Events**: New commits with author info and commit messages
- **Pull Requests**: Open, close, merge, and reopen events
- **Issues**: Open, close, and reopen with labels
- **Releases**: New releases with descriptions and download links
- **Create/Delete**: Branch and tag creation/deletion events

## Quick Start

### Prerequisites

- Python 3.11 or higher
- A Discord server where you have admin permissions
- A GitHub repository
- A hosting service (Railway, Render, Heroku, or your own server)

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Under "Privileged Gateway Intents", enable "Message Content Intent"
6. Go to "OAuth2" → "URL Generator"
7. Select "bot" scope and "Send Messages" permission
8. Use the generated URL to invite the bot to your server

### 2. Get Discord Channel ID

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on the channel where you want notifications
3. Click "Copy ID"

### 3. Set Up GitHub Webhook

1. Go to your GitHub repository
2. Navigate to Settings → Webhooks → Add webhook
3. Set the Payload URL to: `https://your-domain.com/webhook`
4. Set Content type to: `application/json`
5. Generate a webhook secret (save this!)
6. Select events: Push, Pull requests, Issues, Releases, Create, Delete
7. Click "Add webhook"

### 4. Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd discord-bot
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your tokens and IDs
   ```

3. **Run the bot**:
   ```bash
   python main.py
   ```

4. **Local Testing** (Optional):
   ```bash
   # Test webhook locally
   python dev-tools/local_test.py test push

   # Or use PowerShell helper
   ./dev-tools/local-dev.ps1 test push
   ```

📖 **Complete local testing guide**: See [`docs/LOCAL_TESTING.md`](docs/LOCAL_TESTING.md)

### 5. Environment Variables

Create a `.env` file with the following variables:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here

# GitHub Webhook Configuration
GITHUB_WEBHOOK_SECRET=your_github_webhook_secret_here

# Server Configuration (optional)
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
```

## Deployment

### Quick Deployment Options

- **🚀 Railway** (Recommended): Easy deployment with persistent connections
- **⚡ Vercel**: Free serverless option for internal use  
- **🐳 Docker**: Containerized deployment for any platform
- **☁️ Render**: Alternative cloud platform

### Railway Deployment (Recommended)

1. **Connect your repository**:
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository
## 🚀 Deployment Options

### Render Deployment (Recommended - Docker)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR-USERNAME/YOUR-REPO-NAME)

**Quick Setup**:
1. Click the "Deploy to Render" button above
2. Set your environment variables during setup
3. Wait for build completion (2-5 minutes)
4. Configure GitHub webhook with your new Render URL

📖 **Complete Render guide**: See [`docs/RENDER_DEPLOYMENT.md`](docs/RENDER_DEPLOYMENT.md)

### Railway Deployment (Alternative)

Fast deployment with excellent developer experience:

```bash
# One-click deploy
railway deploy --template=your-repo
```

1. **Connect your repository**:
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo" 
   - Select your repository
   - Deploy automatically

2. **Set environment variables** in Railway dashboard:
   - `DISCORD_TOKEN`
   - `DISCORD_CHANNEL_ID` 
   - `GITHUB_WEBHOOK_SECRET`

3. **Configure GitHub webhook**:
   - Use your Railway URL: `https://your-app.up.railway.app/webhook`

📖 **Detailed Railway guide**: See [`docs/RAILWAY_DEPLOYMENT.md`](docs/RAILWAY_DEPLOYMENT.md)

### Vercel Deployment (Serverless)

Perfect for internal use with serverless architecture:

```bash
# Quick deploy
npx vercel

# Set environment variables
vercel env add DISCORD_TOKEN
vercel env add DISCORD_CHANNEL_ID
vercel env add GITHUB_WEBHOOK_SECRET
```

📖 **Detailed Vercel guide**: See [`docs/VERCEL_DEPLOYMENT.md`](docs/VERCEL_DEPLOYMENT.md)

### Docker Deployment (Self-Hosted)

For containerized deployment (Docker files are in root directory):

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build image manually
docker build -t patchy-discord-bot .
docker run -p 8000:8000 --env-file .env patchy-discord-bot
```

📖 **Complete Docker guide**: See [`docs/DOCKER.md`](docs/DOCKER.md)
   - Railway will automatically detect the `railway.json` configuration
   - Your bot will be deployed and running!

4. **Update GitHub webhook**:
   - Use your Railway domain: `https://your-app.railway.app/webhook`

### Render Deployment

1. **Create a new Web Service**:
   - Go to [Render](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment: `Python 3`

3. **Set environment variables**:
   - Add all required environment variables

4. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy your bot

5. **Update GitHub webhook**:
   - Use your Render domain: `https://your-app.onrender.com/webhook`

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t github-discord-bot .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name github-discord-bot \
     -p 8000:8000 \
     -e DISCORD_TOKEN=your_token \
     -e DISCORD_CHANNEL_ID=your_channel_id \
     -e GITHUB_WEBHOOK_SECRET=your_secret \
     github-discord-bot
   ```

## Configuration

### Discord Bot Permissions

Your Discord bot needs the following permissions:
- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands (if you plan to add them)

### GitHub Webhook Events

The bot supports these GitHub events:
- `push` - New commits
- `pull_request` - PR events
- `issues` - Issue events
- `release` - Release events
- `create` - Branch/tag creation
- `delete` - Branch/tag deletion

### Customization

You can customize the bot by modifying the embed creation functions in `webhook_server.py`:
- Change colors by modifying the `color` parameter
- Add or remove fields in the embeds
- Modify the emoji and formatting
- Add custom logic for specific repositories

## Monitoring and Logs

### Health Checks

The bot provides health check endpoints:
- `GET /` - Basic health check
- `GET /health` - Detailed health information

### Logging

The bot uses structured logging with different levels:
- `DEBUG` - Detailed debugging information
- `INFO` - General information about operations
- `WARNING` - Warning messages
- `ERROR` - Error messages

### Error Handling

The bot includes comprehensive error handling:
- Invalid webhook signatures are rejected
- Discord API errors are logged and handled gracefully
- Malformed GitHub payloads are handled safely
- Network issues are retried automatically

## Troubleshooting

### Common Issues

1. **Bot not responding**:
   - Check if the bot is online in Discord
   - Verify the Discord token is correct
   - Check the channel ID is valid

2. **Webhook not working**:
   - Verify the webhook URL is accessible
   - Check the GitHub webhook secret matches
   - Ensure the bot is running and healthy

3. **Missing notifications**:
   - Check which events are selected in GitHub webhook settings
   - Verify the bot has permission to send messages
   - Check the logs for any errors

### Debug Mode

Enable debug mode for detailed logging:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Testing Webhooks

You can test your webhook using curl:
```bash
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{"test": "payload"}'
```

## Security Considerations

- **Webhook Secret**: Always use a strong, unique secret for GitHub webhooks
- **Environment Variables**: Never commit tokens or secrets to version control
- **HTTPS**: Always use HTTPS in production
- **Permissions**: Use the principle of least privilege for Discord bot permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Support for push, pull request, issue, and release events
- Beautiful Discord embeds with rich formatting
- Comprehensive error handling and logging
- Ready for deployment on Railway, Render, and Docker
