#!/bin/bash
set -euo pipefail

echo "🚀 Deploying to Render..."

if ! command -v render &> /dev/null; then
    cat <<'EOF'
❌ Render CLI not found.

Please install the official Render CLI or trigger a deploy from the Render dashboard:
https://render.com/docs/cli

Once the CLI is available in PATH, re-run this script to kick off a deployment.
EOF
    exit 1
fi

echo "📦 Deploying backend to Render..."
render deploy

echo "✅ Render deployment initiated!"
echo "🌐 Your app will be available at: https://presenton-api.onrender.com"
echo "📊 Check deployment status at: https://dashboard.render.com/web/presenton-api"
