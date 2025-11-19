#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOTENV_FILE="$ROOT_DIR/.env"

if [[ -f "$DOTENV_FILE" ]]; then
    # shellcheck disable=SC1090
    set -a
    source "$DOTENV_FILE"
    set +a
fi

cd "$ROOT_DIR"

echo "🚀 Deploying to Render..."

WORKSPACE_ID=$(render workspace current --output json | python3 -c '
import json, sys
print(json.load(sys.stdin)["id"])
')
export RENDER_WORKSPACE="$WORKSPACE_ID"

if ! command -v render &> /dev/null; then
    cat <<'EOF'
❌ Render CLI not found.

Please install the official Render CLI or trigger a deploy from the Render dashboard:
https://render.com/docs/cli

Once the CLI is available in PATH, re-run this script to kick off a deployment.
EOF
    exit 1
fi

SERVICE_ID=$(render services --output json | python3 -c '
import json, sys
services = json.load(sys.stdin)
if not services:
    raise SystemExit("No services found in Render workspace")
print(services[0]["service"]["id"])
')

echo "📦 Deploying backend to Render..."
render deploys create "$SERVICE_ID" --confirm --output json

echo "✅ Render deployment initiated!"
echo "🌐 Your app will be available at: https://presenton-api.onrender.com"
echo "📊 Check deployment status at: https://dashboard.render.com/web/presenton-api"
