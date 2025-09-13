# 📁 Project Structure Guide

This document explains the organized structure of the Patchy Discord Bot project.

## 🏗️ Directory Structure

```
discord-bot/
├── 📄 Core Application Files (Essential)
│   ├── main.py                 # Main application entry point
│   ├── discord_bot.py          # Discord bot implementation  
│   ├── webhook_server.py       # FastAPI webhook server
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── railway.json          # Railway deployment config
│   ├── Procfile              # Process definition
│   ├── env.example           # Environment variables template
│   └── README.md             # Main project documentation
│
├── � Docker Files (Important)
│   ├── Dockerfile            # Container definition
│   ├── docker-compose.yml    # Container orchestration
│   ├── .dockerignore         # Docker ignore rules
│   └── .env.docker.example   # Docker environment template
│
├── �📚 docs/                   # Documentation
│   ├── DOCKER.md             # Docker containerization guide
│   ├── LOCAL_TESTING.md      # Local development testing
│   ├── RAILWAY_DEPLOYMENT.md # Railway deployment guide
│   └── VERCEL_DEPLOYMENT.md  # Vercel deployment guide
│
├── 🛠️ dev-tools/             # Development & Testing Tools
│   ├── test_webhook.py       # Original webhook testing
│   ├── test_railway.py       # Railway-specific testing
│   ├── local_test.py         # Local development testing utility
│   ├── local-dev.ps1         # PowerShell development helper
│   └── run_dev.py            # Development runner
│
└── 📦 optional/              # Optional Platform Files
    ├── setup.py              # Package setup (if needed)
    └── deployments/          # Alternative deployment platforms
        ├── vercel.json       # Vercel configuration
        ├── render.yaml       # Render configuration  
        ├── requirements-vercel.txt # Vercel dependencies
        ├── deploy-vercel.ps1 # Vercel deployment script
        ├── deploy-vercel.sh  # Vercel deployment script (bash)
        └── api/              # Vercel serverless functions
            ├── health.py     # Serverless health endpoint
            ├── webhook.py    # Serverless webhook endpoint
            └── requirements.txt # API dependencies
```

## 🎯 File Categories

### ✅ **Essential Files** (9 files - keep in root)
These files are required for the basic Railway deployment:
- Core application code
- Railway configuration  
- Environment template
- Main documentation

### � **Docker Files** (4 files - important for containerization)
Docker containerization setup for flexible deployment:
- Container definition and orchestration
- Docker-specific configuration and environment

### �📚 **Documentation** (`docs/` folder)
All markdown documentation files for different aspects of the project:
- Docker setup and usage
- Local development and testing
- Deployment guides for different platforms

### 🛠️ **Development Tools** (`dev-tools/` folder)  
Testing utilities and development helpers:
- Testing scripts for different scenarios
- Development automation tools
- Local development utilities

### 📦 **Optional Files** (`optional/` folder)
Files for alternative deployment methods or advanced features:

#### `optional/deployments/`
Configuration files for alternative deployment platforms:
- Vercel (serverless)
- Render (cloud platform)
- Associated deployment scripts and dependencies

## 🚀 Usage Based on Your Needs

### **Just Want to Run on Railway?**
You only need the core files:
```
✅ Use: Core application files (root directory)
❌ Ignore: docs/, dev-tools/, optional/
```

### **Want to Use Docker?**
Use Docker setup:
```  
✅ Use: Core files + Docker files (all in root)
📚 Reference: docs/DOCKER.md
```

### **Want to Test Locally?**
Use development tools:
```
✅ Use: Core files + dev-tools/
📚 Reference: docs/LOCAL_TESTING.md
```

### **Want to Deploy to Vercel?**
Use Vercel configuration:
```
✅ Use: Core files + optional/deployments/
📚 Reference: docs/VERCEL_DEPLOYMENT.md  
```

## 🧹 Benefits of This Structure

- **🎯 Clear Separation**: Essential vs optional files
- **� Docker Ready**: Docker files easily accessible in root
- **�📚 Organized Documentation**: All guides in one place
- **🛠️ Isolated Dev Tools**: Testing tools don't clutter main directory
- **📦 Platform Flexibility**: Easy to find platform-specific files
- **🚀 Simple Deployment**: Core files stay in root for easy deployment
- **🔍 Easy Navigation**: Logical folder structure

## 🔧 Updating File Paths

If you use any of the moved files, update your references:

**Old Paths** → **New Paths**
```bash
# Documentation
DOCKER.md → docs/DOCKER.md
LOCAL_TESTING.md → docs/LOCAL_TESTING.md

# Development Tools  
test_railway.py → dev-tools/test_railway.py
local-dev.ps1 → dev-tools/local-dev.ps1

# Docker Files (now in root - no path change needed)
Dockerfile → Dockerfile (✅ in root)
docker-compose.yml → docker-compose.yml (✅ in root)

# Alternative Deployments
vercel.json → optional/deployments/vercel.json
api/ → optional/deployments/api/
```

## 💡 Pro Tips

- **Keep root directory clean** for easy deployment
- **Use dev-tools/** for local development and testing
- **Reference docs/** for setup and configuration guides
- **Explore optional/** when you need alternative deployment methods
- **Delete unused folders** if you don't need them (e.g., delete `optional/docker/` if you don't use Docker)

This structure makes your project more maintainable and easier to navigate! 🎉