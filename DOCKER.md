# Docker Containerization Guide

## Overview
This document explains how to containerize and run the Patchy Discord Bot using Docker.

## Why .env Files Are Ignored

The `.env` file is excluded from Docker containers for several important reasons:

### Security
- Prevents sensitive data (API keys, tokens) from being baked into Docker images
- Ensures secrets don't get accidentally shared with image registries
- Follows security best practices for container deployment

### Environment Flexibility
- Same Docker image can be used across different environments (dev, staging, prod)
- Configuration is provided at runtime, not build time
- Supports the "build once, deploy anywhere" principle

## Docker Setup

### Prerequisites
- Docker installed and running
- Docker Compose (usually included with Docker Desktop)

### Files Structure
```
discord-bot/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration setup
├── .dockerignore           # Files to exclude from container
├── .env                    # Your local environment variables (ignored by Docker)
├── .env.docker.example     # Template for Docker environment variables
└── requirements.txt        # Python dependencies
```

## Usage Methods

### Method 1: Docker Compose (Recommended)

1. **Copy your environment variables:**
   ```bash
   cp .env.docker.example .env.docker
   # Edit .env.docker with your actual values
   ```

2. **Run with Docker Compose:**
   ```bash
   # Build and run
   docker-compose up --build

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

## Environment Variables

Required variables:
- `DISCORD_TOKEN` - Your Discord bot token
- `DISCORD_CHANNEL_ID` - Target Discord channel ID
- `GITHUB_WEBHOOK_SECRET` - GitHub webhook secret

Optional variables:
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: false)
- `LOG_LEVEL` - Logging level (default: INFO)

## Health Monitoring

The container includes a health check that verifies the webhook server is responding:

```bash
# Check container health
docker-compose ps

# View health check logs
docker inspect --format='{{json .State.Health}}' patchy-discord-bot
```

## Logs and Debugging

### View logs:
```bash
# Docker Compose
docker-compose logs -f

# Pure Docker
docker logs -f patchy-discord-bot
```

### Debug inside container:
```bash
# Access running container
docker-compose exec patchy-bot /bin/bash

# Or with pure Docker
docker exec -it patchy-discord-bot /bin/bash
```

## Production Deployment

### Environment-Specific Files
Create separate environment files for different deployment environments:
- `.env.development`
- `.env.staging`
- `.env.production`

### Using with CI/CD
```yaml
# Example GitHub Actions step
- name: Deploy with Docker Compose
  run: |
    docker-compose --env-file .env.production up -d
```

### Resource Limits
Add resource limits to docker-compose.yml:
```yaml
services:
  patchy-bot:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in docker-compose.yml or .env file
   PORT=8001
   ```

2. **Environment variables not loaded:**
   - Verify `.env` file exists and has correct format
   - Ensure no spaces around `=` in environment files
   - Check file permissions

3. **Container keeps restarting:**
   ```bash
   # Check logs for errors
   docker-compose logs patchy-bot
   ```

4. **Health check failing:**
   - Verify webhook server is starting correctly
   - Check if port 8000 is accessible inside container
   - Review application logs

### Cleaning Up
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi patchy-discord-bot

# Clean up all unused Docker resources
docker system prune -a
```

## Security Best Practices

1. **Never commit .env files** to version control
2. **Use specific image tags** in production instead of `latest`
3. **Regularly update base images** for security patches
4. **Run containers as non-root user** (already implemented)
5. **Use secrets management** in production environments
6. **Scan images for vulnerabilities** before deployment

## Next Steps

- Set up container orchestration (Kubernetes, Docker Swarm)
- Implement log aggregation (ELK stack, Fluentd)
- Add monitoring (Prometheus, Grafana)
- Configure backup strategies for persistent data