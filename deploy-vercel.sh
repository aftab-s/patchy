#!/bin/bash

# Deploy Patchy to Vercel
# This script helps automate the deployment process

set -e

echo "🚀 Deploying Patchy - GitHub Discord Webhook Bot to Vercel"
echo "=========================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Installing..."
    npm install -g vercel
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel:"
    vercel login
fi

echo "📦 Deploying to Vercel..."
vercel

echo "🔧 Setting up environment variables..."
echo "Please enter your environment variables:"

# Get Discord Token
read -p "Discord Bot Token: " DISCORD_TOKEN
vercel env add DISCORD_TOKEN <<< "$DISCORD_TOKEN"

# Get Discord Channel ID
read -p "Discord Channel ID: " DISCORD_CHANNEL_ID
vercel env add DISCORD_CHANNEL_ID <<< "$DISCORD_CHANNEL_ID"

# Get GitHub Webhook Secret
read -p "GitHub Webhook Secret: " GITHUB_WEBHOOK_SECRET
vercel env add GITHUB_WEBHOOK_SECRET <<< "$GITHUB_WEBHOOK_SECRET"

echo "🚀 Deploying to production..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get your webhook URL from the deployment output"
echo "2. Configure GitHub webhook with your URL"
echo "3. Test by making a commit to your repository"
echo ""
echo "🔗 Your webhook endpoint will be: https://your-project.vercel.app/webhook"
echo "🏥 Health check endpoint: https://your-project.vercel.app/health"
