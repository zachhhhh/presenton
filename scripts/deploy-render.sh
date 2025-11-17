#!/bin/bash

echo "🚀 Deploying to Render..."

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found. Installing..."
    npm install -g @render/cli
fi

# Deploy to Render
echo "📦 Deploying backend to Render..."
render deploy

echo "✅ Render deployment initiated!"
echo "🌐 Your app will be available at: https://presenton-api.onrender.com"
echo "📊 Check deployment status at: https://dashboard.render.com/web/presenton-api"