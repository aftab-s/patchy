# 🐳 Docker Containerization Guide

> **Quick Start**: Run `docker-compose up --build` to get started immediately

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Deployment Methods](#deployment-methods)
6. [Environment Variables](#environment-variables)
7. [Monitoring & Debugging](#monitoring--debugging)
8. [Production Setup](#production-setup)
9. [Troubleshooting](#troubleshooting)
10. [Security Best Practices](#security-best-practices)

---

## 🎯 Overview

This guide explains how to containerize and run the **Patchy Discord Bot** using Docker. The bot is packaged into a lightweight, secure container that can run anywhere Docker is supported.

### ✨ Key Benefits

- **🔒 Secure**: Environment variables handled safely outside images
- **🚀 Portable**: Same image runs everywhere (dev, staging, production)
- **⚡ Fast**: Multi-stage builds for optimized image size
- **🔄 Consistent**: Identical environments across all deployments
- **📦 Self-contained**: All dependencies included and isolated

### 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│              Docker Container           │
│  ┌─────────────────────────────────────┐ │
│  │         Python 3.11 App             │ │
│  │  ┌─────────────┐ ┌─────────────────┐│ │
│  │  │ Discord Bot │ │ Webhook Server  ││ │
│  │  │   (Bot)     │ │   (FastAPI)     ││ │
│  │  └─────────────┘ └─────────────────┘│ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
               │         │
               ▼         ▼
         Discord API   GitHub Webhooks
```

---

## 🔧 Prerequisites

Before you begin, ensure you have:

- ✅ **Docker** installed and running ([Download Docker](https://www.docker.com/products/docker-desktop))
- ✅ **Docker Compose** (included with Docker Desktop)
- ✅ **Environment variables** configured (see [Environment Variables](#environment-variables))
- ✅ **Discord bot token** and channel ID
- ✅ **GitHub webhook secret**

---

## ⚡ Quick Start

### 🚀 Method 1: Docker Compose (Recommended)

```powershell
# 1. Copy environment template
cp .env.docker.example .env.docker

# 2. Edit environment variables (add your tokens)
# Edit .env.docker with your actual values

# 3. Build and run
docker-compose up --build

# 4. Run in background (detached mode)
docker-compose up -d --build
```

### 🔧 Method 2: Direct Docker Commands

```powershell
# 1. Build the image
docker build -t patchy-discord-bot .

# 2. Run with environment file
docker run -d --name patchy-bot -p 8000:8000 --env-file .env.docker patchy-discord-bot

# 3. Run with individual variables
docker run -d --name patchy-bot -p 8000:8000 `
  -e DISCORD_TOKEN="your_token_here" `
  -e DISCORD_CHANNEL_ID="your_channel_id" `
  -e GITHUB_WEBHOOK_SECRET="your_secret" `
  patchy-discord-bot
```

---

## 📁 Configuration

### 📂 File Structure
```
discord-bot/
├── 🐳 Dockerfile                    # Container definition
├── 🔧 docker-compose.yml           # Orchestration setup  
├── 🚫 .dockerignore                # Files excluded from build
├── 🔐 .env.docker.example          # Environment template
├── 🔐 .env                         # Your local variables (gitignored)
├── 📦 requirements.txt             # Python dependencies
└── 📚 docs/DOCKER_ENV.md          # Environment variables guide
```

### 🔄 Environment File Options

| File | Purpose | Usage |
|------|---------|-------|
| `.env` | Local development | Auto-loaded by docker-compose |
| `.env.docker` | Docker-specific | Use with `--env-file .env.docker` |
| `.env.production` | Production | Use with `--env-file .env.production` |
| `.env.staging` | Staging | Use with `--env-file .env.staging` |

   # Run in detached mode (background)
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop the container
   docker-compose down
   ```

### Method 2: Pure Docker Commands

1. **Build the image:**
   ```bash
   docker build -t patchy-discord-bot .
   ```

2. **Run with environment variables:**
   ```bash
   docker run -d \
     --name patchy-bot \
     -p 8000:8000 \
     -e DISCORD_TOKEN="your_token_here" \
     -e DISCORD_CHANNEL_ID="your_channel_id" \
     -e GITHUB_WEBHOOK_SECRET="your_secret" \
     patchy-discord-bot
   ```

3. **Or use an environment file:**
   ```bash
   docker run -d \
     --name patchy-bot \
     -p 8000:8000 \
     --env-file .env.docker \
     patchy-discord-bot
   ```

### Method 3: Using Your Existing .env File

If you want to use your existing `.env` file with Docker Compose:

```bash
# This will automatically load variables from .env file
docker-compose up
```

---

## 🌍 Environment Variables

### 🔑 Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | `MTIzNDU2Nzg5MA.GhI...` |
| `DISCORD_CHANNEL_ID` | Target Discord channel ID | `1234567890123456789` |
| `GITHUB_WEBHOOK_SECRET` | GitHub webhook secret | `my-secure-webhook-secret` |

### ⚙️ Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `8000` | Server port (auto-assigned in some platforms) |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

### 📋 Environment File Template

Create `.env.docker` from the template:

```env
# Required - Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here

# Required - GitHub Configuration  
GITHUB_WEBHOOK_SECRET=your_secure_webhook_secret_here

# Optional - Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

### 🔒 Security Notes

> **⚠️ Important**: Never commit `.env` files containing secrets to version control!

- ✅ `.env` files are gitignored by default
- ✅ Environment variables are not baked into Docker images  
- ✅ Use different secrets for different environments
- ✅ Rotate secrets regularly in production

---

## 🚀 Deployment Methods

### 🎯 Method 1: Docker Compose (Recommended)

**Best for**: Local development, testing, simple deployments

```powershell
# Start the bot
docker-compose up --build

# Run in background
docker-compose up -d --build

# View real-time logs  
docker-compose logs -f patchy-bot

# Stop the bot
docker-compose down

# Restart with new changes
docker-compose restart patchy-bot
```

**✅ Pros**: Easy setup, automatic dependency management, volume mounting  
**❌ Cons**: Requires docker-compose.yml file

### 🎯 Method 2: Pure Docker Commands

**Best for**: CI/CD pipelines, custom deployments, learning Docker

```powershell
# Build image
docker build -t patchy-discord-bot .

# Run with environment file
docker run -d --name patchy-bot -p 8000:8000 --env-file .env.docker patchy-discord-bot

# Run with manual environment variables
docker run -d --name patchy-bot -p 8000:8000 `
  -e DISCORD_TOKEN="your_token" `
  -e DISCORD_CHANNEL_ID="your_channel" `
  -e GITHUB_WEBHOOK_SECRET="your_secret" `
  patchy-discord-bot

# View logs
docker logs -f patchy-bot

# Stop and remove container
docker stop patchy-bot && docker rm patchy-bot
```

**✅ Pros**: Full control, no extra files needed  
**❌ Cons**: More verbose, manual dependency management

### 🎯 Method 3: Environment-Specific Deployments

**Best for**: Production deployments with different configurations

```powershell
# Development environment
docker-compose --env-file .env.development up -d

# Staging environment
docker-compose --env-file .env.staging up -d

# Production environment
docker-compose --env-file .env.production up -d
```

**✅ Pros**: Environment separation, easy switching  
**❌ Cons**: Requires multiple environment files

---

## 📊 Monitoring & Debugging

### 🏥 Health Monitoring

The container includes built-in health checks to monitor the webhook server:

```powershell
# Check container health status
docker-compose ps

# View detailed health check logs
docker inspect --format='{{json .State.Health}}' patchy-discord-bot

# Manual health check
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

### 📋 Viewing Logs

```powershell
# Docker Compose - Real-time logs
docker-compose logs -f patchy-bot

# Docker Compose - Last 100 lines
docker-compose logs --tail=100 patchy-bot

# Pure Docker - Real-time logs
docker logs -f patchy-discord-bot

# Pure Docker - Last 50 lines with timestamps
docker logs --tail=50 --timestamps patchy-discord-bot
```

### 🐛 Debugging Inside Container

```powershell
# Access running container shell
docker-compose exec patchy-bot /bin/bash

# Or with pure Docker
docker exec -it patchy-discord-bot /bin/bash

# View container processes
docker-compose exec patchy-bot ps aux

# Check Python environment
docker-compose exec patchy-bot python --version
docker-compose exec patchy-bot pip list
```

### 📈 Performance Monitoring

```powershell
# Container resource usage
docker stats patchy-discord-bot

# System-wide Docker resource usage
docker system df

# Container inspection
docker inspect patchy-discord-bot
```

---

## 🏭 Production Setup

### 🔧 Resource Management

Add resource limits to your `docker-compose.yml`:

```yaml
services:
  patchy-bot:
    deploy:
      resources:
        limits:
          cpus: '0.5'           # Maximum 0.5 CPU cores
          memory: 512M          # Maximum 512MB RAM
        reservations:
          memory: 256M          # Reserved 256MB RAM
    restart: unless-stopped     # Auto-restart policy
```

### 🌍 Multi-Environment Configuration

Create environment-specific files:

```
├── .env.development      # Development settings
├── .env.staging         # Staging settings  
├── .env.production      # Production settings
└── docker-compose.prod.yml  # Production compose file
```

**Example production docker-compose.prod.yml**:
```yaml
version: '3.8'
services:
  patchy-bot:
    build: .
    restart: unless-stopped
    env_file: .env.production
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 1G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 🚀 CI/CD Integration

**GitHub Actions example**:
```yaml
- name: Deploy with Docker Compose
  run: |
    docker-compose --env-file .env.production up -d --build
    
- name: Health Check
  run: |
    sleep 30
    curl -f http://localhost:8000/health
```

### 📊 Production Monitoring

```powershell
# Check production deployment
docker-compose --env-file .env.production ps

# Monitor resource usage
docker stats --no-stream

# Check logs for errors
docker-compose logs --tail=100 | Select-String "ERROR"
```

---

## 🔧 Troubleshooting

### ❓ Common Issues & Solutions

#### 🔴 Port Already in Use
**Problem**: `Error: Port 8000 is already in use`

```powershell
# Solution 1: Change port in docker-compose.yml
# Edit docker-compose.yml and change "8000:8000" to "8001:8000"

# Solution 2: Stop conflicting process
netstat -ano | Select-String ":8000"    # Find process using port
Stop-Process -Id <PID>                  # Kill the process

# Solution 3: Use different port in environment
$env:PORT=8001; docker-compose up
```

#### 🔴 Environment Variables Not Loading
**Problem**: Bot can't connect to Discord or webhook fails

```powershell
# Check if .env file exists and has correct format
Get-Content .env.docker

# Verify no spaces around = in environment files
# ❌ WRONG: DISCORD_TOKEN = your_token
# ✅ RIGHT: DISCORD_TOKEN=your_token

# Test with explicit variables
docker run --env-file .env.docker -it patchy-discord-bot env | Select-String "DISCORD"
```

#### 🔴 Container Keeps Restarting
**Problem**: Container starts then immediately stops

```powershell
# Check container logs for errors
docker-compose logs patchy-bot

# Common causes:
# - Missing required environment variables
# - Invalid Discord token  
# - Python syntax errors
# - Missing dependencies in requirements.txt

# Debug: Run container interactively
docker run -it --env-file .env.docker patchy-discord-bot /bin/bash
```

#### 🔴 Health Check Failing
**Problem**: Docker reports container as unhealthy

```powershell
# Check health check logs
docker inspect --format='{{json .State.Health}}' patchy-discord-bot | ConvertFrom-Json

# Manual health check
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Common causes:
# - Webhook server not starting
# - Port 8000 not accessible inside container
# - FastAPI application errors
```

#### 🔴 Discord Messages Not Appearing
**Problem**: Webhooks received but no Discord notifications

```powershell
# Check Discord bot token and permissions
docker-compose logs | Select-String "discord"

# Verify bot is in the Discord server
# Verify channel ID is correct
# Check bot permissions: "Send Messages", "Embed Links"

# Test Discord connection
docker-compose exec patchy-bot python -c "
import discord
client = discord.Client()
print('Discord connection test')
"
```

### 🛠️ Debugging Commands

```powershell
# View all Docker containers
docker ps -a

# Check Docker images
docker images

# View container resource usage
docker stats --no-stream

# Inspect container configuration
docker inspect patchy-discord-bot

# Test network connectivity inside container
docker-compose exec patchy-bot curl -I http://localhost:8000/health

# View environment variables inside container  
docker-compose exec patchy-bot env | Sort-Object
```

### 🧹 Cleanup Commands

```powershell
# Stop and remove containers
docker-compose down

# Remove stopped containers  
docker container prune -f

# Remove unused images
docker image prune -f

# Remove everything (containers, images, volumes, networks)
docker system prune -a -f

# Remove specific image
docker rmi patchy-discord-bot
```

---

## 🔒 Security Best Practices

### 🛡️ Container Security

1. **🚫 Never Commit Secrets**
   ```powershell
   # Verify .env files are gitignored
   git status --ignored | Select-String ".env"
   
   # Check for accidentally committed secrets
   git log --oneline -S "discord_token" --all
   ```

2. **🔄 Use Specific Image Tags**
   ```dockerfile
   # ❌ Avoid using 'latest' in production
   FROM python:latest
   
   # ✅ Use specific versions
   FROM python:3.11-slim
   ```

3. **👤 Run as Non-Root User**
   ```dockerfile
   # Already implemented in our Dockerfile
   RUN adduser --disabled-password --gecos '' --uid 1000 appuser
   USER appuser
   ```

### 🔐 Environment Security

1. **📋 Environment File Permissions**
   ```powershell
   # Restrict access to environment files (Unix-like systems)
   icacls .env.docker /grant:r "$(whoami):F" /inheritance:r
   ```

2. **🔄 Secret Rotation**
   ```powershell
   # Rotate secrets regularly
   # 1. Generate new webhook secret
   # 2. Update GitHub webhook settings
   # 3. Update environment file
   # 4. Restart containers
   docker-compose restart
   ```

3. **🏷️ Environment Separation**
   ```
   # Different secrets for each environment
   .env.development     # Development secrets
   .env.staging        # Staging secrets  
   .env.production     # Production secrets
   ```

### 🔍 Security Monitoring

1. **📊 Regular Image Scanning**
   ```powershell
   # Scan for vulnerabilities (if available)
   docker scan patchy-discord-bot
   
   # Update base images regularly
   docker build --pull --no-cache -t patchy-discord-bot .
   ```

2. **📋 Security Checklist**
   - ✅ No secrets in Docker images
   - ✅ Environment files gitignored
   - ✅ Running as non-root user
   - ✅ Resource limits configured  
   - ✅ Health checks implemented
   - ✅ Logs monitored for security events
   - ✅ Regular security updates applied

---

## 🎯 Next Steps

### 🚀 Advanced Features

1. **🔄 Container Orchestration**
   - Deploy with **Kubernetes** for production scaling
   - Use **Docker Swarm** for simple clustering
   - Implement **load balancing** for high availability

2. **📊 Observability**
   ```yaml
   # Add to docker-compose.yml
   logging:
     driver: "fluentd"
     options:
       fluentd-address: "localhost:24224"
   ```

3. **📈 Monitoring Stack**
   - **Prometheus** for metrics collection
   - **Grafana** for visualization  
   - **Alertmanager** for notifications

### 🔗 Integration Options

1. **☁️ Cloud Deployment**
   - **AWS ECS** for managed containers
   - **Google Cloud Run** for serverless containers
   - **Azure Container Instances** for simple deployments

2. **🔄 CI/CD Integration**
   - **GitHub Actions** for automated deployments
   - **Jenkins** for enterprise CI/CD
   - **GitLab CI** for integrated DevOps

---

## 📚 Additional Resources

- **📖 Docker Documentation**: [docs.docker.com](https://docs.docker.com)
- **🐳 Docker Compose Reference**: [docs.docker.com/compose](https://docs.docker.com/compose)
- **🔐 Environment Variables Guide**: [`docs/DOCKER_ENV.md`](./DOCKER_ENV.md)
- **⚡ Local Testing Guide**: [`docs/LOCAL_TESTING.md`](./LOCAL_TESTING.md)
- **🚀 Railway Deployment**: [`docs/RAILWAY_DEPLOYMENT.md`](./RAILWAY_DEPLOYMENT.md)

---

> **🎉 Success!** Your Patchy Discord Bot is now containerized and ready for deployment anywhere Docker runs!