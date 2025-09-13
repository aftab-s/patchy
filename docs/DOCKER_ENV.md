# 🔧 Docker Environment Variables Guide

> **Complete guide to managing environment variables in Docker deployments**

## � Table of Contents

1. [Overview](#overview)
2. [Environment Variable Methods](#environment-variable-methods)
3. [File-Based Configuration](#file-based-configuration)
4. [Docker Compose Strategies](#docker-compose-strategies)
5. [Security Best Practices](#security-best-practices)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Techniques](#advanced-techniques)

---

## 🎯 Overview

Docker environment variables provide configuration data to containers without hardcoding values into images. This enables the same Docker image to run in different environments (development, staging, production) with different configurations.

### 🔒 Why Environment Variables Matter

- **🛡️ Security**: Keep secrets out of Docker images and code
- **🔄 Flexibility**: Same image works across all environments
- **📦 Portability**: Configuration separate from application logic
- **🔧 Maintainability**: Easy to update without rebuilding images

### 🏗️ Environment Variable Flow

```
.env file → Docker Compose → Container → Application
    ↓            ↓              ↓           ↓
Configuration → Runtime → Environment → Python os.getenv()
```

---

## 🚀 Environment Variable Methods

### 🎯 Method 1: Docker Compose with .env file (Recommended)

**Best for**: Local development, consistent environments

```powershell
# 1. Ensure your .env file exists with all required variables
# (Docker Compose automatically loads .env from project root)

# 2. Run with Docker Compose  
docker-compose up --build

# 3. Run in background (detached mode)
docker-compose up -d --build

# 4. View logs with environment context
docker-compose logs -f patchy-bot
```

**✅ Pros**: Simple, automatic loading, version controlled (template)  
**❌ Cons**: Limited to single environment file

### 🎯 Method 2: Docker Compose with Custom Environment File

**Best for**: Multiple environments, production deployments

```powershell
# Use specific environment file
docker-compose --env-file .env.docker up --build
docker-compose --env-file .env.staging up --build  
docker-compose --env-file .env.production up --build

# Example production deployment
docker-compose --env-file .env.production up -d --build
docker-compose --env-file .env.production logs -f
```

**✅ Pros**: Environment separation, flexible file naming  
**❌ Cons**: Must specify file explicitly

### 🎯 Method 3: Direct Docker Commands

**Best for**: CI/CD pipelines, scripts, fine-grained control

```powershell
# Build the image
docker build -t patchy-discord-bot .

# Option A: Environment variables from file
docker run -d `
  --name patchy-bot `
  -p 8000:8000 `
  --env-file .env `
  patchy-discord-bot

# Option B: Individual environment variables
docker run -d `
  --name patchy-bot `
  -p 8000:8000 `
  -e DISCORD_TOKEN="your_token_here" `
  -e DISCORD_CHANNEL_ID="your_channel_id" `
  -e GITHUB_WEBHOOK_SECRET="your_secret" `
  patchy-discord-bot

# Option C: Environment variables from custom file
docker run -d `
  --name patchy-bot `
  -p 8000:8000 `
  --env-file .env.production `
  patchy-discord-bot
```

**✅ Pros**: Maximum control, scripting friendly  
**❌ Cons**: More verbose, manual management

### 🎯 Method 4: Mixed Approach

**Best for**: Complex deployments with overrides

```powershell
# Use environment file + override specific variables
docker run -d `
  --name patchy-bot `
  --env-file .env.production `
  -e DEBUG=true `
  -e LOG_LEVEL=DEBUG `
  patchy-discord-bot
```

**✅ Pros**: Flexible, override capabilities  
**❌ Cons**: Can be confusing to track
---

## 📁 File-Based Configuration

### 📋 Environment File Templates

Create different environment files for different scenarios:

#### `.env` (Default - Local Development)
```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here

# GitHub Configuration  
GITHUB_WEBHOOK_SECRET=your_secure_webhook_secret_here

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
HOST=0.0.0.0
PORT=8000
```

#### `.env.docker` (Docker-Specific)
```env  
# Docker-optimized settings
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here
GITHUB_WEBHOOK_SECRET=your_secure_webhook_secret_here

# Docker settings
DEBUG=false
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Docker-specific optimizations
PYTHONUNBUFFERED=1
PYTHONIOENCODING=utf-8
```

#### `.env.production` (Production Deployment)
```env
# Production configuration
DISCORD_TOKEN=your_production_discord_token
DISCORD_CHANNEL_ID=your_production_channel_id
GITHUB_WEBHOOK_SECRET=your_production_webhook_secret

# Production settings
DEBUG=false
LOG_LEVEL=WARNING
HOST=0.0.0.0
PORT=8000

# Performance optimizations  
PYTHONUNBUFFERED=1
PYTHONOPTIMIZE=2
```

#### `.env.staging` (Staging Environment)
```env
# Staging configuration
DISCORD_TOKEN=your_staging_discord_token
DISCORD_CHANNEL_ID=your_staging_channel_id  
GITHUB_WEBHOOK_SECRET=your_staging_webhook_secret

# Staging settings (more verbose than production)
DEBUG=false
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### � File Usage Examples

```powershell
# Use different files for different environments
docker-compose --env-file .env.development up      # Development
docker-compose --env-file .env.staging up          # Staging  
docker-compose --env-file .env.production up -d    # Production

# Override with additional variables
docker-compose --env-file .env.production up -d -e DEBUG=true
```

---

## 🔄 Docker Compose Strategies

### 🎯 Strategy 1: Single Compose File with Environment Files

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  patchy-bot:
    build: .
    restart: unless-stopped
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - DISCORD_CHANNEL_ID=${DISCORD_CHANNEL_ID}
      - GITHUB_WEBHOOK_SECRET=${GITHUB_WEBHOOK_SECRET}
      - DEBUG=${DEBUG:-false}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
```

**Usage**:
```powershell
# Uses .env by default
docker-compose up

# Uses specific environment file
docker-compose --env-file .env.production up -d
```

### 🎯 Strategy 2: Multiple Compose Files

**docker-compose.yml** (Base):
```yaml
version: '3.8'
services:
  patchy-bot:
    build: .
    ports:
      - "8000:8000"
```

**docker-compose.prod.yml** (Production Override):
```yaml
version: '3.8'
services:
  patchy-bot:
    restart: unless-stopped
    env_file: .env.production
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

**Usage**:
```powershell  
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 🎯 Strategy 3: Environment-Specific Compose Files

Create separate compose files:
- `docker-compose.dev.yml`
- `docker-compose.staging.yml`  
- `docker-compose.prod.yml`

```powershell
# Use environment-specific compose file
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔒 Security Best Practices

### 🛡️ File Security

#### 1. Environment File Hierarchy (Priority Order)
```
1. .env.local          # Highest priority - local overrides
2. .env.production     # Environment-specific values
3. .env.docker         # Docker-specific defaults
4. .env                # Base configuration (lowest priority)
```

#### 2. Proper .gitignore Configuration
```gitignore
# Secure environment files
.env
.env.local
.env.*.local
.env.production
.env.staging

# Keep templates in git
!.env.example
!.env.docker.example

# Other sensitive files
values.txt
secrets/
```

#### 3. File Permissions (Unix-like systems)
```bash
# Restrict access to environment files
chmod 600 .env.production      # Owner read/write only  
chmod 644 .env.docker.example  # Public template
```

### � Docker Secrets (Production)

For production environments, consider Docker secrets:

#### docker-compose.prod.yml with Secrets:
```yaml
version: '3.8'
services:
  patchy-bot:
    build: .
    secrets:
      - discord_token
      - webhook_secret
    environment:
      - DISCORD_TOKEN_FILE=/run/secrets/discord_token
      - GITHUB_WEBHOOK_SECRET_FILE=/run/secrets/webhook_secret

secrets:
  discord_token:
    external: true
  webhook_secret:
    external: true
```

#### Create Docker Secrets:
```powershell
# Create secrets (requires Docker Swarm mode)
echo "your_discord_token" | docker secret create discord_token -
echo "your_webhook_secret" | docker secret create webhook_secret -

# Deploy with secrets
docker stack deploy -c docker-compose.prod.yml patchy-bot-stack
```

### 🔍 Security Validation

```powershell
# Check that secrets aren't in images
docker history patchy-discord-bot | Select-String "TOKEN"

# Verify environment variables in container
docker exec patchy-bot env | Select-String "DISCORD" | Select-String -NotMatch "TOKEN"

# Check file permissions
docker exec patchy-bot ls -la /run/secrets/
```

### Common Issues

1. **Environment file not found**
   ```
   Solution: Ensure .env file exists in same directory as docker-compose.yml
   ```

2. **Variables not loaded**
   ```
   Solution: Check file format - no spaces around = signs
   DISCORD_TOKEN=value  ✅
   DISCORD_TOKEN = value  ❌
   ```

3. **Permission errors**
   ```
   Solution: Check file permissions
   chmod 600 .env.docker
   ```

## 📝 Environment File Templates

### .env.docker.example (Template)
```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here

# GitHub Webhook Configuration  
GITHUB_WEBHOOK_SECRET=your_github_webhook_secret_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO

# Docker-specific settings
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### .env.production (Production Template)
```env
# Production Discord Bot Configuration
DISCORD_TOKEN=prod_bot_token
DISCORD_CHANNEL_ID=prod_channel_id

# Production GitHub Webhook Configuration
GITHUB_WEBHOOK_SECRET=prod_webhook_secret

# Production Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=WARNING

# Production optimizations
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

## 🚀 Quick Start Commands

```bash
# Development
docker-compose up --build

# Production
docker-compose --env-file .env.production up -d

# Custom environment
docker-compose --env-file .env.staging up -d

# View logs
docker-compose logs -f patchy-bot

# Stop
docker-compose down
```