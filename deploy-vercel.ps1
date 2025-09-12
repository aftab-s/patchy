# Deploy Patchy to Vercel
# This PowerShell script helps automate the deployment process

Write-Host "🚀 Deploying Patchy - GitHub Discord Webhook Bot to Vercel" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "npm install -g vercel" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in
try {
    vercel whoami | Out-Null
    Write-Host "✅ Logged in to Vercel" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please log in to Vercel:" -ForegroundColor Yellow
    vercel login
}

Write-Host "📦 Deploying to Vercel..." -ForegroundColor Blue
vercel

Write-Host "🔧 Setting up environment variables..." -ForegroundColor Blue
Write-Host "Please enter your environment variables:" -ForegroundColor Yellow

# Get Discord Token
$DISCORD_TOKEN = Read-Host "Discord Bot Token"
Write-Output $DISCORD_TOKEN | vercel env add DISCORD_TOKEN

# Get Discord Channel ID
$DISCORD_CHANNEL_ID = Read-Host "Discord Channel ID"
Write-Output $DISCORD_CHANNEL_ID | vercel env add DISCORD_CHANNEL_ID

# Get GitHub Webhook Secret
$GITHUB_WEBHOOK_SECRET = Read-Host "GitHub Webhook Secret"
Write-Output $GITHUB_WEBHOOK_SECRET | vercel env add GITHUB_WEBHOOK_SECRET

Write-Host "🚀 Deploying to production..." -ForegroundColor Blue
vercel --prod

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Get your webhook URL from the deployment output" -ForegroundColor White
Write-Host "2. Configure GitHub webhook with your URL" -ForegroundColor White
Write-Host "3. Test by making a commit to your repository" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Your webhook endpoint will be: https://your-project.vercel.app/webhook" -ForegroundColor Cyan
Write-Host "🏥 Health check endpoint: https://your-project.vercel.app/health" -ForegroundColor Cyan
