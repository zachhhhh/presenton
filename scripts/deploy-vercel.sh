#!/bin/bash

echo "🚀 Deploying to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Deploy to Vercel
echo "📦 Deploying frontend to Vercel..."
vercel --prod

echo "✅ Vercel deployment initiated!"
echo "🌐 Your app will be available at: https://presenton-1.vercel.app"
echo "📊 Check deployment status at: https://vercel.com/dashboard"