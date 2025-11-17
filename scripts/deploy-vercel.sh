#!/bin/bash
set -euo pipefail

echo "🚀 Deploying to Vercel..."

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

cd "$ROOT_DIR"

TOKEN_ARGS=()
if [[ -n "${VERCEL_TOKEN:-}" ]]; then
    TOKEN_ARGS+=(--token "$VERCEL_TOKEN")
fi

echo "📦 Deploying frontend to Vercel (servers/nextjs)..."
vercel --prod --yes "${TOKEN_ARGS[@]}"

echo "✅ Vercel deployment initiated!"
echo "🌐 Your app will be available at: https://presenton-1.vercel.app"
echo "📊 Check deployment status at: https://vercel.com/dashboard"
